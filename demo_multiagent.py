"""
Curated multi-agent demo — deterministic walkthrough of spawn_subagent / return_to_parent.

This is NOT an LLM run. It exercises the env directly with a hand-picked action
sequence so judges (and the README) can see the multi-agent flow working
end-to-end without the variance of model behaviour.

Run:
    PYTHONPATH=. uv run python demo_multiagent.py

What it shows:
  1. Recon on visible hosts (10.0.2.10 web, 10.0.2.20).
  2. SSRF on 10.0.2.10 /api/upload/image — the env emits a [REVEALED] block
     announcing two new internal hosts (10.0.2.30, 10.0.2.40) that became
     reachable via the SSRF.
  3. Main agent submits the SSRF finding, then SPAWNS a sub-agent against
     10.0.2.30 with a 6-step budget.
  4. Sub-agent does its own recon-and-test on 10.0.2.30, submits a finding,
     and returns to parent.
  5. Main agent resumes, optionally spawns another sub-agent for 10.0.2.40,
     then generates the report.
  6. Final grader output shows the Delegation Score component lit up
     (productive_spawns / total_spawns).
"""
from __future__ import annotations

from server.security_audit_env_environment import SecurityAuditEnvironment
from models import SecurityAuditAction


def banner(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def step(env, action: SecurityAuditAction, label: str) -> "SecurityAuditObservation":
    obs = env.step(action)
    sid = env._active_subagent_id() or "main"
    print(f"\n[{sid}] {label}")
    print(f"  reward = {obs.reward:+.2f}    cum = {env._episode_reward:+.2f}    done = {obs.done}")
    if "[REVEALED]" in (obs.tool_output or ""):
        # Trim the output for readability — print the first 6 lines + the [REVEALED] block
        lines = obs.tool_output.split("\n")
        for L in lines[:8]:
            print(f"     {L}")
        rev_idx = next((i for i, L in enumerate(lines) if "[REVEALED]" in L), None)
        if rev_idx is not None and rev_idx >= 8:
            print("     ...")
            for L in lines[rev_idx : rev_idx + 4]:
                print(f"     {L}")
    elif obs.tool_output:
        # Just first line + maybe a couple
        first = obs.tool_output.strip().split("\n", 2)
        for L in first[:2]:
            print(f"     {L}")
    return obs


def main() -> None:
    env = SecurityAuditEnvironment()
    banner("VAPT-Env multi-agent demo — medium scenario, deterministic trace")
    obs = env.reset(scenario_id="medium")
    print(f"Scenario: {env._scenario['id']}  hosts={list(env._scenario.get('hosts', {}).keys())}")
    print(f"Initial attack_surface (visible only): {sorted(env._attack_surface)}")

    banner("Phase 1 — main thread recon")
    step(env, SecurityAuditAction(
        action_type="use_tool", tool_name="network_scan",
        arguments={"target": "10.0.2.0/24"},
    ), "network_scan 10.0.2.0/24")
    step(env, SecurityAuditAction(
        action_type="use_tool", tool_name="web_crawl",
        arguments={"host": "10.0.2.10"},
    ), "web_crawl 10.0.2.10")

    banner("Phase 2 — gateway vuln triggers attack-surface revelation")
    step(env, SecurityAuditAction(
        action_type="use_tool", tool_name="test_injection",
        arguments={"host": "10.0.2.10", "endpoint": "/api/upload/image"},
    ), "test_injection on /api/upload/image  (SSRF gateway)")
    print(f"  attack_surface NOW: {sorted(env._attack_surface)}")
    print(f"  revealed_targets:   {[r['target'] for r in env._revealed_targets]}")

    step(env, SecurityAuditAction(
        action_type="submit_finding",
        arguments={
            "title": "SSRF in /api/upload/image",
            "host": "10.0.2.10",
            "type": "Server-Side Request Forgery (SSRF)",
            "severity": "Critical",
            "cvss_score": 9.1,
            "cwe": "CWE-918",
            "owasp": "A10:2021 - Server-Side Request Forgery",
            "endpoint": "/api/upload/image",
            "evidence": "Server fetched internal URL via image_url parameter; returned AWS metadata",
            "remediation": "Allow-list URL hosts and block internal/private IP ranges",
        },
    ), "submit_finding (SSRF) — main thread")

    banner("Phase 3 — DELEGATE: spawn_subagent on 10.0.2.30 (revealed by SSRF)")
    step(env, SecurityAuditAction(
        action_type="spawn_subagent",
        arguments={"scope": "host", "target": "10.0.2.30", "budget": 6},
    ), "spawn_subagent host=10.0.2.30 budget=6")

    step(env, SecurityAuditAction(
        action_type="use_tool", tool_name="vulnerability_scan",
        arguments={"host": "10.0.2.30"},
    ), "(in sub) vulnerability_scan 10.0.2.30")
    step(env, SecurityAuditAction(
        action_type="use_tool", tool_name="test_auth",
        arguments={"host": "10.0.2.30"},
    ), "(in sub) test_auth 10.0.2.30")
    step(env, SecurityAuditAction(
        action_type="submit_finding",
        arguments={
            "title": "Default credentials on Jenkins admin panel",
            "host": "10.0.2.30",
            "type": "Default Credentials",
            "severity": "High",
            "cvss_score": 8.8,
            "cwe": "CWE-798",
            "owasp": "A07:2021 - Identification and Authentication Failures",
            "endpoint": "/jenkins/login",
            "evidence": "admin:admin accepted; full pipeline access granted",
            "remediation": "Force credential rotation; enforce SSO / MFA on Jenkins admin",
        },
    ), "(in sub) submit_finding default-creds")

    banner("Phase 4 — return_to_parent: sub-agent closes")
    step(env, SecurityAuditAction(
        action_type="return_to_parent", arguments={},
    ), "return_to_parent")
    print(f"  subagent_outcomes: {env._subagent_outcomes}")

    banner("Phase 5 — main thread resumes, generate_report")
    obs = step(env, SecurityAuditAction(
        action_type="generate_report", arguments={},
    ), "generate_report (final grader runs)")

    banner("FINAL — multi-dim grader output")
    if obs.tool_output:
        for L in obs.tool_output.split("\n"):
            print(f"  {L}")
    print()


if __name__ == "__main__":
    main()
