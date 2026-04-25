# 2-Minute Demo Video Script — VAPT-Env

**Goal:** Land 30% Storytelling and reinforce the 40% Innovation case in under 120 seconds.
**Tools you need:** screen recorder (Mac: `Cmd+Shift+5` → record), terminal at the project root, browser, optional voiceover mic.
**Final upload:** YouTube (unlisted is fine), then add `**Demo Video:** <YouTube URL>` to the README under the Live Environment line.

---

## Shot list (target 110-120 seconds total)

### 0:00 – 0:15 — Hook (15s)
**Screen:** Open the README on https://huggingface.co/spaces/Sayuj63/Vapt-env in a browser. Zoom to the headline table:

> | Easy | `[CRITICAL] SQL Injection, CWE-89, CVSS 9.8` | regex 1.00 | Gemini 0.83 |
> | Hard | `POST /login: 1000 reqs in 18.7s, 0 blocked`     | regex 0.00 | Gemini 0.27 |

**Voiceover:**
> "Most AI security tools just parse labeled scanner output. We built an environment where the labels disappear — and we measure what an LLM can actually reason out from raw evidence."

---

### 0:15 – 0:35 — The reasoning gap, live (20s)
**Screen:** Cut to terminal. Type and run:

```bash
ENV_URL=https://Sayuj63-Vapt-env.hf.space MODEL_NAME=openai/gpt-oss-120b uv run python inference.py
```

**Don't show the full run** — pause the recording, wait for it to finish (or paste pre-recorded output), then resume. Show just the last block:

```
BASELINE SCORES
  easy      : 1.0000
  medium    : 0.0750
  hard      : 0.0000
  average   : 0.3583
```

**Voiceover:**
> "Same env, same grader, three difficulty tiers — easy is labeled output, hard is raw HTTP. Frontier models nail easy and collapse on hard. That gap *is* the reasoning gap. It's reproducible — anyone with five dollars of OpenRouter credit can verify these numbers."

---

### 0:35 – 1:15 — Multi-agent delegation in action (40s)
**Screen:** Run the curated demo:

```bash
PYTHONPATH=. uv run python demo_multiagent.py
```

Highlight three frames as they scroll past:

1. **The `[REVEALED]` block** — show the SSRF disclosing two new internal hosts.
2. **The `spawn_subagent` line** — sub-agent registered with budget=6.
3. **The `PRODUCTIVE (reward +0.05)` line** at return_to_parent.
4. The final grader output showing **Pivoting Score: 1.00, Classification: 1.00, subagent_productive: 1**.

**Voiceover:**
> "Real pentesters don't follow a static plan — they discover during the attack. An SSRF reveals an internal IP. The agent decides: persist on the main thread, or spawn a sub-agent on the new branch. We built dynamic attack surface and budgeted sub-agents into the environment — the productive ones earn delegation reward, the unproductive ones cost. The grader has a 5% Delegation Score component that rewards good multi-agent decision-making."

---

### 1:15 – 1:45 — Three themes, one env (30s)
**Screen:** Show the README intro section with the triple-theme bullets.

**Voiceover:**
> "VAPT-Env hits three of the hackathon themes in one design. Theme 3.1 World Modeling — partially observable enterprise simulation, real tools, dynamic state. Theme 2 Long-Horizon Planning — 25 to 45 step audits with sparse rewards and recovery paths. Theme 1 Multi-Agent Interactions — sub-agent delegation as a first-class action."

---

### 1:45 – 2:00 — Training-curve teaser + close (15s)
**Screen:** Show `plots/reward_per_episode.png` (or the W&B run URL once you have one).

**Voiceover:**
> "We have a baseline: Llama 3.2 3B scores zero point seven one on easy out of the box. Next we train it with GRPO on this env and watch it close the reasoning gap. The pipeline is in `AISHA_RL_Training_Colab.ipynb` — open it on a Colab T4 and run all. That's VAPT-Env. Live link in the description."

---

## Voiceover quick-record alternative

If you can't record yourself, use macOS Text-to-Speech: open Terminal and run:

```bash
say -v Daniel -o voiceover.aiff -f docs/blog/VIDEO_SCRIPT.md
```

(That'll dump the whole script as audio; you can splice the relevant chunks in iMovie or QuickTime.)

## Final checklist before upload

- [ ] Total length 110-120 seconds
- [ ] Live HF Space URL visible at least once
- [ ] At least one frame of `[REVEALED]` block
- [ ] At least one frame of `spawn_subagent` and `PRODUCTIVE` outcome
- [ ] Final grader scores visible (showing Pivoting=1.00 / Classification=1.00 etc.)
- [ ] Upload to YouTube *Unlisted*
- [ ] Add link to README under Live Environment line: `**Demo Video:** <URL>`
- [ ] Push README + commit to HF Space (it auto-rebuilds)
