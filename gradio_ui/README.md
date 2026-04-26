---
title: VAPT-Env Live
emoji: "🛡️"
colorFrom: teal
colorTo: indigo
sdk: gradio
sdk_version: "5.4.0"
app_file: app.py
pinned: false
short_description: "Live demo: Llama 3.2 3B before vs after GRPO on VAPT-Env"
---

# VAPT-Env — Live Operations Center

Gradio demo over the live VAPT-Env on HuggingFace Spaces. Pick a scenario, pick an agent, hit run — watch Llama 3.2 3B before vs after GRPO post-training side-by-side.

**Headline result:** Llama 3.2 3B average score 0.075 → 0.482 (6.4× improvement) post-GRPO.

**Companion artifacts:**
- Live env (FastAPI, OpenEnv-compliant): https://huggingface.co/spaces/Sayuj63/Vapt-env
- Trained LoRA adapter: https://huggingface.co/Sayuj63/vapt-env-llama32-3b-grpo
- W&B training run: https://wandb.ai/sayujpillai63-itm/vapt-env-grpo/runs/ln2jq71s
- GitHub: https://github.com/Sayuj63/vapt-env

## How to run locally

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:7860
```
