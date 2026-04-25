"""
Security Audit Environment — Baseline Inference Script
=======================================================
MANDATORY for hackathon submission.

Uses OpenAI Client to run an LLM agent against the security audit
environment. Reads API credentials from environment variables.

ENV VARS (required):
    API_BASE_URL  — The API endpoint for the LLM
    MODEL_NAME    — The model identifier to use
    OPENROUTER_API_KEY (or HF_TOKEN / OPENAI_API_KEY) — API key passed to the client

Optional:
    INFERENCE_LOG_LLM — If set, append each raw model response to this file path
    INFERENCE_LOG_API — If set, append API errors and fallback-to-list_tools events
    INFERENCE_INTERACTIVE — 1 / true: wait for Enter between steps (see --interactive)
    INFERENCE_PAUSE — step (default) | scenario: what "interactive" pauses between
    INFERENCE_SUMMARY_FILE — If set, append a short grader + stats block per scenario
"""

import argparse
import os
import sys
import textwrap
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# --- ENV VARS ---
# Defaults favour OpenRouter + a small Llama; override with env or .env.
API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
# Accept any of the common token-env-var names. Whichever is set first wins.
API_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or os.getenv("HF_TOKEN")
    or os.getenv("OPENAI_API_KEY")
)

if API_KEY is None:
    raise ValueError(
        "Set OPENROUTER_API_KEY (or HF_TOKEN / OPENAI_API_KEY) in your env or .env"
    )

# --- CONFIG ---
SCENARIO_MAX_STEPS = {"easy": 25, "medium": 35, "hard": 45}
TEMPERATURE = float(os.getenv("INFERENCE_TEMPERATURE", "0.5"))
MAX_TOKENS = 1024
SCENARIOS = ["easy", "medium", "hard"]
ENV_NAME = "security_audit_env"

# --- SYSTEM PROMPT ---
# Kept short and example-driven so small open models (Llama 3.2 3B, Qwen 1.5B)
# can follow it. You're scored on findings submitted, not tools run.
SYSTEM_PROMPT = textwrap.dedent("""\
You are a security auditor. Reply with ONE JSON object only — no prose, no code fences.

Five action shapes:
  USE TOOL:   {"action_type":"use_tool","tool_name":"<tool>","arguments":{...}}
  SUBMIT:     {"action_type":"submit_finding","arguments":{"title":"...","host":"<ip>","type":"<vuln>","severity":"Critical|High|Medium|Low","cvss_score":<0-10>,"cwe":"CWE-XX","owasp":"AXX:2021 - ...","endpoint":"<path>","evidence":"<why>","remediation":"<fix>"}}
  SPAWN:      {"action_type":"spawn_subagent","arguments":{"scope":"host","target":"10.0.2.30","budget":6}}
  RETURN:     {"action_type":"return_to_parent","arguments":{}}
  REPORT:     {"action_type":"generate_report"}

Tools (most-used): network_scan(target), web_crawl(host), test_injection(host,endpoint),
test_xss(host,endpoint), test_auth(host), test_config(host), test_crypto(host),
check_secrets(host,endpoint), vulnerability_scan(host), service_fingerprint(host).

Rough flow: scan once → crawl each host once → test endpoints → submit a finding for
EVERY anomaly, error, or labeled issue you see in tool output → generate_report.

DELEGATION (the multi-agent move). Tool output sometimes ends with a
"[REVEALED] Sub-agent delegation candidates: ..." block. Those are *new*
attack-surface targets uncovered by the current finding (e.g. an SSRF reveals
internal hosts you couldn't see before). Two ways to handle them:
  1. Continue the main thread and ignore them (safer if the main scope still has
     clear leads).
  2. Spawn a sub-agent: {"action_type":"spawn_subagent","arguments":{"scope":"host","target":"<ip>","budget":6}}
     The next steps will be scoped to that branch; recon/test/submit findings
     on the new target. When you've squeezed it (or it's clearly empty), call
     {"action_type":"return_to_parent","arguments":{}} and the parent thread
     resumes. Productive sub-agents (≥1 finding) earn +0.05; unproductive ones
     cost -0.05, so only spawn when you have a real lead.

Examples (output format — copy this style):

Tool output: "[CRITICAL] SQL Injection DETECTED at /api/login (param=username), CWE-89, CVSS 9.8"
Your reply: {"action_type":"submit_finding","arguments":{"title":"SQL Injection in /api/login","host":"10.0.1.10","type":"SQL Injection","severity":"Critical","cvss_score":9.8,"cwe":"CWE-89","owasp":"A03:2021 - Injection","endpoint":"/api/login","evidence":"Tool flagged param=username vulnerable","remediation":"Use parameterized queries"}}

Tool output: "Anomalous response — server fetched internal URL via image_url parameter (HTTP 200, body: AWS metadata)"
Your reply: {"action_type":"submit_finding","arguments":{"title":"SSRF via image_url","host":"10.0.2.20","type":"SSRF","severity":"High","cvss_score":8.6,"cwe":"CWE-918","owasp":"A10:2021 - SSRF","endpoint":"/api/upload","evidence":"image_url parameter fetched internal AWS metadata","remediation":"Validate and allow-list URL hosts"}}

Tool output: "Discovered host 10.0.1.10 (web), 10.0.1.20 (db)"
Your reply: {"action_type":"use_tool","tool_name":"web_crawl","arguments":{"host":"10.0.1.10"}}

Rules:
- Each scenario has a SMALL FIXED number of real vulnerabilities (~3 on easy, ~6 on medium, ~10 on hard). Do NOT exceed that — every extra finding is an escalating false-positive penalty (-0.03, -0.04, ... up to -0.08 each) that wipes out true positives.
- ONE finding per unique (host, vulnerability_type) pair. Do NOT submit duplicates or near-duplicates.
- The moment you have NO new evidence to act on, call generate_report. Do NOT keep submitting findings to fill steps.
- Do NOT repeat list_tools or network_scan once you've called them.
- If you're uncertain about CVSS/CWE, make a reasonable guess from the evidence — submitting one well-grounded finding is better than not, but inventing findings is worse than submitting nothing.
""").strip()


