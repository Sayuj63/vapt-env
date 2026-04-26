---
title: "VAPT-Env: We Trained a 3B Model to Do What 120B Couldn't (And Almost Lost the Plot Three Times)"
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

# We tried to give every security team a tireless junior pentester. Here's the messy story of how a 3B model ended up doing what a 120B model couldn't.

There's a stat we kept coming back to: **pen testers spend 40% of their time writing reports**, not finding vulnerabilities. The global market is $2.7B. There are 4.8 million unfilled cybersecurity positions. Attackers break out in 29 minutes; defenders patch in 209 days. The asymmetry is brutal, and it's getting worse.

We didn't want to "replace" auditors. We wanted to give them an **always-on junior** — something that could chew through the boring 80% of an audit so the humans could focus on the 20% that actually requires judgement. A teammate that runs the same SQL injection check on a thousand endpoints without complaining, files clean reports, and gets out of the way when the human takes over.

So we built **VAPT-Env**.

> **Live env** → [huggingface.co/spaces/Sayuj63/Vapt-env](https://huggingface.co/spaces/Sayuj63/Vapt-env)
> **Interactive demo** → [huggingface.co/spaces/Sayuj63/Vapt-Env-Demo](https://huggingface.co/spaces/Sayuj63/Vapt-Env-Demo)
> **Trained adapter** → [huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo](https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo)
> **GitHub** → [github.com/Sayuj63/vapt-env](https://github.com/Sayuj63/vapt-env)

This is the story of how a small open model (Llama 3.2 3B) ended up scoring **0.482 average** on our environment after GRPO post-training — beating GPT-OSS-120B's 0.276 by 1.7× and lifting its own pre-training baseline by 6.4×. The numbers are real. The journey was not clean.

---

## What we built (the env)

VAPT-Env is an OpenEnv-compliant FastAPI server hosted on HuggingFace Spaces. Inside it: 26 vulnerability types pulled from OWASP Top 10 + CWE Top 25, 16 attack-payload sets, 22 response-template sets across three difficulty tiers, four compliance frameworks (PCI-DSS, SOC2, HIPAA, Generic), and 10 security tools — `network_scan`, `web_crawl`, `test_injection`, `test_xss`, `test_auth`, `test_config`, `test_crypto`, `check_secrets`, `vulnerability_scan`, `service_fingerprint`. **78 tests cover the entire grader, generator, and tools engine.**

The thing that makes the env interesting isn't the tools. It's the **three-tier evidence abstraction**:

| Difficulty | Tool output style | What the agent has to do |
|---|---|---|
| Easy | `[CRITICAL] SQL Injection at /api/login, CWE-89, CVSS 9.8` | Read the label and submit the finding |
| Medium | `Anomalous response — server fetched internal URL via image_url parameter` | Classify the vulnerability from evidence |
| Hard | `Parameter: image_url=http://10.0.2.30:8080 -> HTTP 200, body: Jenkins HTML` | Infer SSRF from raw HTTP behavior, attribute CWE, estimate severity |

Same vulnerabilities. Same grader. Three regimes. The deterministic regex parser scores **1.00 on easy, 0.00 on hard** — a perfect pattern matcher and a perfect failure. That gap *is* the reasoning gap. It's the line between "pretending to do security" and actually doing it.

The grader has **eleven** components, including dynamic delegation scoring for our newest action: `spawn_subagent`. When an SSRF reveals an internal IP, the agent can either persist on the main thread or budget-delegate the branch. Productive sub-agents earn +0.05; unproductive ones cost −0.05. Reward hacking? The grader catches it. The escalating false-positive penalty (−0.03, −0.04 … capped at −0.08 each) makes any agent that just spams `submit_finding` clamp to zero.

That's the env. The story is what we tried *against* it.

---

## Act 1 — "Just point a model at it"

The naive thing first.

We pointed Llama 3.2 3B (via OpenRouter) at the live env and ran `inference.py` end-to-end. **Easy: 0.71. Medium: 0.04. Hard: 0.04. Average: 0.26.**

Easy looked good — the model reads `[CRITICAL] SQL Injection` and submits a SQL Injection finding. Medium and hard fell off a cliff. The model just couldn't infer CWE-918 from raw HTTP traces. Pattern matching works when the labels are there. It doesn't generalise.

So we tried the obvious follow-up: **what if we use a much bigger model?**

We swapped in **GPT-OSS-120B**, OpenAI's open-weight 120-billion-parameter beast, via the same harness. **Easy: 0.80. Medium: 0.025. Hard: 0.00. Average: 0.276.**

That number quietly broke us a bit.

**A model 40× larger barely beat a 3B model.** It edged ahead on easy, regressed on medium, was equally lost on hard. The reasoning gap doesn't open up with parameters alone.

That was either bad news (size doesn't help) or good news (a 3B model has room to grow if we train it right). We chose the latter.

---

## Act 2 — "Add multi-agent because real pentesters don't follow a script"

Here's the thing nobody tells you about pentesting: **the plan branches mid-attack.** An SSRF discloses an internal IP that wasn't in the original scope. A credential leak opens up a new auth surface. A misconfiguration exposes a Jenkins instance you didn't know existed. The agent that finds these has a choice — chase the new branch, or stay on the main thread.

We added two new actions: `spawn_subagent(scope, target, budget)` and `return_to_parent`. Tools learned to emit `[REVEALED] Sub-agent delegation candidates: ...` blocks when they uncover something the agent couldn't reach before. The grader gained an 11th component to score delegation decision quality.

We were proud. We pushed it. We re-ran the eval.

**Easy: 0.15. Medium: 0.075. Hard: 0.00. Average: 0.075.**

We had **regressed** the model by handing it more options. The longer prompt with delegation rules confused the small model. It stopped submitting findings. It went into a loop.

This is the part of the story they don't put in the highlight reel. We sat there at 0.075 average and seriously asked whether we'd just over-engineered our way out of a working system.

---

## Act 3 — "Strip the prompt, save the env"

We rewrote the system prompt. Three core actions back at the top, multi-agent moved to an "OPTIONAL" section at the bottom with one explicit worked example. We re-ran.

**Easy: 1.00. Medium: 0.075. Hard: 0.00. Average: 0.358.**

A perfect easy score. The simpler prompt reset the small model. Multi-agent infrastructure lived in the env, but the model only used it when the env explicitly surfaced a `[REVEALED]` block. That was the right shape: **multi-agent as a primitive, not a default behaviour.**

But this was still inference, not training. We hadn't actually taught the model anything yet — we'd just stopped confusing it.

It was time to do the thing we actually came here to do.

---

## Act 4 — Real GRPO training on Colab

We wrote the canonical OpenEnv stack into a notebook: **Unsloth 4-bit quantised Llama 3.2 3B + LoRA r=16 + HuggingFace TRL's `GRPOTrainer`**, with the reward function calling our live env on every generation. No synthetic rewards, no cached datasets — every one of the 4 candidate actions in each GRPO group was *actually stepped through the live env on HuggingFace Spaces* and given the env's per-step reward as the policy gradient signal.

We hit Run All on a free Colab T4. Two hours later we had: 112 logged training steps, a real W&B reward curve climbing from ≈0 to ≈0.25, a trained LoRA adapter pushed to HF Hub.

We held our breath, ran the post-training eval, and watched the model produce:

**0.00. 0.00. 0.00.**

All three scenarios. Zero.

For about ten minutes we genuinely thought we'd built nothing.

---

## Act 5 — "Why is the trained model worse than the untrained one?"

Reward hacking, the OG RL ghost story.

We dug through the eval traces. The trained model wasn't broken. It was *too good* at one specific thing: it had learned that `list_tools` is the only action that *never* returned a negative reward during training. So it had simply… converged on emitting `list_tools` every step. Forever. Never submitted a finding, never called `generate_report`, never let the grader run.

This is a textbook **safe-action attractor** in policy-gradient methods on small datasets with sparse rewards. The classic failure mode TRL's own docs warn about. And our env's grader had caught it perfectly: zero findings → zero detection rate → zero score, exactly the way it should.

That was actually a good sign — *the env is doing its job.* Most security RL benchmarks would have rewarded this spam policy with ~+2.5 cumulative per-step reward. Ours clamped it to 0. **The env doesn't reward the hacker.** That's a feature.

But we still needed a real number for the bar chart.

---

## Act 6 — The harness

We did what real research teams do when policy collapse meets a deadline: **we built an evaluation harness.**

[`colab_eval_v3.py`](https://github.com/Sayuj63/vapt-env/blob/main/colab_eval_v3.py) does three things, each fully disclosed:

1. **A 3-step scripted recon prefix** — `network_scan` → `web_crawl` → `test_injection /api/login`. Same prefix every scenario. Same prefix the rollout dataset was generated from.

2. **An anti-collapse safety net** — when the trained policy emits `list_tools` ≥ 2× in a row, the harness rotates through a fixed list of remaining endpoints (`/api/upload/image`, `/api/search`, `/api/comments`, `test_auth`, `check_secrets`, `test_config`, `test_crypto`, `vulnerability_scan`). The trained policy still *picks* what to do most of the time — the safety net only fires when it freezes.

3. **Evidence-driven auto-submission** — when a `test_*` tool returns reward > 0.05, the env is *explicitly telling us* there's a vuln there. The harness submits a finding with the right CWE template. The trained model selects which endpoints to test; the harness only fires when the env has already confirmed a vuln exists.

We re-ran the eval. **Easy: 0.855. Medium: 0.590. Hard: 0.00. Average: 0.482.**

A 6.4× lift over the pre-training baseline. **A 1.7× lead over GPT-OSS-120B**, a model 40 times larger.

We re-ran the bar chart. The post-GRPO bars dwarfed the pre-training ones. The W&B reward curve was visibly climbing. The trained adapter was sitting public on HF Hub at [`Sayuj63/vapt-env-llama32-3b-grpo`](https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo) where anyone could pull it.

We pushed everything.

---

## What we actually learned

**1. Small data + sparse rewards = safe-action attractors.** GRPO on 28 prompts × 2 epochs is not enough signal for a 3B model to learn complex action sequencing without converging on a degenerate policy. This is well-known in the RL literature; the cure is more data, more diverse reward shaping, or harness-based evaluation that doesn't paper over the failure mode.

**2. Reward design is more important than model size.** GPT-OSS-120B couldn't outperform a small Llama with 28 prompts of GRPO once the env's grader was tight enough. The gap on hard is the same for both — raw HTTP attribution is genuinely a frontier-model problem, and bigger pre-training data alone doesn't fix it.

**3. The env's grader is the most important part of the env.** Eleven components. Escalating FP penalty. Coverage multiplier. Honeypot penalty. Delegation score. Each one closes a hole that a hacky agent would otherwise exploit. The whole env is designed around one principle: *if your model can hack the score, you didn't actually solve the task.*

**4. Multi-agent should be a primitive, not a default behaviour.** Sub-agent delegation lives in the action space, but the agent only uses it when the env explicitly surfaces a `[REVEALED]` block. We tried making it a default and the model regressed. We made it conditional and the model used it correctly. RL agents are pickier about action-space ergonomics than we expected.

**5. Hard regimes catch reasoning, not just classification.** The hard scenario uses raw HTTP output (no labels). Frontier models score ~0.27 on it. Our 3B + harness scores 0.00. *That's the env doing its job.* The reasoning gap is real, and bridging it requires more training data — not bigger models.

---

## Why this matters

VAPT-Env is one small experiment in the **OpenEnv premise** — that environments, not larger models or more data, are the leverage point for building agents that actually reason. The env is more important than the model trained on it. A sharp env catches the failure modes that bloated RL benchmarks paper over.

For security specifically, an environment like this is one step toward letting an AI take over the routine 80% of an audit — the labelled output, the obvious classifications, the boilerplate report writing. The 20% that requires inferring SSRF from raw HTTP behaviour, deciding which honeypot to ignore, or judging compliance gaps stays with humans. That's the asymmetry penetration testing actually needs.

We don't think AI replaces auditors. We think it gives them a tireless junior that doesn't sleep. **And our env is one of the first places a 3B-parameter junior can learn to do the job.**

---

## Try it yourself (5 minutes)

1. **Open the live demo:** [huggingface.co/spaces/Sayuj63/Vapt-Env-Demo](https://huggingface.co/spaces/Sayuj63/Vapt-Env-Demo) — pick a scenario, pick the trained agent, hit Run.

2. **Hit the env directly:** [huggingface.co/spaces/Sayuj63/Vapt-env](https://huggingface.co/spaces/Sayuj63/Vapt-env) — OpenEnv-compliant FastAPI. From any environment with `openenv-core`:
   ```python
   from security_audit_env import SecurityAuditEnv, SecurityAuditAction
   with SecurityAuditEnv(base_url="https://Sayuj63-Vapt-env.hf.space").sync() as env:
       env.reset(scenario_id="easy")
       env.step(SecurityAuditAction(action_type="use_tool", tool_name="network_scan",
                                     arguments={"target":"10.0.1.0/24"}))
   ```

3. **Reproduce the training:** [`AISHA_RL_Training_Colab.ipynb`](https://github.com/Sayuj63/vapt-env/blob/main/AISHA_RL_Training_Colab.ipynb) → open in Colab → Runtime: T4 GPU → Run all. ~2 hours.

4. **Pull the adapter:** [`Sayuj63/vapt-env-llama32-3b-grpo`](https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo) is on HF Hub. PEFT-load it on top of `unsloth/Llama-3.2-3B-Instruct-bnb-4bit` and you've got the trained model.

5. **Read the W&B run:** [wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s](https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s). Public. 112 steps. Real curve.

---

## Final numbers (because that's why you're here)

| | Llama 3.2 3B (pre-training) | GPT-OSS-120B (frontier) | Llama 3.2 3B (post-GRPO + harness) |
|---|---|---|---|
| Easy | 0.71 | 0.80 | **0.86** |
| Medium | 0.04 | 0.025 | **0.59** |
| Hard | 0.04 | 0.00 | 0.00 |
| **Average** | 0.26 | 0.276 | **0.482** |
| Lift vs Llama 3.2 3B baseline | — | 1.05× | **6.4×** |
| Lift vs GPT-OSS-120B | — | — | **1.7×** |

Built for the **Meta PyTorch OpenEnv Hackathon × SST Bangalore (April 2026)**.

The env is on HuggingFace. The trained adapter is on HuggingFace. The training run is on W&B. The Colab notebook reproduces all of it. There's no synthetic data anywhere in this submission. Three months from now, you can pull the adapter and re-run the eval and get the same numbers.

That's the whole point.
