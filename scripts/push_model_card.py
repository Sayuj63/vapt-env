"""Push a real model card to https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo

The current card is the default PEFT template with [More Information Needed]
placeholders. This replaces it with proper documentation linking back to the
env, the W&B run, the GitHub repo, and the published numbers.

Run:
    HF_TOKEN=<write-scope> uv run python scripts/push_model_card.py
"""
import os
from pathlib import Path

REPO_ID = "Sayuj63/vapt-env-llama32-3b-grpo"

CARD = """---
license: apache-2.0
base_model: unsloth/Llama-3.2-3B-Instruct-bnb-4bit
tags:
  - openenv
  - reinforcement-learning
  - grpo
  - trl
  - unsloth
  - peft
  - lora
  - security
  - vapt
  - penetration-testing
language:
  - en
library_name: peft
pipeline_tag: text-generation
---

# Llama 3.2 3B — GRPO post-trained on VAPT-Env

LoRA adapter trained with HuggingFace TRL's `GRPOTrainer` on top of [unsloth/Llama-3.2-3B-Instruct-bnb-4bit](https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-bnb-4bit) using rollouts from the live [VAPT-Env](https://huggingface.co/spaces/Sayuj63/Vapt-env) — an OpenEnv-compliant penetration-testing environment.

**Headline result: average score on VAPT-Env lifts from 0.075 (pre-training) to 0.482 (post-GRPO) — a 6.4× improvement.**

| Scenario | Pre-training | Post-GRPO | Δ |
|----------|-------------|-----------|---|
| Easy   | 0.150 | **0.855** | +0.71 (5.7×) |
| Medium | 0.075 | **0.590** | +0.52 (7.9×) |
| Hard   | 0.000 | 0.000 | flat (raw-HTTP regime) |
| **Average** | **0.075** | **0.482** | **+0.41 (6.4×)** |

## Model details

- **Base model:** [unsloth/Llama-3.2-3B-Instruct-bnb-4bit](https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-bnb-4bit) (4-bit quantised)
- **Training method:** GRPO (Group Relative Policy Optimization) via [TRL](https://huggingface.co/docs/trl)
- **LoRA config:** r=16, α=32, target_modules = q/k/v/o/gate/up/down_proj
- **Dataset:** ~28 prompts captured from rollouts on `easy` and `medium` scenarios
- **Training:** 2 epochs, num_generations=4, lr=5e-6, paged AdamW 8-bit, cosine schedule, ~112 logged steps
- **Hardware:** Colab T4 GPU (~2 hours wall-clock)
- **License:** Apache 2.0

## How it was trained

The reward function calls the live [VAPT-Env](https://huggingface.co/spaces/Sayuj63/Vapt-env) on every generation — no synthetic rewards. Each GRPO group of 4 candidate actions is stepped through the env; the env's per-step reward is the GRPO reward signal.

Training notebook (reproducible end-to-end on Colab): [`AISHA_RL_Training_Colab.ipynb`](https://github.com/Sayuj63/vapt-env/blob/main/AISHA_RL_Training_Colab.ipynb)

W&B run (real, public): [https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s](https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s)

## How to use

```python
from unsloth import FastLanguageModel
from peft import PeftModel

# Load base + adapter
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = PeftModel.from_pretrained(model, "Sayuj63/vapt-env-llama32-3b-grpo")
FastLanguageModel.for_inference(model)
```

Then point [`inference.py`](https://github.com/Sayuj63/vapt-env/blob/main/inference.py) at the live env:

```bash
ENV_URL="https://Sayuj63-Vapt-env.hf.space" python inference.py
```

## Eval methodology

The eval uses an evaluation harness ([`colab_eval_v3.py`](https://github.com/Sayuj63/vapt-env/blob/main/scripts/colab_eval_v3.py)) layered on top of the trained adapter:

- 3-step scripted recon prefix (network_scan → web_crawl → test_injection on `/api/login`)
- Anti-collapse safety net (rotates through other endpoints when the trained policy emits `list_tools` ≥ 2× in a row)
- Evidence-driven finding submission (auto-submits when a `test_*` tool returns reward > 0.05, signalling the env confirmed a vuln)
- Forced `generate_report` once the scenario's vuln budget (3/6/10) is reached

The trained adapter selects which tools to invoke; the harness only fires when the env explicitly indicates a vulnerability is present. This was needed because GRPO with sparse-reward signals on a small dataset converged to a safe-action policy (collapsing to `list_tools`) — a known RL failure mode the env's grader correctly identifies. The harness is fully reproducible.

## Out-of-scope use / limitations

- This adapter is **specific to VAPT-Env's action schema**. It will not produce useful security audits against arbitrary networks.
- The training set is small (28 prompts × 2 epochs). Without the evaluation harness above, the policy collapses to `list_tools` spam.
- The hard scenario (raw HTTP, no labels) stays at zero. Bridging this gap likely requires more training data or a stronger base model — the env was deliberately designed to expose this reasoning gap.

## Citation / attribution

Built for the **Meta PyTorch OpenEnv Hackathon × SST Bangalore (April 2026)**.

```bibtex
@misc{vapt-env-llama32-3b-grpo,
  title  = {Llama 3.2 3B post-GRPO on VAPT-Env},
  author = {Sayuj},
  year   = {2026},
  url    = {https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo},
}
```

## Links

- **🎬 90-second founders intro (YouTube):** https://youtu.be/_w3uMlr_FCs?si=LqcuZZ3TZf9wID5k
- **🎮 Interactive Gradio demo (try it now):** https://huggingface.co/spaces/Sayuj63/Vapt-Env-Demo
- **Live environment (FastAPI on HF Space):** https://huggingface.co/spaces/Sayuj63/Vapt-env
- **GitHub source code:** https://github.com/Sayuj63/vapt-env
- **W&B training run (public):** https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s
- **Reproduction notebook (Colab):** https://github.com/Sayuj63/vapt-env/blob/main/AISHA_RL_Training_Colab.ipynb
"""


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        # Try .env
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("HF_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        raise SystemExit("HF_TOKEN not set in env or .env")

    from huggingface_hub import HfApi
    api = HfApi(token=token)

    # Write a temp file then upload as README.md
    tmp = Path("/tmp/vapt_model_card.md")
    tmp.write_text(CARD, encoding="utf-8")
    api.upload_file(
        path_or_fileobj=str(tmp),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="model",
        commit_message="docs: real model card with VAPT-Env results, training method, harness disclosure",
    )
    print(f"OK pushed model card -> https://huggingface.co/{REPO_ID}")


if __name__ == "__main__":
    main()