def _append_llm_log(path: str, scenario_id: str, step: int, text: str) -> None:
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n=== {scenario_id} step={step} ===\n{text}\n")
    except OSError:
        pass


def _append_api_log(path: str, scenario_id: str, step: int, text: str) -> None:
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n=== {scenario_id} step={step} API ===\n{text.rstrip()}\n")
    except OSError:
        pass


def _append_summary_file(path: str, text: str) -> None:
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text)
            if not text.endswith("\n"):
                f.write("\n")
    except OSError:
        pass


def _format_grader_block(scenario_id: str, grades: Dict[str, Any], episode_step_reward_sum: float) -> str:
    """Human-readable grader output (where your final 'reward' / score comes from)."""
    lines = [
        "",
        f"{'='*60}",
        f"  REWARD / GRADER BREAKDOWN  —  scenario: {scenario_id}",
        f"{'='*60}",
        f"  final_score (0–1, main benchmark):  {grades.get('final_score', 0.0):.4f}",
        f"  sum of per-step rewards (episode):  {episode_step_reward_sum:.4f}",
        f"  true positives / total vulns:     {grades.get('true_positives', 0)}/{grades.get('total_vulnerabilities', 0)}  (detection_rate={grades.get('detection_rate', 0.0):.2f})",
        f"  hosts examined / total hosts:        {grades.get('hosts_examined', 0)}/{grades.get('total_hosts', 0)}  (coverage={grades.get('coverage', 0.0):.2f})",
        f"  false positives (penalty):         {grades.get('false_positives', 0)}  (fp_penalty -{grades.get('fp_penalty', 0.0):.2f})",
        f"  severity / classification:         {grades.get('severity_accuracy', 0.0):.2f} / {grades.get('classification_accuracy', 0.0):.2f}",
        f"  report quality:                    {grades.get('report_quality', 0.0):.2f}",
        f"{'='*60}",
    ]
    return "\n".join(lines) + "\n"


def _format_zero_score_hint(
    n_list_tools: int,
    n_api_errors: int,
    total_steps: int,
) -> str:
    parts = [
        "  HINT: final_score is 0 when no findings match the scenario, or coverage is near zero.",
    ]
    if n_list_tools >= max(1, total_steps - 1) and total_steps > 0:
        parts.append(
            "  → Most steps were 'list_tools' (no discovery). Use use_tool (network_scan, web_crawl) then submit_finding."
        )
    if n_api_errors > 0:
        parts.append(
            f"  → {n_api_errors} LLM API call(s) failed (see INFERENCE_LOG_API or stderr); responses may be fallbacks, not the model."
        )
    return "\n".join(parts) + "\n"


