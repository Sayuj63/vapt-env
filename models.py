# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Security Audit Environment.

Simulates real-world VAPT (Vulnerability Assessment & Penetration Testing)
engagements where an AI agent audits infrastructure for security compliance.
"""

import json
import re
from typing import Any, Dict, List, Literal, Optional, Tuple

from openenv.core.env_server.types import Action, Observation, State
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SecurityAuditAction(Action):
    """Action for the Security Audit environment.

    The agent interacts via tool calls — discover hosts, scan services,
    test for vulnerabilities, submit findings, and generate reports.
    """

    action_type: Literal[
        "list_tools",
        "use_tool",
        "submit_finding",
        "generate_report",
    ] = Field(..., description="Type of action to take")

    tool_name: Optional[str] = Field(
        default=None,
        description="Tool to invoke (required when action_type='use_tool')",
    )

    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tool-specific arguments",
    )


class LLMJsonAction(BaseModel):
    """Wire JSON for one model turn, validated before ``SecurityAuditAction``.

    Unknown top-level keys are ignored so minor format drift does not fail parsing.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    action_type: Literal["list_tools", "use_tool", "submit_finding", "generate_report"] = Field(
        ...,
        description="Which environment action to take",
    )
    tool_name: Optional[str] = Field(
        default=None,
        description="Tool name when action_type is use_tool",
    )
    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments for use_tool or fields for submit_finding",
    )

    def to_security_audit_action(self) -> SecurityAuditAction:
        return SecurityAuditAction(
            action_type=self.action_type,
            tool_name=self.tool_name,
            arguments=self.arguments,
        )


def extract_json_object_from_text(raw: str) -> Optional[Dict[str, Any]]:
    """Return the first JSON object from model text, or None."""
    if not (raw and raw.strip()):
        return None

    text = raw.strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    try:
        val = json.loads(text)
    except json.JSONDecodeError:
        val = None

    if isinstance(val, dict):
        return val

    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL)
    if match:
        try:
            v2 = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
        if isinstance(v2, dict):
            return v2

    return None


def parse_llm_action_text(raw: str) -> Tuple[Optional[LLMJsonAction], Optional[str]]:
    """Parse and validate one action from a chat message.

    Returns (model, None) on success, or (None, error_message) on failure.
    """
    data = extract_json_object_from_text(raw)
    if data is None:
        return None, "Could not extract a JSON object from model response"
    try:
        return LLMJsonAction.model_validate(data), None
    except ValidationError as exc:
        return None, str(exc)


class SecurityAuditObservation(Observation):
    """Observation returned after each step.

    Contains tool output, current discovery state, and audit progress.
    """

    tool_output: str = Field(
        default="",
        description="Text output from the executed tool",
    )

    available_tools: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of available tools (populated by list_tools action)",
    )

    discovered_hosts: List[str] = Field(
        default_factory=list,
        description="Hosts discovered so far",
    )

    discovered_services: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Services discovered per host (host → [service descriptions])",
    )

    findings_submitted: int = Field(
        default=0,
        description="Number of findings submitted so far",
    )

    steps_remaining: int = Field(
        default=0,
        description="Steps remaining before episode ends",
    )

    message: str = Field(
        default="",
        description="Human-readable status message",
    )

    truncated: bool = Field(
        default=False,
        description="True if episode ended due to step limit (truncation), "
                    "False if agent called generate_report (termination). "
                    "Important for RL value function estimation.",
    )

    current_phase: str = Field(
        default="reconnaissance",
        description="Current audit phase: reconnaissance, enumeration, exploitation, or reporting",
    )


class SecurityAuditState(State):
    """Full episode state for the security audit.

    Extends base State (episode_id, step_count) with audit-specific tracking.
    """

    scenario_id: str = Field(default="", description="Current scenario identifier")
    scenario_name: str = Field(default="", description="Human-readable scenario name")
    target_network: str = Field(default="", description="Target network CIDR")
    max_steps: int = Field(default=50, description="Maximum steps allowed")
    discovered_hosts: List[str] = Field(default_factory=list)
    discovered_ports: Dict[str, List[int]] = Field(default_factory=dict)
    discovered_services: Dict[str, List[str]] = Field(default_factory=dict)
    submitted_findings: List[Dict[str, Any]] = Field(default_factory=list)
    total_reward: float = Field(default=0.0)
