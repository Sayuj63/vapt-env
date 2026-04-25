"""
Build a trajectory dataset from VAPT-Env rollouts and push to HF Hub.

Captures per-step (observation, action, reward, ...) tuples from inference runs
across multiple models and scenarios, formats them as a HuggingFace dataset,
and (optionally) uploads to the Hub. The result is a standalone research
artifact — other teams can use it for offline RL, behaviour cloning, or
trajectory analysis without re-running the env themselves.

Run:
    # capture trajectories from a single model/scenario set
    uv run python build_trajectory_dataset.py \\
        --model meta-llama/llama-3.2-3b-instruct \\
        --scenarios easy medium hard \\
        --episodes 3

    # also push to HF Hub (requires HF_TOKEN env)
    uv run python build_trajectory_dataset.py --push --repo-id Sayuj63/vapt-env-trajectories

Output:
    dataset/trajectories.jsonl  — raw trajectories, one episode per line
    dataset/dataset_info.json   — schema + summary stats
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from security_audit_env import SecurityAuditEnv, SecurityAuditAction
from models import LLMJsonAction, parse_llm_action_text


SCENARIO_MAX_STEPS = {"easy": 25, "medium": 35, "hard": 45}

# Use the SAME system prompt as inference.py — small models need the worked
# examples to emit the right action_type Literal values (otherwise they
# hallucinate "REPORT" or use a tool name as the action_type).
from inference import SYSTEM_PROMPT  # noqa: E402


def render_observation(obs) -> str:
    return "\n".join([
        f"phase={obs.current_phase}",
        f"hosts={obs.discovered_hosts or []}",
        f"services={obs.discovered_services or {}}",
        f"findings_submitted={obs.findings_submitted}",
        f"steps_remaining={obs.steps_remaining}",
        f"tool_output:\n{(obs.tool_output or '')[:1200]}",
    ])


def call_llm(client: OpenAI, model: str, observation_text: str) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": observation_text},
        ],
        max_tokens=512,
        temperature=0.5,
    )
    return resp.choices[0].message.content or ""


def collect_episode(
    env_url: str,
    client: OpenAI,
    model: str,
    scenario_id: str,
    max_steps: int,
) -> Dict[str, Any]:
    """Run one episode end-to-end. Return a serialisable trajectory dict."""
    episode_id = str(uuid.uuid4())
    steps: List[Dict[str, Any]] = []
    cum_reward = 0.0

    with SecurityAuditEnv(base_url=env_url).sync() as env:
        result = env.reset(scenario_id=scenario_id)
        obs = result.observation

        for step in range(max_steps):
            obs_text = render_observation(obs)
            try:
                completion = call_llm(client, model, obs_text)
                llm_action, parse_err = parse_llm_action_text(completion)
                action = (
                    llm_action.to_security_audit_action()
                    if llm_action is not None
                    else SecurityAuditAction(action_type="list_tools")
                )
            except Exception as e:
                completion = f"<api_error: {e!r}>"
                action = SecurityAuditAction(action_type="list_tools")
                parse_err = str(e)

            try:
                rs = env.step(action)
                next_obs = rs.observation
                step_reward = float(rs.reward or 0.0)
                done = bool(rs.done)
            except Exception as e:
                next_obs = obs
                step_reward = 0.0
                done = True
                parse_err = (parse_err or "") + f" | step_error: {e!r}"

            cum_reward += step_reward

            steps.append({
                "step": step,
                "observation_text": obs_text,
                "completion_raw": completion,
                "action_type": action.action_type,
                "tool_name": action.tool_name,
                "arguments": action.arguments,
                "reward": step_reward,
                "cumulative_reward": cum_reward,
                "done": done,
                "discovered_hosts": list(next_obs.discovered_hosts or []),
                "findings_submitted": int(next_obs.findings_submitted or 0),
                "current_phase": next_obs.current_phase,
                "parse_error": parse_err,
            })

            obs = next_obs
            if done:
                break

    final_score = steps[-1]["reward"] if steps and steps[-1]["action_type"] == "generate_report" else 0.0
    return {
        "episode_id": episode_id,
        "scenario_id": scenario_id,
        "model": model,
        "max_steps": max_steps,
        "n_steps": len(steps),
        "cumulative_reward": cum_reward,
        "final_score": final_score,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "env_url": env_url,
        "steps": steps,
    }


def build_dataset(
    env_url: str,
    api_base_url: str,
    api_key: str,
    model: str,
    scenarios: List[str],
    episodes: int,
    out_dir: Path,
) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = out_dir / "trajectories.jsonl"

    client = OpenAI(base_url=api_base_url, api_key=api_key)

    n_total = 0
    final_scores: Dict[str, List[float]] = {s: [] for s in scenarios}

    with jsonl_path.open("a", encoding="utf-8") as f:
        for scenario_id in scenarios:
            max_steps = SCENARIO_MAX_STEPS.get(scenario_id, 30)
            for ep in range(episodes):
                print(f"  collecting [{model}] scenario={scenario_id} episode={ep+1}/{episodes}", flush=True)
                traj = collect_episode(env_url, client, model, scenario_id, max_steps)
                f.write(json.dumps(traj) + "\n")
                n_total += 1
                final_scores[scenario_id].append(traj["final_score"])

    summary = {
        "model": model,
        "env_url": env_url,
        "n_trajectories": n_total,
        "scenarios": scenarios,
        "mean_final_score": {
            s: (sum(final_scores[s]) / len(final_scores[s])) if final_scores[s] else 0.0
            for s in scenarios
        },
        "schema": [
            "episode_id", "scenario_id", "model", "max_steps", "n_steps",
            "cumulative_reward", "final_score", "captured_at", "env_url",
            "steps[*].step", "steps[*].observation_text", "steps[*].completion_raw",
            "steps[*].action_type", "steps[*].tool_name", "steps[*].arguments",
            "steps[*].reward", "steps[*].cumulative_reward", "steps[*].done",
            "steps[*].discovered_hosts", "steps[*].findings_submitted",
            "steps[*].current_phase", "steps[*].parse_error",
        ],
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "dataset_info.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def push_to_hf_hub(
    out_dir: Path,
    repo_id: str,
    private: bool = False,
) -> str:
    """Upload the dataset directory to a HF Hub dataset repo."""
    from huggingface_hub import HfApi, login

    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN env var required to push to Hub")
    login(token=token)

    # Write a dataset card if missing
    card_path = out_dir / "README.md"
    if not card_path.exists():
        info = json.loads((out_dir / "dataset_info.json").read_text())
        card_path.write_text(textwrap.dedent(f"""\
        ---
        license: mit
        task_categories:
          - reinforcement-learning
          - text-generation
        language:
          - en
        tags:
          - openenv
          - vapt
          - security
          - long-horizon
          - multi-agent
        size_categories:
          - n<1K
        ---

        # VAPT-Env Trajectories

        Per-step trajectory data captured from rollouts of LLM agents against the
        live [VAPT-Env](https://huggingface.co/spaces/Sayuj63/Vapt-env) on Hugging
        Face Spaces. Each row is one full episode (reset → ... → generate_report).

        Useful for **offline RL**, **behaviour cloning**, and **trajectory analysis**
        without spinning up the live env yourself.

        ## Source

        Generated with `build_trajectory_dataset.py` from
        https://github.com/Sayuj63/vapt-env

        ## Models captured

        - `{info["model"]}`

        ## Scenarios

        {", ".join(info["scenarios"])}

        ## Mean final score per scenario

        ```json
        {json.dumps(info["mean_final_score"], indent=2)}
        ```

        ## Schema (one episode per JSONL line)

        ```
        {chr(10).join("  - " + s for s in info["schema"])}
        ```
        """), encoding="utf-8")

    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=private, exist_ok=True)
    api.upload_folder(
        folder_path=str(out_dir),
        repo_id=repo_id,
        repo_type="dataset",
        commit_message=f"trajectories: {datetime.now(timezone.utc).isoformat()}",
    )
    url = f"https://huggingface.co/datasets/{repo_id}"
    print(f"OK uploaded → {url}")
    return url


def main() -> None:
    p = argparse.ArgumentParser(description="Capture trajectories from VAPT-Env rollouts.")
    p.add_argument("--model", default="meta-llama/llama-3.2-3b-instruct",
                   help="OpenRouter / OpenAI-compatible model id (default: Llama 3.2 3B)")
    p.add_argument("--scenarios", nargs="+", default=["easy", "medium", "hard"])
    p.add_argument("--episodes", type=int, default=3,
                   help="Episodes per scenario (default: 3)")
    p.add_argument("--out-dir", type=Path, default=Path("dataset"))
    p.add_argument("--api-base-url",
                   default=os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1"))
    p.add_argument("--env-url",
                   default=os.getenv("ENV_URL", "https://Sayuj63-Vapt-env.hf.space"))
    p.add_argument("--push", action="store_true",
                   help="Push the captured dataset to HF Hub")
    p.add_argument("--repo-id", default="Sayuj63/vapt-env-trajectories",
                   help="HF Hub dataset repo id (used with --push)")
    args = p.parse_args()

    api_key = (
        os.getenv("OPENROUTER_API_KEY")
        or os.getenv("HF_TOKEN")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        sys.exit("Set OPENROUTER_API_KEY / HF_TOKEN / OPENAI_API_KEY in env or .env")

    print(f"Capturing trajectories")
    print(f"  model      = {args.model}")
    print(f"  scenarios  = {args.scenarios}")
    print(f"  episodes   = {args.episodes}")
    print(f"  env_url    = {args.env_url}")
    print(f"  out_dir    = {args.out_dir}")
    print()

    summary = build_dataset(
        env_url=args.env_url,
        api_base_url=args.api_base_url,
        api_key=api_key,
        model=args.model,
        scenarios=args.scenarios,
        episodes=args.episodes,
        out_dir=args.out_dir,
    )

    print()
    print("=" * 60)
    print(f"OK captured {summary['n_trajectories']} trajectories")
    print(f"  out_dir      = {args.out_dir}")
    print(f"  jsonl        = {args.out_dir / 'trajectories.jsonl'}")
    print(f"  mean scores  = {json.dumps(summary['mean_final_score'], indent=2)}")

    if args.push:
        print()
        url = push_to_hf_hub(args.out_dir, args.repo_id)
        print(f"  hub url      = {url}")


if __name__ == "__main__":
    main()