def _env_bool(name: str) -> bool:
    return os.getenv(name, "").lower() in ("1", "true", "yes", "on")


def _wait_interactive(
    message: str,
) -> str:
    """Block until the user accepts the next action. Returns a short status for logging."""
    if not sys.stdin.isatty():
        return "skipped (no tty)"
    try:
        return input(message).strip().lower() or "ok"
    except EOFError:
        return "eof"


def _config_interactive() -> Tuple[bool, str]:
    """(interactive, pause) where pause is 'step' or 'scenario'."""
    pause = os.getenv("INFERENCE_PAUSE", "step").lower().strip()
    if pause not in ("step", "scenario"):
        pause = "step"
    return _env_bool("INFERENCE_INTERACTIVE"), pause


def build_prompt(step: int, observation: Any, history: List[str], max_steps: int = 30) -> str:
    """Build user prompt from current observation and history."""
    parts = [f"[Step {step}/{max_steps}]"]

    if hasattr(observation, "tool_output") and observation.tool_output:
        output = observation.tool_output
        if len(output) > 2000:
            output = output[:2000] + "\n... (truncated)"
        parts.append(f"\nTool Output:\n{output}")

    if hasattr(observation, "message") and observation.message:
        parts.append(f"\nMessage: {observation.message}")

    hosts = []
    if hasattr(observation, "discovered_hosts") and observation.discovered_hosts:
        hosts = observation.discovered_hosts
        parts.append(f"\nDiscovered Hosts: {', '.join(hosts)}")

    findings = 0
    if hasattr(observation, "findings_submitted"):
        findings = observation.findings_submitted
        parts.append(f"Findings Submitted: {findings}")

    if hasattr(observation, "steps_remaining"):
        parts.append(f"Steps Remaining: {observation.steps_remaining}")

    if history:
        parts.append(f"\nRecent Actions:\n" + "\n".join(history[-8:]))

    has_scanned = any("network_scan" in h for h in history)
    has_crawled = any("web_crawl" in h for h in history)
    has_tested = any(t in " ".join(history) for t in ["test_injection", "test_xss", "test_auth", "test_config"])

    if not has_scanned:
        parts.append("\n>> Phase 1: Run network_scan on the target CIDR now.")
    elif not has_crawled and hosts:
        parts.append(f"\n>> Phase 2: Run web_crawl on each host: {', '.join(hosts)}")
    elif has_crawled and not has_tested:
        parts.append("\n>> Phase 3: Test endpoints with test_injection, test_xss, test_auth, test_config, test_crypto, check_secrets, vulnerability_scan.")
    elif has_tested and findings == 0:
        parts.append("\n>> Phase 4: You MUST submit_finding for any anomalies detected. Review tool output and submit findings NOW.")
    elif step >= max_steps - 2:
        parts.append("\n>> Phase 5: Time is almost up. Run generate_report NOW.")

    parts.append("\nRespond with a single JSON action.")
    return "\n".join(parts)


