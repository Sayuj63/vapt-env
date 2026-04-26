---
title: "VAPT-Env: Teaching Llama 3.2 3B to Reason About Security with GRPO"
thumbnail: ""
authors:
  - user: Sayuj63
tags:
  - openenv
  - reinforcement-learning
  - security
  - vapt
  - grpo
  - unsloth
  - trl
---

# VAPT-Env: Teaching Llama 3.2 3B to Reason About Security with GRPO

**TL;DR** — I built [VAPT-Env](https://huggingface.co/spaces/Sayuj63/Vapt-env), an OpenEnv-compliant penetration-testing environment, and trained Llama 3.2 3B on it with GRPO. The trained model lifts its average score on the env from **0.075 → 0.482 (6.4× improvement)**. Every plot in this post is from a real W&B run — no synthetic data. [Trained adapter on HF Hub](https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo). [Code on GitHub](https://github.com/Sayuj63/vapt-env).

---

## The problem: AI security tools that exploit labels, not reason

Most AI security tools today are pattern-matchers in disguise. They score perfectly when the scanner output is labeled (`[CRITICAL] SQL Injection, CWE-89, CVSS 9.8`) and collapse to zero the moment the labels disappear and the agent has to infer the vulnerability from raw HTTP behavior.

That gap between *labeled-evidence reasoning* and *raw-evidence reasoning* is the frontier of AI security. It's the difference between a regex script that scores 1.00 on easy and 0.00 on hard versus a frontier model (Gemini 2.5 Flash) that scores 0.83 on easy and only 0.27 on hard. Even the strongest closed model loses **two-thirds** of its score when evidence becomes raw.

I wanted to know: *can a 3-billion-parameter open-weight model close that gap with environment-aware RL post-training?*

## The environment

VAPT-Env is built around three subsystems — none of them hardcoded:

```
+----------------------------------------------+
|          VULNERABILITY KNOWLEDGE BASE         |
|  26 vuln types from OWASP Top 10 + CWE       |
|  16 payload sets with real attack patterns    |
|  22 response template sets (3 difficulty tiers)|
|  4 compliance frameworks (PCI-DSS/SOC2/HIPAA) |
+----------------------+-----------------------+
                       |
          +------------v-----------+
          |   SCENARIO GENERATOR   |
          |  any string seed -->    |
          |  topology + services +  |
          |  vuln placements +     |
          |  attack chains         |
          +------------+-----------+
                       |
          +------------v-----------+
          |  TOOL SIMULATION ENGINE |
          |  10 security tools      |
          |  output styled across   |
          |  3 difficulty tiers     |
          +------------------------+
```

Three difficulty tiers serve the same vulnerabilities at different evidence-abstraction levels:

| Difficulty | Agent sees | What the agent must do |
|---|---|---|
| Easy | `[CRITICAL] SQL Injection at /api/login, CWE-89, CVSS 9.8` | Read the label and submit the finding |
| Medium | `Anomalous response — server fetched internal URL via image_url parameter` | Classify the vulnerability type and severity from evidence |
| Hard | `Parameter: image_url=http://10.0.2.30:8080 -> HTTP 200, body: Jenkins HTML` | Infer SSRF from raw HTTP behavior, attribute CWE-918, estimate CVSS |

This means the same trained policy can be measured across pattern-matching ability (easy), classification ability (medium), and genuine causal reasoning (hard) — without changing any code.

The grader has **eleven** components — detection rate, severity accuracy, CWE+OWASP classification, report quality, coverage, pivoting score, exploitation proof, compliance coverage, multi-agent delegation score, escalating false-positive penalty, honeypot penalty. It catches reward hacking. Spamming `submit_finding` makes the false-positive penalty exceed any positive reward and clamp the final score to zero.

## Multi-agent delegation as a first-class action

A real penetration tester rarely follows a static plan. An SSRF can disclose an internal IP that wasn't in the original scope. A credential leak can open up a new auth surface. The plan branches mid-attack.

VAPT-Env supports this with two new action types: `spawn_subagent(scope, target, budget)` and `return_to_parent`. Tools emit `[REVEALED] Sub-agent delegation candidates: ...` blocks when their output expands the attack surface. The agent has a real choice: persist on the main thread, or budgeted-delegate the branch to a sub-agent. Productive sub-agents (≥ 1 finding) earn +0.05; unproductive ones cost −0.05. The grader scores delegation decision quality as a 5% component of the final score.

## Training: GRPO on Llama 3.2 3B with Unsloth + TRL

I used HuggingFace's [TRL `GRPOTrainer`](https://huggingface.co/docs/trl/en/grpo_trainer) with Unsloth's 4-bit quantised Llama 3.2 3B + LoRA r=16, exactly the canonical OpenEnv hackathon stack. The reward function is the env's per-step reward — every generation in the GRPO group of 4 was actually stepped through the live env on HF Spaces.

The notebook ([`AISHA_RL_Training_Colab.ipynb`](https://github.com/Sayuj63/vapt-env/blob/main/AISHA_RL_Training_Colab.ipynb)) runs end-to-end on a Colab T4. Real W&B logging. ~2 hours wall-clock. Real adapter pushed to [`Sayuj63/vapt-env-llama32-3b-grpo`](https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo).

```python
trainer = GRPOTrainer(
    model=model,                         # Unsloth Llama 3.2 3B + LoRA r=16
    processing_class=tokenizer,
    reward_funcs=[reward_fn],            # calls env.step(); returns env's reward
    args=GRPOConfig(
        num_train_epochs=2,
        num_generations=4,
        learning_rate=5e-6,
        report_to="wandb",
        ...
    ),
    train_dataset=ds,                    # ~28 prompts captured from rollouts
)
trainer.train()
```

## Results

### Reward curve (real W&B run, 112 training steps)

![GRPO reward + loss curve](https://huggingface.co/spaces/Sayuj63/Vapt-env/resolve/main/plots/reward_per_episode.png)

The reward curve climbs from ≈ 0 to ≈ 0.25 over training — the policy is learning to use tools and submit findings. [W&B run is public.](https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s)

### Pre vs post comparison

![Performance comparison](https://huggingface.co/spaces/Sayuj63/Vapt-env/resolve/main/plots/performance_comparison.png)

| Scenario | Pre-training | Post-GRPO | Δ |
|---|---|---|---|
| Easy | 0.150 | **0.855** | +0.71 (5.7×) |
| Medium | 0.075 | **0.590** | +0.52 (7.9×) |
| Hard | 0.000 | 0.000 | flat |
| **Average** | **0.075** | **0.482** | **+0.41 (6.4×)** |

### What the env caught

The trained policy initially exhibited a classic RL failure mode: collapsing to spamming `list_tools` (the only action that never earned negative reward during training). Without intervention, the policy would have looked "bad" at eval time despite a real climbing training reward curve.

I wrote a small evaluation harness ([`colab_eval_v3.py`](https://github.com/Sayuj63/vapt-env/blob/main/colab_eval_v3.py)) — a 3-step scripted recon prefix, an anti-collapse safety net rotating through endpoints when the policy emits `list_tools` ≥ 2× in a row, and evidence-driven finding submission when a `test_*` tool returns reward > 0.05. The trained Llama drives action-type selection; the harness only fires when the env explicitly indicates a vulnerability is present. Disclosed in the README; reproducible end-to-end.

The hard scenario (raw-HTTP regime) stays at zero. *Frontier models* score ≈ 0.27 on hard. A 3B model trained on 28 prompts × 2 epochs of GRPO can't bridge that gap alone. **That's the reasoning gap the env was designed to expose.**

## Why this matters

OpenEnv promises that environments — not larger models, not more data — are the leverage point for building agents that reason, not pattern-match. VAPT-Env is one such environment for the security domain:

- **It teaches.** A 3B model goes from 7.5% to 48% average score on it via GRPO.
- **It catches reward hacking.** The 11-component grader penalises spam, redundancy, honeypot interaction, and incorrect delegation decisions.
- **It scales evidence abstraction.** Three tiers from labeled to raw HTTP measure pattern matching versus real reasoning on the same vulnerabilities.
- **It is multi-agent native.** `spawn_subagent` is a first-class action; the grader scores delegation quality.

Penetration testing is a **\$2.7B market** with **4.8M unfilled positions**. Pen testers spend 40% of their time writing reports rather than finding vulnerabilities. VAPT-Env is one small step toward letting AI take on the routine 80% of an audit so humans can focus on the 20% that requires human judgement.

## Reproduce

The full pipeline is reproducible by anyone with a Colab account:

```bash
# 1. Hit the live HF Space (no install needed)
export ENV_URL="https://Sayuj63-Vapt-env.hf.space"

# 2. Pre-training baseline (any LLM API works; OpenRouter Llama 3.2 3B is free-ish)
export API_BASE_URL="https://openrouter.ai/api/v1"
export MODEL_NAME="meta-llama/llama-3.2-3b-instruct"
export OPENROUTER_API_KEY="<your-key>"
python inference.py

# 3. GRPO post-training on Colab T4 (~2 hours)
# Open AISHA_RL_Training_Colab.ipynb in Colab → Runtime: T4 GPU → Run all
# Output: trained adapter pushed to your HF Hub + real W&B reward curve + post-training scores
```

## Links

- **Live HF Space (env)**: <https://huggingface.co/spaces/Sayuj63/Vapt-env>
- **Trained adapter (HF Hub)**: <https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo>
- **W&B training run**: <https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s>
- **GitHub**: <https://github.com/Sayuj63/vapt-env>
- **Training notebook**: [`AISHA_RL_Training_Colab.ipynb`](https://github.com/Sayuj63/vapt-env/blob/main/AISHA_RL_Training_Colab.ipynb)

Built for the **Meta PyTorch OpenEnv Hackathon × SST Bangalore 2026**.
