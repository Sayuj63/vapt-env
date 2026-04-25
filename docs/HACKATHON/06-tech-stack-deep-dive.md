# Tech Stack Deep Dive — What Each Tool Does and Its 2026 Frontier

*Purpose: deep technical reconnaissance for the Meta PyTorch OpenEnv Hackathon finalist team. For each tool: what it is, what it does at each layer, 2026 frontier features, integration points, gotchas that break the LLM-screener gate, real APIs, and depth-of-help ceiling.*

---

## Executive summary — what's a differentiator, what's table stakes

**Table stakes (every serious team has these):**
- OpenEnv (you must submit an env)
- TRL GRPOTrainer (default training path)
- HF Spaces + Docker (deployment target)
- PyTorch, Python, Colab (substrate)
- W&B (logging)

**Pitch differentiators (most teams won't use these at depth):**
1. **TRL v1.2 `environment_factory` with multi-env + per-env reward masking** — released 2026-04-17, 2 days before the hackathon email. Almost nobody outside the HF core team has done multi-environment GRPO yet.
2. **OpenEnv v0.2.2+ MCP native environments (`MCPEnvironment`)** — RFC 003, production+simulation modes, tool discovery through MCP JSON-RPC. Lets your env speak to *any* MCP server in the world.
3. **RFC 004 Rubrics** — LLM-as-judge rewards with delayed signals, baked into v0.2.2. Most teams will hand-write reward functions.
4. **Unsloth ultra-long-context RL** (Jan 2026 update) — 380K ctx gpt-oss on a single B200, 110K on an H100. If your env benefits from long horizons, this is your moat.
5. **RFC 005 agentic harness integration** — makes your env callable from Claude Code / OpenClaw directly. Zero teams will ship this.
6. **TRL v1.1 AsyncGRPOTrainer + chunked LM head** — 44× lower peak memory on 8K seq. Unlocks bigger models on Colab.
7. **Torchforge Services model** (`.route()`, `.fanout()`, `.session()` adverbs on Monarch actors) — sticky-session KV cache reuse is brand new.
8. **TRL v1.2 SSDTrainer (self-distillation, no reward model)** — self-improvement loop with no verifier needed.

---

## Tool 1: OpenEnv (meta-pytorch/OpenEnv)

**Elevator:** A Gymnasium-style interface library + server runtime for defining isolated, reproducible RL environments that agents/LLMs train against; current v0.2.3 (Mar 28 2026).

### What it does at each layer
- **Contract layer:** Defines typed `Action`, `Observation`, `State`, `StepResult` Pydantic models per environment. Standardizes `reset()`/`step(action)`/`state()`.
- **Server runtime:** Wraps your env in a FastAPI app (`create_app(...)`) inside a Docker container, exposed over HTTP + WebSocket. Handles concurrency, session IDs, `/web` UI, `/health`.
- **Client runtime:** Auto-generated Python client (`MyEnv(base_url=...)`). Async-first (`async with EchoEnv(...) as client:`) with sync wrappers.
- **Publishing layer:** Bundles env as a Hugging Face Space (Docker SDK), pip-installable via `git+https://huggingface.co/spaces/<org>/<env>`.
- **Catalog layer:** HF collection `openenv/openenv-environment-hub`, discoverable by short name or repo ID.

### Latest features (Q4 2025 → Q1 2026)
- **v0.2.1 (Feb 4 2026):** First MCP support lands (FastMCP integration). TDD workflow with git hooks and skills. RFC 004 rubrics introduced.
- **v0.2.2 (Mar 20 2026 — THE BIG ONE):**
  - **MCPEnvironment** with tool discovery (`ListToolsAction`), tool-call execution (`CallToolAction`), FastMCP 2.x/3.x compatibility, reserved-name validation, persistent MCP sessions, production vs simulation modes, code mode support.
  - **Async-first clients** with persistent WebSocket sessions + sync wrappers.
  - **Rubric/evaluation support** with delayed rewards and LLM-based scoring (RFC 004).
  - **Auto-discovery API** — load env by short name or Hub repo ID (`load_env("echo")`).
  - **Built-in web UI** at `/web` with dynamic forms, action history, live state.
  - **Creator CLI** (`openenv init`, `build`, `validate`, `push`, `fork`, `serve`, `skills`).
  - **One-command HF publishing** + fork/duplicate for Spaces + custom registry push.
  - **GenericEnvClient / GenericAction** — raw-dict access without installing env-specific code (great for testing unknown envs).
- **v0.2.3 (Mar 28 2026 — polish release):**
  - `GET /` + `GET /web` redirect to `/web/` for Gradio-backed Spaces.
  - `GET /web/state` returns 409 before reset (instead of 500).
  - `POST /web/reset` accepts optional reset kwargs.
  - Shared `gradio_web` probe, `repl_web` expanded for root-path validation.
  - Canonical collection discovery defaults to first-party unsuffixed Spaces.
  - REPL-specific Gradio control panel retained + server compat fixes for Hub.

### Killer integration points
- **↔ TRL:** `GRPOTrainer(environment_factory=MyEnv)` — TRL imports `openenv-core>=0.2.1` implicitly. Works over WebSocket to your Space.
- **↔ HF Spaces:** `openenv push` one-shot publishes; Space provides the Docker runtime AND the web UI AND the pip install path.
- **↔ MCP (RFC 003):** Wrap any MCP server as an env; or expose env actions *as* MCP tool calls (RFC 004).
- **↔ smolagents:** `coding_env` uses smolagents sandbox under the hood for persistent-context Python execution.
- **↔ Claude Code / OpenClaw (RFC 005):** agentic-harness integration — your env becomes a skill any harness can call.

### Gotchas that break the LLM screener
- **Concurrency trap:** default `max_concurrent_envs=1`. TRL opens N WebSockets (one per generation). MUST set `SUPPORTS_CONCURRENT_SESSIONS = True` and `create_app(..., max_concurrent_envs>=generation_batch_size)` or training hangs and the screener will see no reward signal.
- **Platform flag:** `docker run --platform linux/amd64 ...` is mandatory on Apple Silicon. Without it the Space image fails to run on a judge's Mac.
- **Duplicate the Space for training:** shared community Spaces throttle to 1 session — training will appear to "work" for 1 episode then silently stall.
- **Port collision:** map Space port 8000 → host 8001 so vLLM can keep 8000.
- **Docstring-driven tool schema:** tool methods MUST have `Args:`-style docstrings with typed params or TRL generates a broken tool schema and the model never calls them. (Screener sees 0 reward.)
- **`reset()` signature:** must accept `**kwargs` — TRL forwards dataset columns into it. Not doing this crashes on first batch.
- **`__init__` no-args rule:** TRL calls `MyEnv()` with zero args. Configure via module-level vars or env vars, not constructor args.

### Specific APIs / commands
```python
# Core env author code
from openenv import Action, Observation, Environment, create_app

@dataclass
class MyAction(Action):
    move: str

@dataclass
class MyObservation(Observation):
    board: list[list[str]]
    reward: float
    done: bool

class MyEnv(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True
    def reset(self, **kwargs) -> MyObservation: ...
    def step(self, action: MyAction) -> StepResult[MyObservation]: ...

app = create_app(MyEnv, MyAction, MyObservation, max_concurrent_envs=64)
```

```bash
# CLI
openenv init my_env
openenv validate                    # run contract checks
openenv build                       # docker build
openenv serve --port 8000           # local run
openenv push --repo-id me/my_env    # HF Space deploy
openenv fork openenv/echo_env       # duplicate existing env

# Docker deploy
docker run -d -p 8001:8000 --platform linux/amd64 registry.hf.space/<org>-<env>:latest
```

```python
# MCP environment (RFC 003)
from openenv.mcp import MCPEnvironment, ListToolsAction, CallToolAction
env = MCPEnvironment(mcp_server_urls=["http://localhost:3333"])
tools = env.step(ListToolsAction())                         # discovers tools
result = env.step(CallToolAction(tool_name="search",
                                 parameters={"q": "..."}))
```

### Depth-of-help ceiling
OpenEnv takes you all the way from env definition → containerized deployment → HF Space → pip-installable artifact. It does **not** do: reward shaping (that's your code), training (TRL's job), or evaluation harnesses beyond rubrics (you wire those yourself). Hard ceiling: single-process-per-episode. If you need true multi-agent concurrent interaction (not just parallel rollouts), you hand-roll on top.

---

## Tool 2: HF TRL — Transformers Reinforcement Learning

**Elevator:** HuggingFace's RL post-training library; the canonical place where GRPO, DPO, KTO, PPO live. v1.2.0 (Apr 17 2026) landed 2 days before the hackathon email.

### What it does at each layer
- **Algorithm layer:** Implementations of GRPO, DPO, KTO, PPO, GSPO, SFT, DPPO, VESPO, SDPO, SSDTrainer (v1.2 self-distillation, no reward model), DistillationTrainer.
- **Rollout layer:** Handles multi-turn generation via vLLM (colocate or server mode), tool-call parsing, environment stepping.
- **Reward layer:** Reward functions are plain Python callables receiving `environments` kwarg.
- **Logging layer:** Native W&B / TensorBoard / MLflow via `report_to`.
- **Env layer:** `environment_factory` (recommended) or `rollout_func` (escape hatch).

### Latest features (v1.0 → v1.2 diff)
- **v1.0.0 (Mar 31 2026):**
  - **AsyncGRPOTrainer** — decouples generation from gradient updates via external vLLM server.
  - **VESPO** (variational sequence-level soft PO) — addresses training instability with smooth asymmetric Gamma weighting.
  - **DPPO** (divergence-based PPO clipping).
  - **SDPO** (self-distillation using model's high-reward trajectories as teacher).
  - Reward functions can return extra diagnostic columns via `log_extra` / `log_metric`.
  - 35% faster packing (BFD strategy, `"bfd_split"`).
  - v0→v1 migration guide published.
- **v1.1.0 (Apr 12 2026):**
  - **DistillationTrainer** — on-policy knowledge distillation with generation buffers (up to 40× speedup), external teacher support, binary-encoded logprobs (~5× payload reduction).
  - **AsyncGRPOTrainer** chunked LM-head computation → **44× lower peak memory on 8192-token sequence**.
  - SFTTrainer auto-patches chat templates missing `{% generation %}` markers.
  - Tool-calling expanded: GPT-OSS, GLM-4-MoE, Qwen3-VL, Gemma 4.
  - VLM training end-to-end with images in tool responses.
- **v1.2.0 (Apr 17 2026 — HACKATHON RELEASE):**
  - **SSDTrainer** — self-distillation without reward models (samples at training-time temp, fine-tunes on unverified samples).
  - GRPOTrainer: tool results now use **rollback instead of truncation** when exceeding `max_completion_length` (eliminates ~80 lines of image-boundary bookkeeping).
  - Tool-calling: Llama 3.1/3.2 + DeepSeek-V3 templates.
  - KTO/DPO alignment cleanup.

### Killer integration points
- **↔ OpenEnv:** `environment_factory=MyEnvClass` — the one-line integration. TRL discovers tool methods from docstrings.
- **↔ vLLM:** `use_vllm=True, vllm_mode="colocate"` (1-GPU Colab) or `"server"` (2+ GPU). Colocate shares GPU memory between inference + train.
- **↔ W&B:** `GRPOConfig(report_to="wandb", log_completions=True)` — logs completions as rich HTML tables.
- **↔ Unsloth:** Unsloth monkey-patches TRL's GRPOTrainer; you write TRL code and get Unsloth speedups transparently.
- **↔ HF Hub:** `push_to_hub=True` uploads trained LoRA/full checkpoint as a Model repo.
- **↔ HF Jobs (new v0.27+):** `uv run examples/scripts/openenv/echo.py` + `hf jobs` runs training in HF cloud.

### Gotchas that break the LLM screener
- **`transformers>=5.2.0` requirement for `environment_factory`** — main branch install. Pinning to older transformers silently disables the factory path.
- **`environment_factory` is marked experimental** — its exact signature may change; pin TRL to `1.2.0` exactly.
- **Pass the CLASS not an instance:** `environment_factory=MyEnvClass` (no parens). Passing `MyEnvClass()` will break multi-rollout parallelism.
- **`max_completion_length` is TOTAL tokens across all turns**, not per-turn. Default 256–1024 will cut off multi-turn episodes mid-game — bump to 4096 minimum for anything non-trivial.
- **Tool method discovery is reflection-based:** any public method (no leading `_`) becomes a tool. A stray `def helper(self)` becomes an advertised tool and confuses the model.
- **Reward metric logging ignores `reward_weights`** (open issue #5352 as of Mar 2026) — the displayed reward is unweighted sum even though training uses weights. Don't panic if W&B chart looks off.
- **`num_generations` must divide `per_device_train_batch_size × gradient_accumulation_steps`** or GRPO crashes with an obscure assert.

### Specific APIs
```python
from trl import GRPOTrainer, GRPOConfig

trainer = GRPOTrainer(
    model="Qwen/Qwen3-1.7B",
    reward_funcs=[reward_func],                 # can be list of funcs
    train_dataset=dataset,
    args=GRPOConfig(
        use_vllm=True,
        vllm_mode="colocate",                   # or "server"
        num_generations=4,
        gradient_accumulation_steps=64,
        max_completion_length=4096,
        chat_template_kwargs={"enable_thinking": False},
        log_completions=True,
        report_to="wandb",
        loss_type="gspo",                       # or "grpo" or "dr_grpo"
        epsilon=0.2,
        epsilon_high=0.28,                      # one-sided clipping
        delta=1.5,                              # two-sided clipping
        mask_truncated_completions=True,
    ),
    environment_factory=MyEnvClass,             # THE factory — CLASS, not instance
)
trainer.train()
trainer.push_to_hub("my-team/grpo-wordle-qwen3-1.7b")
```

```bash
# vLLM server mode (2+ GPU)
CUDA_VISIBLE_DEVICES=0 trl vllm-serve --model Qwen/Qwen3-1.7B --host 0.0.0.0 --port 8000
CUDA_VISIBLE_DEVICES=1 python train.py --vllm-mode server --vllm-server-url http://localhost:8000

# HF Jobs
uv run examples/scripts/openenv/wordle.py
```

### Depth-of-help ceiling
TRL owns the entire training pipeline from prompts → trained model. It *does not* own: memory optimization (Unsloth), env definition (OpenEnv), distributed-scale scheduling (Torchforge/accelerate). On a Colab T4 you'll hit OOM on any model >3B without Unsloth.

---

## Tool 3: Unsloth

**Elevator:** A drop-in speed+memory optimizer for HF transformers that enables LoRA/QLoRA GRPO on consumer GPUs, with 5–8× memory reduction and 2–3× speedups.

### What it does at each layer
- **Kernel layer:** Triton kernels for LM head, attention, MLP, layer norm. `torch.compile` integration yields 8× smaller memory for linear kernels.
- **Model loader layer:** `FastLanguageModel.from_pretrained(..., load_in_4bit=True, fast_inference=True)` — patches HF model with Unsloth kernels in-place.
- **Training adapter:** Monkey-patches TRL's GRPOTrainer so you write TRL code and get Unsloth's perf transparently.
- **vLLM shared memory:** Unsloth eliminates the 5GB double-alloc overhead when vLLM and training both hold weights.

### Latest features (Q4 2025 → Q1 2026)
- **Jan 15 2026 update — Ultra-long context RL:**
  - **gpt-oss QLoRA at 380K context** on a single 192GB B200.
  - **Qwen3-8B GRPO at 110K context** on an 80GB H100.
  - New batching algorithms → 7× longer context (often 12×) with no accuracy or speed regression.
- **gpt-oss RL support:** 3× faster inference, 50% less VRAM, 8× longer context for gpt-oss specifically.
- **Qwen3-VL-8B GSPO/GRPO on free Colab T4** — the "vision-RL-on-Colab" flex.
- **GSPO (Group Sequence PO)** — Alibaba Qwen's sequence-level variant. Set `loss_type='gspo'`.
- **Vision RL (VLM RL)** guide for multimodal tasks.
- **DPO/ORPO/KTO** preference optimization also supported.

### Killer integration points
- **↔ TRL:** `from unsloth import FastLanguageModel` before `from trl import ...` — patches TRL silently.
- **↔ vLLM:** `fast_inference=True` enables shared weight memory between vLLM (for GRPO rollouts) and training.
- **↔ HF Hub:** `model.push_to_hub_merged(...)` — pushes LoRA merged into the base checkpoint.
- **↔ Colab:** Unsloth's notebooks are literally designed to fit on a free T4 (16GB). This is where 95% of hackathon submissions will train.

### Gotchas
- **Import order matters:** `from unsloth import FastLanguageModel` MUST come before any transformers/trl imports or patching fails silently.
- **`fast_inference=True` is vLLM-dependent** — only for vLLM-supported models. If unsupported, set `False` or model loader crashes.
- **4-bit + LoRA is the sweet spot** — LoRA 16-bit uses 4× more VRAM than QLoRA 4-bit.
- **Minimum 300 GRPO steps before rewards move** (often 1000+). Teams that train for 50 steps and demo "it's not learning" are mis-reading the signal.
- **500 rows dataset is optimal; works with 10+** — do not over-engineer curriculum at scale.
- **Unsloth is GPL-licensed.** If your submission needs a permissive license for judges, check the README.

### Specific APIs
```python
from unsloth import FastLanguageModel
from trl import GRPOTrainer, GRPOConfig

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-1.7B-Instruct",
    max_seq_length=4096,
    load_in_4bit=True,
    fast_inference=True,              # vLLM shared memory
    gpu_memory_utilization=0.6,
)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
    lora_alpha=16,
    use_gradient_checkpointing="unsloth",  # async system RAM offload
)

trainer = GRPOTrainer(model=model, tokenizer=tokenizer, ...)
trainer.train()
model.save_lora("my_lora")
model.push_to_hub_merged("me/qwen3-grpo-wordle", tokenizer, save_method="merged_16bit")
```

### Depth-of-help ceiling
Takes you from "free Colab T4 can't even load a 4B model" → "train a 8B with 110K ctx GRPO on one H100." Ceiling: does NOT do multi-GPU DDP/FSDP training at scale — use Torchforge for that. Also tied to supported model families (Llama/Qwen/Gemma/Phi/Mistral/gpt-oss/DeepSeek-R1-Qwen); exotic archs not supported.

---

## Tool 4: PyTorch (+ PyTorch Foundation)

**Elevator:** The native ML framework underlying everything on this stack — Meta's flagship, and the *reason* the hackathon judging is biased toward PyTorch-native solutions.

### What it does at each layer
- **Tensor + autograd** core (nothing new to explain here).
- **`torch.compile`** — Unsloth, vLLM, TRL all depend on this for 2–3× speedups.
- **DTensor + DeviceMesh** — distributed tensors that Torchforge's TorchStore uses for resharding.
- **FSDP2** — fully sharded data parallel, the path to training 70B+ with Torchforge/TorchTitan.
- **`torch.export`** — ahead-of-time compile for deployment.

### Latest features (relevant for 2026 hackathon)
- **PyTorch 2.9** (Oct 2025) — required minimum for Torchforge + Monarch.
- **vLLM 0.7+** integration finalized — required by TRL for colocate mode.
- **Meta's Monarch** (PyTorch-native distributed coordination) — open-sourced Oct 2025.

### Integration points
- Everything here is built on PyTorch. Specifically, TRL *requires* `transformers>=5.2.0` which requires `torch>=2.5`.

### Gotchas
- **Don't pin torch below 2.5.** TRL v1.2 will silently fall back and break env_factory.
- **CUDA mismatch:** Colab's CUDA version shifts; use `torch==X.Y.Z+cuXXX` form.

### Depth-of-help ceiling
Foundation layer. If you write custom CUDA ops, you're in it. Otherwise it's transparent infrastructure.

---

## Tool 5: HuggingFace Hub / Spaces / Datasets

**Elevator:** The tripod of deployment — Spaces host your env server, Models host your trained checkpoint, Datasets host your curriculum.

### What it does at each layer
- **Spaces** = Docker container runtime with auto-generated URL, public pip-install path, ZeroGPU option. Your OpenEnv env lives here.
- **Models** = Git LFS repos for model weights. Your trained checkpoint lives here with a Model Card.
- **Datasets** = Parquet/CSV/JSON on Hub. Your curriculum + eval data lives here, accessible via `datasets.load_dataset("me/my_curriculum")`.
- **Collections** = curated grouping that the OpenEnv catalog uses.
- **Jobs (new 2025 Q4)** = `hf jobs run --script ...` cloud-executes a script on rented GPUs.
- **Inference Providers** = serverless inference routing (for eval, not training).

### Latest features (Q4 2025 → Q1 2026)
- **ZeroGPU on H200** — free-tier now gets NVIDIA H200 slices (~70GB VRAM) dynamically allocated. This is the single biggest quality-of-life change in 2026.
- **PRO at $9/mo** includes 8× ZeroGPU quota = 25 min H200/day, 10× private storage (1TB), 2M Inference Provider credits, up to 10 ZeroGPU Spaces with Dev Mode (SSH/VS Code).
- **Pay-as-you-go GPU credits:** $1 per 10 min H200 beyond quota.
- **Spaces Dev Mode:** SSH/VS Code into running Space (PRO).
- **HF Jobs** — `uv run ...` + PEP 723 inline deps + cloud execution.

### Integration points
- **↔ OpenEnv:** `openenv push` = `git push` to Space with Docker SDK.
- **↔ TRL:** `GRPOTrainer(..., push_to_hub=True)` writes checkpoint to Models.
- **↔ smolagents:** agents can be shared via Hub.

### Gotchas
- **Free Spaces have CPU by default** — you need to explicitly enable ZeroGPU or upgrade tier.
- **Space sleep:** free tier sleeps after 48h idle. Judges opening your Space will get a cold start (~30–90s). Pre-warm before demo.
- **Concurrency on free Spaces is LIMITED.** 1 WebSocket = 1 user. Training will starve. Duplicate to your account + upgrade.
- **`registry.hf.space/<namespace>-<space>:latest`** is the Docker image format — note the dash not slash.
- **Dataset cards are LLM-screened.** Judging is partly automated; missing YAML frontmatter = potential filter.

### Specific APIs
```bash
hf login
hf upload me/my_lora ./output_dir --repo-type model
hf upload me/my_curriculum ./data.parquet --repo-type dataset
hf download openenv/echo_env --repo-type=space --local-dir=echo_env
hf jobs run --flavor a10g-small --script train.py

# Space Docker image
docker pull registry.hf.space/me-my_env:latest
```

```python
from datasets import load_dataset
ds = load_dataset("me/my_curriculum", split="train")
```

### Depth-of-help ceiling
Takes you from "I have a dataset/env/model" to "anyone in the world can `pip install git+https://...`." Ceiling: not a training harness, not a reward framework. And free-tier Spaces are too constrained for training — use for *serving* only.

---

## Tool 6: Docker + FastAPI (OpenEnv server runtime)

**Elevator:** The execution sandbox in which your env server actually runs; OpenEnv generates a `Dockerfile` + FastAPI app that together become the thing an agent talks to.

### What it does
- **FastAPI** — OpenEnv's `create_app(...)` emits a FastAPI app with endpoints: `POST /reset`, `POST /step`, `GET /state`, `GET /health`, `GET /web/` (Gradio UI), `WS /ws`.
- **Uvicorn** — the ASGI server hosting FastAPI.
- **Docker** — isolates the env: no egress (configurable), fixed CPU/RAM, reproducible build.

### Latest features
- OpenEnv v0.2.3's Gradio-backed `/web/` path handling (409 before reset, redirect `/` → `/web/`).
- FastMCP 2.x/3.x integration in v0.2.2+.

### Gotchas
- **`--platform linux/amd64`** is mandatory for Mac judges.
- **WebSocket vs HTTP:** some HF Spaces proxies drop idle WS connections after 60s. Set a heartbeat.
- **Container escape risk:** smolagents recommends additional sandboxing (E2B/Modal/Pyodide) for untrusted code in `coding_env` use cases.

### APIs
```bash
docker build -t my_env .
docker run -d -p 8001:8000 --platform linux/amd64 my_env
curl http://localhost:8001/health
```

### Depth-of-help ceiling
Container = containment. Beyond reliability + isolation, it doesn't help with training, rewards, or scaling.

---

## Tool 7: Torchforge (meta-pytorch/torchforge)

**Elevator:** Meta's PyTorch-native, actor-based, async-first RL library (October 2025) for scalable post-training; experimental but the *PyTorch-blessed* path.

### What it does at each layer
- **Services layer (on Monarch):** Distributed actor replicas with automatic load balancing + fault tolerance. `.as_service()` wraps an actor class.
- **Service adverbs:**
  - `.route()` — load-balanced single-replica call.
  - `.fanout()` — broadcast to all replicas.
  - `.session()` — **sticky session for KV-cache reuse** (NEW, barely documented).
- **TorchStore:** Distributed in-memory KV store with DTensor APIs, RDMA transfers, cross-topology resharding. Weight sync without GPU blocking.
- **Monarch:** Single-controller distributed coordination (vs SPMD complexity).
- **Apps:** `apps/sft/main` (SFT), `apps/grpo/main` (GRPO), `apps/blackjack/main` (env GRPO demo).

### Latest features (Q4 2025 → Q1 2026)
- **Announced Oct 2025** by PyTorch team. Still "experimental, expect breaking changes."
- **Together AI demo:** Qwen 1.5B BlackJack GRPO on Together Instant Clusters.
- **TorchStore** with DTensor-based async weight syncing.
- **Any-degree-of-async:** same code scales from sync PPO to fully async off-policy.

### Killer integration points
- **↔ OpenEnv:** `apps/grpo/main` has an OpenEnv-integrated reference (e.g., grpo_blackjack).
- **↔ TorchTitan:** underlying trainer for 70B+ scale. Forge + Titan + vLLM = Meta's internal stack.
- **↔ Together AI / Coreweave:** validated on 512× H100 + Instant Clusters.

### Gotchas
- **"Experimental"** is not just a disclaimer — APIs *will* change. Pin git commit hash.
- **Minimum 2 GPUs for GRPO.** Won't run on Colab free T4.
- **Monarch requires PyTorch 2.9.0+.**
- **ROCm path is separate** (`install_rocm.sh`).

### Specific APIs
```python
# Actor service
policy = PolicyActor.options(
    hosts=1, procs=8, with_gpus=True, num_replicas=16
).as_service()

# Adverbs
response = await policy.generate.route(prompt)            # load-balanced
await policy.update_weights.fanout(new_version)           # broadcast
async with policy.session() as sess:                      # sticky KV
    out = await sess.generate.route(prompt)

# TorchStore
import torchstore as ts
await ts.put("weights_v1", dtensor)
reshard = await ts.get("weights_v1", target_layout_dtensor)
```

```bash
conda create -n forge python=3.12 && conda activate forge
./scripts/install.sh
python -m apps.grpo.main --config apps/grpo/qwen3_1_7b.yaml
```

### Depth-of-help ceiling
Massive async-scale training on many GPUs. For a 1-Colab hackathon submission it's overkill; **however**, *mentioning it in the pitch* and showing a torchforge-compatible config file is a huge "pitch differentiator" signal because judges from Meta will recognize it. Real training ceiling: limited by experimental status — stuff will break under you.

---

## Tool 8: Google Colab

**Elevator:** The default GPU notebook everyone uses; $200/mo credits mentioned in the hackathon email.

### 2026 tier structure
- **Free:** T4 (16GB), time-limited sessions, CPU fallback. ~1.76 CU/hr.
- **Pro ($9.99/mo):** ~100 CU, L4/A100 access, longer sessions. A100 ~15 CU/hr → ~7 hrs/100 CU.
- **Pro+ ($49.99/mo):** background exec, priority queue, more CUs.
- **Pay-as-you-go:** $9.99 per 100 CU. ~57 hrs T4 or ~7 hrs A100 per $10.
- **Colab Enterprise (GCP-backed):** custom pricing, H100 available.

### What $200 credits actually buys you
- **T4 (16GB):** ~114 hrs = ~4.7 days continuous. Plenty for Unsloth 1.5B–3B GRPO.
- **L4 (24GB):** ~80 hrs. The sweet spot — 2× T4 memory, close to A100 speed on LoRA.
- **A100 (40GB):** ~14 hrs. Enough for a serious 7B GRPO run or a long gpt-oss demo.
- **H100 (80GB, Enterprise only):** ~6 hrs for a serious reasoning eval.

### Gotchas
- **Compute units expire.** Don't hoard.
- **Disconnects:** free tier disconnects after ~12 hrs regardless of activity. Pro+ has background exec.
- **Disk:** 100GB local, not persistent. Mount Drive or checkpoint to HF Hub every 50 steps.
- **CUDA version drift:** Colab sometimes upgrades CUDA mid-quarter breaking pinned wheels. Re-run `!pip install` at session start.
- **vLLM on T4 is a pain.** Unsloth's `fast_inference=True` works; raw vLLM often doesn't fit.

### Specific commands
```python
# Colab setup block (must-have)
!pip install -q -U "trl[openenv]==1.2.0" "transformers>=5.2.0" \
    "openenv-core>=0.2.3" "unsloth" "vllm>=0.7.3" wandb
!pip install -q "openenv-textarena @ git+https://huggingface.co/spaces/openenv/wordle"

from google.colab import userdata
import os
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
os.environ["WANDB_API_KEY"] = userdata.get("WANDB_API_KEY")
```

### Depth-of-help ceiling
Gets you from nothing to a running GRPO loop. Ceiling: disconnects kill long runs, single-GPU only, no SSH (unlike HF Spaces Dev Mode on PRO). For multi-GPU scale use HF Jobs or Together AI.

---

## Tool 9: Weights & Biases (W&B)

**Elevator:** The experiment tracker that makes GRPO reward curves beautiful for a pitch deck.

### What it does at each layer
- **Run tracking:** losses, rewards, KL, per-reward-function breakdowns.
- **Rich media:** `log_completions=True` in GRPOConfig logs completions as HTML tables per step — judges can scroll through model outputs.
- **Sweeps:** hyperparameter search with GPU scheduling.
- **Reports:** shareable read-only dashboards — this is what you embed in your Devpost submission.
- **Artifacts:** model / dataset versioning.

### Latest features (Q4 2025 → Q1 2026)
- **Dedicated GRPO dashboard templates** (via `wandb.integration.trl`).
- **Weave** — W&B's LLM observability layer, can trace env interactions end-to-end per episode.
- **Reports v3** — interactive reports with live-updating charts, publishable to a URL.

### Integration points
- **↔ TRL:** `GRPOConfig(report_to="wandb", log_completions=True)` — one line.
- **↔ HF Hub:** W&B run URL can be added to Model Card.
- **↔ Devpost demo:** embed live W&B report URL in your submission — judges see *real-time* training.

### Gotchas
- **`reward` metric is unweighted sum** (TRL issue #5352, Mar 2026) even if `reward_weights` are non-uniform. Model trains correctly but chart is misleading. Log your own weighted metric manually.
- **Free tier:** 100GB artifact storage — plenty for a hackathon.
- **Entity scoping:** if you log under a personal entity vs team, URL structure differs; agree with teammates upfront.

### Specific APIs
```python
import wandb
wandb.init(project="openenv-hackathon",
           name="qwen3-wordle-grpo",
           config={"model": "Qwen/Qwen3-1.7B", "env": "wordle"})

# In GRPOConfig:
report_to="wandb"
log_completions=True
run_name="qwen3-wordle-grpo"

# Log custom reward components
wandb.log({"reward_weighted": w_r * r for r in ...})
```

### Depth-of-help ceiling
Tracking and presentation. Doesn't touch training logic. Ceiling: if you need evaluation-sets-vs-model matrix comparisons, W&B Tables are good but eventually you'll roll your own Streamlit dashboard.

---

## Tool 10: smolagents

**Elevator:** HuggingFace's minimalist "code-writing agent" library (~1000 LOC) — agents that emit Python actions rather than JSON tool calls.

### What it does at each layer
- **Agent loop:** `CodeAgent` generates Python code → executes in sandbox → captures output → loops.
- **Sandbox layer:** Executes code via Blaxel, E2B, Modal, Docker, or Pyodide+Deno WebAssembly.
- **Tool layer:** Tools are Python functions auto-introspected; shared via Hub.
- **Model-agnostic:** transformers, ollama, OpenAI, Anthropic, LiteLLM.

### Latest features (Q4 2025 → Q1 2026)
- **Pyodide+Deno WASM sandbox** — no Docker needed, runs in-browser/WASM.
- **Full Hub integration** for sharing agents.
- **Production-grade first-class OpenAI/Anthropic support** via LiteLLM.

### Integration points
- **↔ OpenEnv's `coding_env`:** smolagents is the sandbox providing persistent Python context, stdout/stderr/exit capture, detailed error handling.
- **↔ TRL:** smolagents agent can be the *thing* you train; wrap it in an env class with `.run()` as a tool method.
- **↔ HF Hub:** `agent.push_to_hub("me/my-agent")`.

### Gotchas
- **Sandbox choice matters for screener:** Pyodide = lightest, E2B = best isolation, Docker = mid. Pick one and pin.
- **Code agents can hang** if they write infinite loops. Set `max_steps` and kill switches.

### Specific APIs
```python
from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),
    executor_type="e2b",   # or "docker", "pyodide"
    max_steps=10,
)
result = agent.run("Find top 3 earthquakes in the past week.")
```

### Depth-of-help ceiling
Great for the "agent that writes Python" use case, especially in `coding_env`-style problems. Ceiling: not optimized for multi-agent orchestration (use LangGraph or OpenClaw for that) and its sandbox is not production-hardened.

---

## Tool 11: MCP (Model Context Protocol) in OpenEnv

**Elevator:** Anthropic's open standard for LLM↔external-tool interop, now native to OpenEnv via RFC 003 and RFC 004 (`MCPEnvironment`).

### What it does at each layer (in OpenEnv context)
- **Discovery:** `ListToolsAction` maps to MCP `tools/list` JSON-RPC.
- **Invocation:** `CallToolAction(tool_name, parameters)` maps to MCP `tools/call`.
- **Primitives:** Resources (GET-like data), Tools (POST-like ops), Prompts (reusable templates).
- **Transport:** FastMCP 2.x/3.x (HTTP + SSE or WebSocket).
- **Modes in OpenEnv v0.2.2:** *production mode* (real MCP server) + *simulation mode* (replayed traces for reproducible eval) + *code mode* (CodeAct execution).

### Latest features
- **RFC 003 (Feb 2026):** MCPEnvironment class, ListTools/CallTool actions, JSON-RPC marshaling, local server bypass for perf, composite parent→child delegation.
- **RFC 004 (In Review, 2026-04):** "Actions as tool calls" — make your env's native actions *be* MCP tool calls. Zero translation overhead. Better introspection for training.

### Killer integration points
- **↔ Any MCP server:** Your env can pull in Slack, GitHub, Filesystem, Puppeteer, etc. MCP servers.
- **↔ TRL:** `environment_factory` + MCP-backed env = model learns to call any MCP tool.
- **↔ Claude Code / OpenClaw (RFC 005):** your env's actions callable by any MCP client.
- **↔ smolagents:** smolagents can invoke MCP tools directly.

### Gotchas
- **FastMCP version pinning:** 2.x vs 3.x semantics differ on tool schema. Pin explicitly.
- **JSON-RPC marshaling overhead** unless you use local-server bypass.
- **Reserved-name validation:** certain tool names (e.g., `reset`, `step`) collide with OpenEnv internals — v0.2.2 validates this at server start.

### Specific APIs
```python
from openenv.mcp import MCPEnvironment, ListToolsAction, CallToolAction

env = MCPEnvironment(
    mcp_server_urls=["http://localhost:3333", "http://localhost:3334"],
    mode="production",   # or "simulation" or "code"
)
env.reset()
tools = env.step(ListToolsAction()).observation.metadata["tools"]
result = env.step(CallToolAction(
    tool_name="github.search_repos",
    parameters={"query": "pytorch grpo"},
)).observation.metadata["result"]
```

### Depth-of-help ceiling
Massive — MCP is *the* emerging standard. Ceiling: MCP ecosystem is new so many servers are buggy. For the hackathon, prefer first-party MCP servers (Anthropic's filesystem/github/puppeteer).

---

## Integration recipe — end-to-end submission

Here is the recipe that plugs everything together; the "one Colab cell to rule them all":

```python
# === 1. Install (Colab, first cell) ===
!pip install -q -U "trl==1.2.0" "transformers>=5.2.0" "openenv-core>=0.2.3" \
    "unsloth" "vllm>=0.7.3" wandb datasets
!pip install -q "openenv-<yourenv> @ git+https://huggingface.co/spaces/<you>/<yourenv>"

# === 2. Auth ===
import os
from google.colab import userdata
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
os.environ["WANDB_API_KEY"] = userdata.get("WANDB_API_KEY")

# === 3. Unsloth-patched model (MUST be first) ===
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-1.7B-Instruct",
    max_seq_length=4096,
    load_in_4bit=True,
    fast_inference=True,
)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    use_gradient_checkpointing="unsloth")

# === 4. Env (your innovation here) ===
from your_env import YourEnvClient, YourAction

class YourToolEnv:
    def __init__(self):
        self.client = YourEnvClient(base_url="https://<you>-<yourenv>.hf.space")
        self.reward = 0.0

    def reset(self, **kwargs) -> str:
        self.reward = 0.0
        return self.client.reset().observation.initial_prompt

    def act(self, move: str) -> str:
        """Make a move.
        Args:
            move: the move to perform
        Returns: result description
        """
        res = self.client.step(YourAction(move=move))
        self.reward = res.reward
        return res.observation.description

# === 5. Reward + curriculum dataset ===
from datasets import load_dataset
ds = load_dataset("me/curriculum", split="train")   # Tool 5: Datasets

def reward_func(environments, **kwargs):
    return [env.reward for env in environments]

# === 6. Train ===
from trl import GRPOTrainer, GRPOConfig
trainer = GRPOTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=ds,
    reward_funcs=[reward_func],
    args=GRPOConfig(
        use_vllm=True, vllm_mode="colocate",
        num_generations=4, gradient_accumulation_steps=16,
        max_completion_length=4096,
        report_to="wandb", log_completions=True,
        push_to_hub=True, hub_model_id="me/qwen3-your-env",
        loss_type="gspo",
    ),
    environment_factory=YourToolEnv,
)
trainer.train()
model.push_to_hub_merged("me/qwen3-your-env-merged", tokenizer)
```

**Dependency order of operations:**
1. Write env → `openenv push` → Space live.
2. Duplicate the Space to your account (for concurrency).
3. Colab: install, auth.
4. Unsloth load model.
5. Wrap env in TRL-compatible class.
6. Train w/ W&B logging.
7. Push model to Hub.
8. Make a W&B Report URL.
9. Link everything in Devpost.

---

## Pitch differentiator features (things 95% of other teams won't use)

1. **Multi-environment GRPO training** (TRL v1.2 `environment_factory` + per-env reward masking with `None` returns). Train one model on Wordle + Sudoku + Your-Env simultaneously and show differential skill curves. Nobody's shipping this yet — it was documented publicly the same week as the hackathon email.

2. **MCPEnvironment with mode=simulation** (OpenEnv v0.2.2). Use *simulation* mode to replay deterministic MCP traces during eval — gives judges reproducible metrics. Pair with production mode for training.

3. **Rubrics (RFC 004) as reward source.** Ship a rubric config that uses an LLM-as-judge for reward with delayed signals instead of hand-written reward funcs. Almost no team will do this.

4. **Torchforge config file, even if you don't train on it.** Commit a `forge.yaml` and show a diagram of how your env scales to Monarch actors. Meta judges *will* notice.

5. **AsyncGRPOTrainer + chunked LM head (TRL v1.1).** 44× peak memory reduction. Lets you train 7B on an A100 where other teams are stuck at 3B.

6. **Unsloth long-context (Jan 2026).** Qwen3-8B GRPO at 110K context on one H100 — if your env benefits from long horizons (e.g., multi-step reasoning), this is the moat.

7. **RFC 005 agentic harness integration.** Make your env a *skill* that Claude Code or OpenClaw can invoke. The "meta" angle: your env improves *coding agents*.

8. **SSDTrainer (TRL v1.2) for self-improvement.** No reward model needed — model distills its own high-quality samples. Pairs beautifully with a "self-improving multi-agent env" narrative.

9. **HF Jobs for cloud training.** `uv run examples/scripts/openenv/<yours>.py` with PEP 723 inline deps → one command cloud-trains on HF's GPUs. Demo-friendly.

10. **GenericEnvClient for universal eval.** Use `GenericEnvClient` / `GenericAction` to eval your trained model against ANY OpenEnv env on the Hub without installing their code — flex "universal generalization."

---

## Gotchas that break the LLM screener (consolidated)

The hackathon has an automated LLM screener gate before human judging. These are the things that will kill you there:

1. **Docker `--platform linux/amd64` missing** → Space doesn't build on judge's Mac.
2. **`max_concurrent_envs=1`** (default) → training hangs, reward is 0, screener sees dead run.
3. **Tool method missing `Args:` docstring** → TRL builds broken tool schema, model never calls the tool, reward stays 0.
4. **`environment_factory=MyEnv()`** (passed as instance not class) → single-rollout stuck, reward flat.
5. **`max_completion_length=512`** on multi-turn env → episodes cut mid-game.
6. **`num_generations` doesn't divide batch_size × grad_accum** → GRPO crash.
7. **Using a shared community Space** → concurrency throttle, silent stall.
8. **`transformers<5.2.0`** → `environment_factory` silently ignored.
9. **Missing Model Card / Dataset Card YAML frontmatter** → LLM screener may flag as "incomplete."
10. **Unsloth imported AFTER transformers** → monkey-patch fails, slow training, OOM.
11. **Free Space sleep** → judge clicks your demo link, cold start, first call 404s.
12. **GRPO run <300 steps** → rewards don't move, looks like "model not learning."
13. **Chat template missing `{% generation %}` markers** → assistant-only loss broken (v1.1 auto-patches, but only for SFT — GRPO does not).
14. **Port 8000 collision** between vLLM and env — map env to 8001.
15. **No duplicate of env Space for training** — training will compete with public demo traffic.

---

## Recommended integration pattern for a Multi-Agent + Self-Improvement env

Since the prior research pointed at multi-agent + self-improvement as a winning category, here's the *canonical* stack:

```
┌──────────────────────────────────────────────────────────┐
│  Devpost submission page                                  │
│  ├─ Links to: Space, Model, Dataset, W&B Report, Colab   │
│  └─ Embedded video demo                                   │
└──────────────────────────────────────────────────────────┘
                       ▲
┌──────────────────────┼───────────────────────────────────┐
│           Hugging Face Hub (Tool 5)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│  │ Space       │  │ Model       │  │ Dataset          │  │
│  │ (env server)│  │ (GRPO ckpt) │  │ (curriculum)     │  │
│  │ FastAPI+    │  │ LoRA merged │  │ multi-agent      │  │
│  │ Docker      │  │ via Unsloth │  │ scenarios        │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘   │
└───────▲─────────────────▲─────────────────▲──────────────┘
        │ WebSocket       │ push_to_hub     │ load_dataset
        │ (OpenEnv)       │ (Unsloth)       │ (Datasets)
        │                 │                 │
┌───────┼─────────────────┼─────────────────┼──────────────┐
│       │   Colab / HF Jobs / Together AI (Tool 8)        │
│   ┌───┴───┐    ┌────────┴────────┐   ┌───────┴────┐     │
│   │OpenEnv│───▶│  TRL v1.2       │◀──│ Dataset    │     │
│   │ env   │    │  GRPOTrainer    │   │ curriculum │     │
│   │ client│    │  env_factory=   │   └────────────┘     │
│   └───┬───┘    │  MultiEnvClass  │                      │
│       │        │                 │                      │
│       │        │  Unsloth patch  │───▶ W&B (Tool 9)     │
│       │        │  + GSPO loss    │     log_completions  │
│       │        │  + SSDTrainer   │     Report URL       │
│       │        │  (self-improve) │                      │
│       │        └────────┬────────┘                      │
│       │                 │                               │
│       │                 ▼                               │
│       │        Merged Qwen3-1.7B/8B LoRA                │
│       │                                                  │
│       └─▶ MCPEnvironment (RFC 003/004)                   │
│            ├─ mode="production" for training             │
│            └─ mode="simulation" for reproducible eval    │
└──────────────────────────────────────────────────────────┘
```

**Multi-agent angle:** Build a `MultiAgentEnv` where multiple agent instances (could be the SAME model at different temperatures, or specialist LoRA adapters) interact. Each agent gets its own set of tool methods. Reward is emergent from their interaction — e.g., a debate scoring game, a coordination puzzle, a trade simulation.

**Self-improvement angle:** Use SSDTrainer (v1.2) so model *distills from its own high-reward trajectories*. After N steps, use the just-trained model as the new teacher. Combined with Unsloth's long-context RL, you can demo: "our model learns from itself without a reward model" — a huge narrative win.

**Key implementation files to write:**
- `envs/my_env/src/envs/my_env/server/app.py` — FastAPI app with `create_app(..., max_concurrent_envs=64)`.
- `envs/my_env/src/envs/my_env/environment.py` — the `Environment` subclass.
- `envs/my_env/src/envs/my_env/models.py` — Pydantic `Action`/`Observation`.
- `train.py` — the Colab cell above, with `MultiEnvClass` + SSDTrainer.
- `README.md` — with `--platform linux/amd64` docker command front and center.
- `rubric.yaml` — LLM-as-judge reward config (RFC 004).
- `wandb_report_url.md` — pin to top of README.

---

## Quick reference: "what version of everything do I pin?"

```
torch >= 2.9.0
transformers >= 5.2.0             # required for environment_factory
trl == 1.2.0                      # pin exactly; experimental API
openenv-core >= 0.2.3
unsloth (latest)
vllm >= 0.7.3
datasets (latest)
wandb (latest)
fastmcp >= 3.0                    # for MCPEnvironment
smolagents (latest)               # if using coding_env
```

---

## Sources

- [OpenEnv Releases (GitHub)](https://github.com/meta-pytorch/OpenEnv/releases)
- [OpenEnv RFC 003: MCP Support](https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/003-mcp-support.md)
- [OpenEnv RFC 004: Actions as Tool Calls](https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/004-actions-as-tool-calls.md)
- [OpenEnv README](https://github.com/meta-pytorch/OpenEnv/blob/main/README.md)
- [TRL Releases (GitHub)](https://github.com/huggingface/trl/releases)
- [TRL OpenEnv Integration Docs](https://huggingface.co/docs/trl/openenv)
- [TRL GRPO Trainer Docs](https://huggingface.co/docs/trl/grpo_trainer)
- [Unsloth RL Guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide)
- [Unsloth GRPO Long Context](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/grpo-long-context)
- [Unsloth gpt-oss RL](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning)
- [Introducing Torchforge (PyTorch Blog)](https://pytorch.org/blog/introducing-torchforge/)
- [Torchforge GitHub](https://github.com/meta-pytorch/torchforge)
- [HuggingFace Pricing](https://huggingface.co/pricing)
- [HuggingFace ZeroGPU Docs](https://huggingface.co/docs/hub/en/spaces-zerogpu)
- [Google Colab Pricing](https://cloud.google.com/colab/pricing)
- [smolagents GitHub](https://github.com/huggingface/smolagents)
- [Building the Open Agent Ecosystem (HF Blog)](https://huggingface.co/blog/openenv)
- [TRL GRPO+WandB Issue #5352](https://github.com/huggingface/trl/issues/5352)