def run_scenario(
    client: OpenAI,
    scenario_id: str,
    env_url: str,
    *,
    interactive: bool = False,
    pause: str = "step",
) -> float:
    """Run the agent on one scenario and return the final score.

    If ``interactive`` and ``pause == "step"``, wait for Enter after each step
    (before the next LLM call) to space out API traffic and avoid rate limits.
    If ``pause == "scenario"``, only :func:`main` pauses between scenarios.
    """
    from security_audit_env import (
        SecurityAuditAction,
        SecurityAuditEnv,
        parse_llm_action_text,
    )

    max_steps = SCENARIO_MAX_STEPS.get(scenario_id, 30)
    api_log = os.getenv("INFERENCE_LOG_API")

    print(f"\n{'='*60}")
    print(f"Running scenario: {scenario_id} (max {max_steps} steps)")
    print(f"{'='*60}")

    # --- MANDATORY STDOUT: [START] ---
    print(f"[START] task={scenario_id} env={ENV_NAME} model={MODEL_NAME}", flush=True)

    all_rewards: List[float] = []
    final_score = 0.0
    total_steps = 0
    success = False
    last_error = None
    user_quit_scenario = False
    last_grades: Optional[Dict[str, Any]] = None
    n_list_tools = 0
    n_api_errors = 0
    summary_path = os.getenv("INFERENCE_SUMMARY_FILE")

    try:
        with SecurityAuditEnv(base_url=env_url).sync() as env:
            if interactive and pause == "step" and sys.stdin.isatty():
                u = _wait_interactive(
                    f"\n>>> Starting '{scenario_id}'. Press Enter to run the first step (LLM call), or 'q' + Enter to skip this scenario.\n> "
                )
                if u == "q":
                    return 0.0

            result = env.reset(scenario_id=scenario_id)
            observation = result.observation
            history: List[str] = []

            def _do_force_report() -> None:
                nonlocal result, all_rewards, total_steps, final_score, success, last_error, observation, last_grades
                try:
                    act = SecurityAuditAction(action_type="generate_report")
                    result = env.step(act)
                    reward = result.reward or 0.0
                    all_rewards.append(reward)
                    total_steps = total_steps + 1
                    _ts = total_steps
                    _cum = sum(all_rewards)
                    print(
                        f"[STEP]  step={_ts} action=generate_report reward={reward:.2f} "
                        f"cum={_cum:.2f} done={str(result.done).lower()} error=null",
                        flush=True,
                    )
                    observation = result.observation
                    grades = getattr(observation, "metadata", {}) or {}
                    grades = grades.get("grades", {})
                    last_grades = grades if isinstance(grades, dict) and grades else None
                    final_score = grades.get("final_score", reward) if last_grades else (reward or 0.0)
                    success = final_score > 0
                except Exception as exc:
                    final_score = 0.0
                    last_error = str(exc)

            for step in range(1, max_steps + 1):
                if result.done:
                    break

                prompt = build_prompt(step, observation, history, max_steps=max_steps)
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]

                last_error = None
                try:
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        stream=False,
                    )
                    response_text = completion.choices[0].message.content or ""
                except Exception as exc:
                    n_api_errors += 1
                    last_error = str(exc)
                    response_text = '{"action_type": "list_tools"}'
                    err_line = f"[API error — using fallback list_tools] {type(exc).__name__}: {exc}"
                    if api_log:
                        _append_api_log(api_log, scenario_id, step, err_line)
                    else:
                        print(f"  {err_line}", flush=True)

                log_path = os.getenv("INFERENCE_LOG_LLM")
                if log_path and response_text:
                    _append_llm_log(log_path, scenario_id, step, response_text)

                llm_action, json_err = parse_llm_action_text(response_text)
                if llm_action is None:
                    last_error = json_err or "Could not parse LLM action JSON"
                    action = SecurityAuditAction(action_type="list_tools")
                else:
                    last_error = None
                    action = llm_action.to_security_audit_action()
                if action.action_type == "list_tools":
                    n_list_tools += 1

                action_str = action.action_type
                if action.tool_name:
                    action_str += f"({action.tool_name})"
                elif action.action_type == "spawn_subagent":
                    _t = (action.arguments or {}).get("target", "?")
                    _s = (action.arguments or {}).get("scope", "?")
                    action_str += f"({_s}:{_t})"

                try:
                    result = env.step(action)
                    observation = result.observation
                    last_error = None
                except Exception as exc:
                    last_error = str(exc)
                    reward = 0.0
                    all_rewards.append(reward)
                    total_steps = step
                    # --- MANDATORY STDOUT: [STEP] ---
                    error_str = last_error.replace("\n", " ") if last_error else "null"
                    _c = sum(all_rewards)
                    print(
                        f"[STEP]  step={step} action={action_str} reward={reward:.2f} "
                        f"cum={_c:.2f} done=false error={error_str}",
                        flush=True,
                    )
                    break

                reward = result.reward or 0.0
                all_rewards.append(reward)
                total_steps = step
                _cum = sum(all_rewards)

                history.append(f"Step {step}: {action_str} → reward {reward:+.2f}")

                # --- MANDATORY STDOUT: [STEP] ---
                done_str = "true" if result.done else "false"
                error_str = last_error.replace("\n", " ") if last_error else "null"
                print(
                    f"[STEP]  step={step} action={action_str} reward={reward:.2f} "
                    f"cum={_cum:.2f} done={done_str} error={error_str}",
                    flush=True,
                )

                if result.done:
                    grades = getattr(observation, "metadata", {}) or {}
                    grades = grades.get("grades", {})
                    last_grades = grades if isinstance(grades, dict) and grades else None
                    # On generate_report, the env's reward IS the grader's final_score
                    # (server/security_audit_env_environment.py:329). Use that as the
                    # source of truth — `metadata` is currently dropped by Pydantic
                    # because SecurityAuditObservation doesn't declare a metadata field.
                    final_score = grades.get("final_score", reward) if last_grades else reward
                    success = final_score > 0
                    break

                if interactive and pause == "step" and sys.stdin.isatty() and not result.done:
                    u2 = _wait_interactive(
                        f"\n>>> {scenario_id} step {step}/{max_steps} done. "
                        "Press Enter for the next LLM call, or 'q' + Enter to end this scenario (a report will be generated).\n> "
                    )
                    if u2 == "q":
                        user_quit_scenario = True
                        break
            else:
                # No break — ran all steps without terminal done: force report
                _do_force_report()
            if user_quit_scenario:
                _do_force_report()
    except Exception as exc:
        last_error = str(exc)
    finally:
        if last_grades is not None:
            _sm = _format_grader_block(scenario_id, last_grades, sum(all_rewards))
            print(_sm, flush=True)
            if summary_path:
                _append_summary_file(summary_path, _sm)
        elif total_steps > 0:
            _mini = (
                f"\n  (No grader report in metadata — score may be unset. "
                f"Steps={total_steps} list_tools_steps≈{n_list_tools} api_errors={n_api_errors})\n"
            )
            print(_mini, flush=True)
            if summary_path:
                _append_summary_file(summary_path, _mini)
        if final_score == 0.0 and (last_grades is not None or total_steps > 0):
            _hint = _format_zero_score_hint(n_list_tools, n_api_errors, total_steps)
            print(_hint, flush=True)
            if summary_path:
                _append_summary_file(summary_path, _hint)
        # --- MANDATORY STDOUT: [END] (always emitted, even on exception) ---
        rewards_str = ",".join(f"{r:.2f}" for r in all_rewards)
        success_str = "true" if success else "false"
        print(f"[END]   success={success_str} steps={total_steps} score={final_score:.2f} rewards={rewards_str}", flush=True)

    return final_score


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the baseline LLM agent on SecurityAuditEnv.",
    )
    p.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Wait for your input between LLM steps (or between scenarios) to space out API calls and reduce rate limits",
    )
    p.add_argument(
        "--pause",
        choices=["step", "scenario"],
        default=None,
        help="With --interactive: 'step' pauses after each environment step; 'scenario' only between easy/medium/hard",
    )
    return p.parse_args()


