# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Security Audit Environment Implementation.

Simulates real-world VAPT engagements where an AI agent audits
infrastructure for security vulnerabilities and compliance gaps.
"""

import random
from copy import deepcopy
from typing import Optional
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment

try:
    from ..models import SecurityAuditAction, SecurityAuditObservation, SecurityAuditState
except ImportError:
    from models import SecurityAuditAction, SecurityAuditObservation, SecurityAuditState

try:
    from .scenarios import get_scenario, list_scenarios
    from .tools_engine import TOOL_DEFINITIONS, execute_tool
    from .grader import grade_episode, match_single_finding
except ImportError:
    from server.scenarios import get_scenario, list_scenarios
    from server.tools_engine import TOOL_DEFINITIONS, execute_tool
    from server.grader import grade_episode, match_single_finding


class SecurityAuditEnvironment(Environment):
    """
    AI Security Audit Training Environment.

    Simulates real-world Vulnerability Assessment & Penetration Testing (VAPT)
    engagements. The agent discovers hosts, scans services, identifies
    vulnerabilities, and submits structured findings — just like a
    professional security auditor.

    Three scenarios with increasing difficulty:
    - Easy: Startup web app (2 hosts, 3 vulns)
    - Medium: E-commerce platform (4 hosts, 6 vulns)
    - Hard: Enterprise SOC2 audit (6 hosts, 10 vulns + honeypots)
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    # Difficulty multiplier for per-step tool/finding rewards
    _DIFFICULTY_REWARD_MULTIPLIER = {"easy": 1.0, "medium": 1.3, "hard": 1.6}

    def __init__(self):
        super().__init__()
        self._state = SecurityAuditState()
        self._scenario = None
        self._discovered_hosts: list = []
        self._discovered_ports: dict = {}
        self._discovered_services: dict = {}
        self._submitted_findings: list = []
        self._action_history: list = []
        self._discovered_vulns: set = set()
        self._episode_reward: float = 0.0
        self._last_tool_call: tuple = ()
        self._rng: random.Random = random.Random()
        # Multi-agent extension: dynamic attack surface + sub-agent registry.
        # ``_attack_surface`` starts as the original scenario hosts and grows
        # whenever tools reveal new targets (e.g. SSRF dumping internal IPs).
        # ``_active_subagents`` tracks delegated investigation branches keyed
        # by spawn_id; each entry carries scope/target/budget/findings/parent_step.
        self._attack_surface: set = set()
        self._revealed_targets: list = []
        self._active_subagents: dict = {}
        self._subagent_outcomes: list = []  # for grader's Delegation Score

    def reset(self, seed=None, episode_id=None, **kwargs) -> SecurityAuditObservation:
        """Reset the environment for a new audit engagement.

        kwargs:
            scenario_id: "easy", "medium", or "hard" (default: "easy")
        """
        scenario_id = kwargs.get("scenario_id", "easy")
        self._scenario = deepcopy(get_scenario(scenario_id))

        self._discovered_hosts = []
        self._discovered_ports = {}
        self._discovered_services = {}
        self._submitted_findings = []
        self._action_history = []
        self._discovered_vulns = set()
        self._episode_reward = 0.0
        self._last_tool_call = ()
        self._rng = random.Random(seed) if seed is not None else random.Random()
        # Reset multi-agent state. Attack surface seeds from initial *visible*
        # hosts only — hidden hosts (those gated by `hidden_until`) only join
        # the attack surface when revealed by tool calls, which is what makes
        # spawn_subagent meaningful as a delegation primitive.
        self._attack_surface = {
            ip for ip, info in (self._scenario or {}).get("hosts", {}).items()
            if not info.get("hidden_until")
        }
        self._revealed_targets = []
        self._active_subagents = {}
        self._subagent_outcomes = []

        eid = episode_id or str(uuid4())
        self._state = SecurityAuditState(
            episode_id=eid,
            step_count=0,
            scenario_id=scenario_id,
            scenario_name=self._scenario["name"],
            target_network=self._scenario["target_network"],
            max_steps=self._scenario["max_steps"],
        )

        self._reset_rubric()

        return SecurityAuditObservation(
            tool_output="",
            message=self._scenario["briefing"],
            discovered_hosts=[],
            discovered_services={},
            findings_submitted=0,
            steps_remaining=self._scenario["max_steps"],
            done=False,
            reward=0.0,
        )

    def step(self, action: SecurityAuditAction, **kwargs) -> SecurityAuditObservation:
        self._state.step_count += 1
        steps_remaining = self._state.max_steps - self._state.step_count

        # Sub-agent budget accounting: if a sub-agent is currently active, every
        # step (other than the spawn that created it, or its own return_to_parent)
        # consumes one budget unit. Auto-close on exhaustion so the env never
        # gets stuck in a sub-context.
        active_sid = self._active_subagent_id()
        if active_sid and action.action_type not in ("spawn_subagent",):
            sub = self._active_subagents[active_sid]
            sub["steps_used"] += 1
            if sub["steps_used"] > sub["budget"] and action.action_type != "return_to_parent":
                # Auto-close as unproductive-by-timeout. Surface this to the
                # agent so it knows control is back at the parent.
                sub["status"] = "completed"
                sub["timeout"] = True
                findings_added = len(self._submitted_findings) - sub["findings_at_spawn"]
                productive = findings_added >= 1
                sub["productive"] = productive
                self._subagent_outcomes.append({
                    "spawn_id": active_sid,
                    "scope": sub["scope"],
                    "target": sub["target"],
                    "budget": sub["budget"],
                    "steps_used": sub["steps_used"],
                    "findings_added": findings_added,
                    "productive": productive,
                    "timeout": True,
                    "spawn_step": sub["spawn_step"],
                    "closed_at_step": self._state.step_count,
                })
                # The agent's current action still runs at the parent layer.
                # We just clear the active sub-agent flag here.

        self._action_history.append({
            "step": self._state.step_count,
            "action_type": action.action_type,
            "tool_name": action.tool_name,
            "arguments": action.arguments,
            "spawn_id": self._active_subagent_id(),
        })

        if steps_remaining <= 0:
            return self._finish_episode("Step limit reached. Audit terminated.", truncated=True)

        if action.action_type == "list_tools":
            return self._handle_list_tools(steps_remaining)
        elif action.action_type == "use_tool":
            return self._handle_use_tool(action, steps_remaining)
        elif action.action_type == "submit_finding":
            return self._handle_submit_finding(action, steps_remaining)
        elif action.action_type == "spawn_subagent":
            return self._handle_spawn_subagent(action, steps_remaining)
        elif action.action_type == "return_to_parent":
            return self._handle_return_to_parent(action, steps_remaining)
        elif action.action_type == "generate_report":
            return self._finish_episode("Audit report generated.", truncated=False)
        else:
            return SecurityAuditObservation(
                tool_output=f"Unknown action_type: {action.action_type}",
                message="Use list_tools, use_tool, submit_finding, spawn_subagent, or generate_report.",
                discovered_hosts=self._discovered_hosts,
                discovered_services=self._discovered_services,
                findings_submitted=len(self._submitted_findings),
                steps_remaining=steps_remaining,
                current_phase=self._current_phase(),
                done=False,
                reward=-0.05,
            )

    def _active_subagent_id(self) -> Optional[str]:
        """Return the currently-active sub-agent spawn_id, if any."""
        for sid, info in self._active_subagents.items():
            if info.get("status") == "active":
                return sid
        return None

    def _handle_spawn_subagent(self, action: SecurityAuditAction, steps_remaining: int) -> SecurityAuditObservation:
        """Register a new sub-agent investigation branch.

        Args (in action.arguments):
            scope:  "host" | "endpoint" | "cred"
            target: the IP / endpoint / credential identifier to investigate
            budget: integer step budget for the sub-agent (default 8, capped 15)

        Validates target is in the dynamic attack_surface (either originally
        scenario-discovered OR revealed by an earlier tool call). Registers
        the sub-agent and adds the target host to discovered_hosts so the
        sub-agent can immediately use scoped tools against it.
        """
        if self._active_subagent_id() is not None:
            return self._obs_with_msg(
                "Cannot spawn — another sub-agent is still active. Call return_to_parent first.",
                steps_remaining, reward=-0.02,
            )
        scope = (action.arguments or {}).get("scope", "host")
        target = (action.arguments or {}).get("target", "")
        budget = int((action.arguments or {}).get("budget", 8) or 8)
        budget = max(2, min(15, budget))  # clamp to a reasonable range

        if scope not in ("host", "endpoint", "cred"):
            return self._obs_with_msg(
                f"Invalid scope '{scope}'. Use one of: host | endpoint | cred.",
                steps_remaining, reward=-0.02,
            )
        if not target:
            return self._obs_with_msg(
                "spawn_subagent requires a 'target' (e.g. 10.0.2.30 for scope=host).",
                steps_remaining, reward=-0.02,
            )
        if scope == "host" and target not in self._attack_surface:
            return self._obs_with_msg(
                f"Target {target} not in current attack_surface. Discover or reveal it first.",
                steps_remaining, reward=-0.02,
            )

        spawn_id = f"sub-{len(self._active_subagents) + 1:02d}-{self._state.step_count}"
        self._active_subagents[spawn_id] = {
            "scope": scope,
            "target": target,
            "budget": budget,
            "steps_used": 0,
            "findings_at_spawn": len(self._submitted_findings),
            "spawn_step": self._state.step_count,
            "parent_step": self._state.step_count,
            "status": "active",
        }

        # If host scope and the target is a revealed-but-not-yet-discovered host,
        # admit it to discovered_hosts now so sub-agent tools can hit it.
        if scope == "host" and target not in self._discovered_hosts and target in self._attack_surface:
            self._discovered_hosts.append(target)
            host_info = self._scenario.get("hosts", {}).get(target, {}) if self._scenario else {}
            if host_info.get("ports"):
                self._discovered_ports[target] = list(host_info.get("ports", []))

        msg = (
            f"Sub-agent {spawn_id} spawned: scope={scope} target={target} budget={budget} steps. "
            f"Subsequent actions are scoped to this branch until you call return_to_parent "
            f"(or budget exhausts)."
        )
        return SecurityAuditObservation(
            tool_output=msg,
            message=msg,
            discovered_hosts=self._discovered_hosts,
            discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings),
            steps_remaining=steps_remaining,
            current_phase=self._current_phase(),
            done=False,
            reward=0.01,  # tiny positive — a valid spawn intent; productivity rewarded on return
        )

    def _handle_return_to_parent(self, action: SecurityAuditAction, steps_remaining: int) -> SecurityAuditObservation:
        """Close the active sub-agent and record its outcome.

        Productivity: a sub-agent is "productive" if it submitted ≥1 finding
        during its run (we only count final-grader matches at episode end —
        for the per-step reward, any finding counts to give a fast signal).

        Reward:
          +0.05 productive
          -0.05 unproductive (penalises spurious branching)
        """
        sid = self._active_subagent_id()
        if not sid:
            return self._obs_with_msg(
                "No active sub-agent to return from. Use spawn_subagent first.",
                steps_remaining, reward=-0.02,
            )
        info = self._active_subagents[sid]
        findings_added = len(self._submitted_findings) - info["findings_at_spawn"]
        productive = findings_added >= 1
        info["status"] = "completed"
        info["findings_added"] = findings_added
        info["productive"] = productive
        info["closed_at_step"] = self._state.step_count
        self._subagent_outcomes.append({
            "spawn_id": sid,
            "scope": info["scope"],
            "target": info["target"],
            "budget": info["budget"],
            "steps_used": info["steps_used"],
            "findings_added": findings_added,
            "productive": productive,
            "spawn_step": info["spawn_step"],
            "closed_at_step": self._state.step_count,
        })
        delegation_reward = 0.05 if productive else -0.05
        msg = (
            f"Sub-agent {sid} closed: {findings_added} findings submitted across "
            f"{info['steps_used']}/{info['budget']} steps. "
            f"{'PRODUCTIVE' if productive else 'unproductive'} (reward {delegation_reward:+.2f})."
        )
        return SecurityAuditObservation(
            tool_output=msg,
            message=msg,
            discovered_hosts=self._discovered_hosts,
            discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings),
            steps_remaining=steps_remaining,
            current_phase=self._current_phase(),
            done=False,
            reward=delegation_reward,
        )

    def _obs_with_msg(self, msg: str, steps_remaining: int, reward: float = 0.0) -> SecurityAuditObservation:
        return SecurityAuditObservation(
            tool_output=msg,
            message=msg,
            discovered_hosts=self._discovered_hosts,
            discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings),
            steps_remaining=steps_remaining,
            current_phase=self._current_phase(),
            done=False,
            reward=reward,
        )

    @property
    def state(self) -> SecurityAuditState:
        self._state.discovered_hosts = list(self._discovered_hosts)
        self._state.discovered_ports = dict(self._discovered_ports)
        self._state.discovered_services = dict(self._discovered_services)
        self._state.submitted_findings = list(self._submitted_findings)
        self._state.total_reward = self._episode_reward
        return self._state

    def _current_phase(self) -> str:
        """Determine current audit phase from agent progress."""
        if len(self._submitted_findings) > 0:
            return "exploitation"
        if len(self._discovered_hosts) > 0:
            return "enumeration"
        return "reconnaissance"

    # --- Action Handlers ---

    def _handle_list_tools(self, steps_remaining):
        tools_text = "Available security audit tools:\n\n"
        for tool in TOOL_DEFINITIONS:
            params = ", ".join(f"{k}: {v}" for k, v in tool["parameters"].items())
            tools_text += f"  {tool['name']}\n"
            tools_text += f"    Description: {tool['description']}\n"
            tools_text += f"    Parameters: {params}\n\n"
        return SecurityAuditObservation(
            tool_output=tools_text, available_tools=TOOL_DEFINITIONS,
            message="Use 'use_tool' action with tool_name and arguments to run a tool.",
            discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings), steps_remaining=steps_remaining,
            current_phase=self._current_phase(), done=False, reward=0.0,
        )

    def _handle_use_tool(self, action, steps_remaining):
        if not action.tool_name:
            return SecurityAuditObservation(
                tool_output="Error: tool_name is required for use_tool action.",
                message="Specify which tool to use.",
                discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
                findings_submitted=len(self._submitted_findings), steps_remaining=steps_remaining,
                current_phase=self._current_phase(), done=False, reward=-0.02,
            )

        target = action.arguments.get("host", action.arguments.get("target", ""))
        honeypots = self._scenario.get("honeypots", [])
        honeypot_penalty = -0.10 if target in honeypots else 0.0

        # Detect redundant tool calls
        current_call = (action.tool_name, tuple(sorted(action.arguments.items())))
        redundancy_penalty = -0.01 if current_call == self._last_tool_call else 0.0
        self._last_tool_call = current_call

        output, new_hosts, new_ports, tool_reward, revealed = execute_tool(
            action.tool_name, action.arguments, self._scenario,
            self._discovered_hosts, self._discovered_ports, self._discovered_vulns,
        )

        # Phase 1: any new revelations expand the dynamic attack_surface so
        # later spawn_subagent actions can validate their target.
        for r in revealed:
            tgt = r.get("target")
            if tgt and tgt not in self._attack_surface:
                self._attack_surface.add(tgt)
                self._revealed_targets.append({**r, "revealed_at_step": self._state.step_count})

        # Difficulty multiplier on positive rewards
        difficulty = self._scenario.get("id", "easy")
        multiplier = self._DIFFICULTY_REWARD_MULTIPLIER.get(difficulty, 1.0)
        if tool_reward > 0:
            tool_reward *= multiplier

        for h in new_hosts:
            if h not in self._discovered_hosts:
                self._discovered_hosts.append(h)
        for h, ports in new_ports.items():
            if h not in self._discovered_ports:
                self._discovered_ports[h] = []
            for p in ports:
                if p not in self._discovered_ports[h]:
                    self._discovered_ports[h].append(p)
        for h in self._discovered_hosts:
            host_ports = self._scenario.get("ports", {}).get(h, [])
            known_ports = self._discovered_ports.get(h, [])
            services = [f"{p['service']}/{p['port']}" for p in host_ports if p["port"] in known_ports]
            if services:
                self._discovered_services[h] = services

        reward = tool_reward + honeypot_penalty + redundancy_penalty
        self._episode_reward += reward

        message = ""
        if honeypot_penalty < 0:
            message = "WARNING: Activity detected on a monitoring system. This may be a honeypot."
        if redundancy_penalty < 0:
            message += " Note: Repeated identical tool call — consider a different action."

        return SecurityAuditObservation(
            tool_output=output, message=message.strip(),
            discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings), steps_remaining=steps_remaining,
            current_phase=self._current_phase(), done=False, reward=reward,
        )

    def _handle_submit_finding(self, action, steps_remaining):
        finding = action.arguments
        required = ["title", "host", "severity"]
        missing = [k for k in required if k not in finding]
        if missing:
            return SecurityAuditObservation(
                tool_output=f"Error: Missing required fields: {', '.join(missing)}",
                message="Finding must include at least: title, host, severity. "
                        "Recommended: cvss_score, cwe, owasp, endpoint, evidence, remediation.",
                discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
                findings_submitted=len(self._submitted_findings), steps_remaining=steps_remaining,
                current_phase=self._current_phase(), done=False, reward=-0.02,
            )

        # Tag finding with current sub-agent context (if any) so the grader's
        # Delegation Score can credit sub-agent productivity correctly.
        active_sid = self._active_subagent_id()
        if active_sid:
            finding = {**finding, "_spawn_id": active_sid, "_parent_step": self._state.step_count}
        self._submitted_findings.append(finding)

        # Match using same logic as grader for consistency
        gt_vulns = self._scenario.get("vulnerabilities", [])
        matched_id = match_single_finding(finding, gt_vulns, self._discovered_vulns)

        difficulty = self._scenario.get("id", "easy")
        multiplier = self._DIFFICULTY_REWARD_MULTIPLIER.get(difficulty, 1.0)

        if matched_id:
            reward = 0.12 * multiplier
            self._discovered_vulns.add(matched_id)
        else:
            # Diminishing reward for unmatched findings to prevent spam
            unmatched = len(self._submitted_findings) - len(self._discovered_vulns)
            if unmatched <= 2:
                reward = 0.02
            elif unmatched <= 4:
                reward = 0.01
            else:
                reward = 0.0

        self._episode_reward += reward
        return SecurityAuditObservation(
            tool_output=f"Finding #{len(self._submitted_findings)} recorded: {finding.get('title', 'Untitled')}",
            message=f"Finding submitted. Total findings: {len(self._submitted_findings)}.",
            discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings), steps_remaining=steps_remaining,
            current_phase=self._current_phase(), done=False, reward=reward,
        )

    def _finish_episode(self, message, truncated=False):
        """End the audit and compute final grade."""
        grades = grade_episode(
            self._scenario, self._submitted_findings,
            self._discovered_hosts, self._discovered_ports,
            steps_used=self._state.step_count,
            subagent_outcomes=self._subagent_outcomes,
        )
        final_score = grades["final_score"]
        self._episode_reward += final_score

        report_lines = [
            "=" * 60, "SECURITY AUDIT REPORT", "=" * 60,
            f"Scenario: {self._scenario['name']}",
            f"Company: {self._scenario['company']}",
            f"Compliance Framework: {self._scenario['compliance_context']}",
            "",
            "RESULTS:",
            f"  Final Score: {final_score:.2f} / 1.00",
            f"  Detection Rate: {grades['detection_rate']:.2f} ({grades['true_positives']}/{grades['total_vulnerabilities']} vulnerabilities found)",
            f"  Coverage: {grades['coverage']:.2f} ({grades['hosts_examined']}/{grades['total_hosts']} hosts examined)",
            f"  Severity Accuracy: {grades['severity_accuracy']:.2f}",
            f"  Classification: CWE {grades['cwe_accuracy']:.2f} | OWASP {grades['owasp_accuracy']:.2f} | Combined {grades['classification_accuracy']:.2f}",
            f"  Report Quality: {grades['report_quality']:.2f} (fields: {grades['field_completeness']:.2f}, narrative: {grades['narrative_quality']:.2f})",
            f"  Pivoting Score: {grades['pivoting_score']:.2f}",
            f"  Exploitation Proof: {grades['exploitation_proof']:.2f}",
            f"  False Positives: {grades['false_positives']} (penalty: -{grades['fp_penalty']:.2f})",
            f"  Honeypot Penalty: -{grades['honeypot_penalty']:.2f}",
            "",
            "COMPLIANCE:",
            f"  Framework: {grades['compliance_framework']}",
            f"  Controls Covered: {grades['compliance_controls_covered']}/{grades['compliance_controls_expected']}",
            f"  Compliance Coverage: {grades['compliance_coverage']:.2f}",
            "",
            f"Steps Used: {self._state.step_count} / {self._scenario['max_steps']} (efficiency: {grades['efficiency']:.2f})",
            f"Findings Submitted: {len(self._submitted_findings)}",
            "=" * 60,
        ]

        return SecurityAuditObservation(
            tool_output="\n".join(report_lines), message=message,
            discovered_hosts=self._discovered_hosts, discovered_services=self._discovered_services,
            findings_submitted=len(self._submitted_findings), steps_remaining=0,
            done=True, truncated=truncated, current_phase="reporting",
            reward=final_score, metadata={"grades": grades},
        )