def main() -> None:
    """Run baseline inference across all scenarios."""
    args = _parse_args()
    env_inter = args.interactive or _env_bool("INFERENCE_INTERACTIVE")
    pause = args.pause or os.getenv("INFERENCE_PAUSE", "step")
    if pause not in ("step", "scenario"):
        pause = "step"

    print("Security Audit Environment — Baseline Inference")
    if env_inter:
        print("Mode: INTERACTIVE (you control the pace; stdin must be a TTY)")
        print(f"  Pause: {pause}  (INFERENCE_PAUSE, or --pause)")
    print(f"API: {API_BASE_URL}")
    print(f"Model: {MODEL_NAME}")

    llm_client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env_url = os.getenv("ENV_URL", "http://localhost:8000")

    scores: Dict[str, float] = {}
    for i, scenario_id in enumerate(SCENARIOS):
        if env_inter and pause == "scenario" and sys.stdin.isatty():
            if i == 0:
                nxt0 = _wait_interactive(
                    f"\n>>> Press Enter to start the first scenario ('{scenario_id}'), or 'q' + Enter to cancel.\n> "
                )
                if nxt0 == "q":
                    print("(Cancelled.)", flush=True)
                    return
            else:
                nxt = _wait_interactive(
                    f"\n>>> Previous scenario(s) finished. Press Enter to start '{scenario_id}', or 'q' + Enter to stop the run.\n> "
                )
                if nxt == "q":
                    print("(Stopping — remaining scenarios skipped.)", flush=True)
                    break
        try:
            score = run_scenario(
                llm_client,
                scenario_id,
                env_url,
                interactive=env_inter,
                pause=pause,
            )
            scores[scenario_id] = score
        except Exception as exc:
            print(f"  ERROR on {scenario_id}: {exc}")
            scores[scenario_id] = 0.0

    print(f"\n{'='*60}")
    print("BASELINE SCORES")
    print(f"{'='*60}")
    for sid in SCENARIOS:
        if sid in scores:
            print(f"  {sid:10s}: {scores[sid]:.4f}")
    rans = [scores[k] for k in SCENARIOS if k in scores]
    avg = sum(rans) / len(rans) if rans else 0.0
    print(f"  {'average':10s}: {avg:.4f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
