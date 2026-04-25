# OpenEnv Ecosystem & Trending Agent Envs

Research date: 2026-04-20. Target event: Meta PyTorch OpenEnv Hackathon Grand Finale, Bangalore, Apr 25-26 2026.

---

## OpenEnv Core (what exists in the framework already)

**Repo:** https://github.com/meta-pytorch/OpenEnv
- Stars: ~1.6k | Forks: ~338 | Latest release: v0.2.3 (Mar 28 2026) | 1,425 commits on main | License: BSD-3
- Blog: https://huggingface.co/blog/openenv (Oct 2025 launch, Meta + HF)
- Docs site: https://meta-pytorch.org/OpenEnv/
- PyPI: `pip install openenv-core`
- HF org: https://huggingface.co/openenv

### Architecture idioms (what judges will expect)
- Gymnasium-style 3-method API: `reset()`, `step(action)`, `state()` returning `StepResult` (obs+reward+done)
- Client-server split: `EnvClient` (typed HTTP) talks to a FastAPI server inside Docker
- Every env ships: `models.py` (Action/Observation/State dataclasses), `client.py`, `server/environment.py`, `server/app.py`, `Dockerfile`, `openenv.yaml` manifest
- Dual sync+async ergonomics (`async with` + `.sync()` wrapper)
- Type safety end-to-end; `from_docker_image()` spins isolated containers
- `openenv push` deploys the container to HF Spaces

### Active RFCs (signals where framework is heading)
- RFC 001 - Core abstractions (Environment/Agent/Task): https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/001-abstractions.md
- RFC 002 - Env spec, packaging, isolation: https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/002-env-spec.md
- RFC 003 - MCP (Model Context Protocol) tool support (landed in v0.2.x)
- RFC 004 - Actions-as-tool-calls + delayed/trajectory rewards: https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/004-actions-as-tool-calls.md
- RFC 005 - Agentic harness integration
- Open: ORS (Open Reward Standard) issue #468 - community-standardized reward primitives
- Open: Community env submission ComtradeBench #527 - proof the project accepts external env PRs

---

## Example Envs Shipped with OpenEnv (29 in `envs/`)

Directory: https://github.com/meta-pytorch/OpenEnv/tree/main/envs

| Env | One-liner | Domain | Reward pattern |
|---|---|---|---|
| `echo_env` | Message-echo reference impl | Testing | `len(msg)*0.1` (trivial, pedagogical) |
| `coding_env` | Sandboxed Python exec via smolagents | Code | stdout/stderr/exit-code driven |
| `chat_env` | Token-ID stepping for LLM chat | LLM | Custom |
| `repl_env` | Interactive Python REPL control | Code | Task-dependent |
| `git_env` | Git ops in a sandbox | Code/SWE | Task-success |
| `chess_env` | Chess w/ configurable opponents | Game | Win/loss + shaping |
| `connect4_env` | Connect-4 | Game | Win/loss |
| `snake_env` | Snake | Game | Score delta |
| `openspiel_env` | Wraps DeepMind OpenSpiel catalog | Game | Game-specific |
| `textarena_env` | Wraps TextArena (Wordle, Sudoku, 74+ games) | Text games | TrueSkill/win |
| `atari_env` | Arcade Learning Environment | Game/classic-RL | Atari score |
| `reasoning_gym_env` | Procedural reasoning (count legs, chess eval, etc.) | Reasoning | 0-1 verifier, curriculum-weighted |
| `calendar_env` | Production-grade calendar tool use w/ ACLs | Tool-use | Workflow success (see Turing blog) |
| `browsergym_env` | MiniWoB/WebArena/WorkArena wrapped | Web | Dense (MiniWoB) + sparse (WebArena) |
| `openapp_env` | Generic app-control env | GUI/Tool-use | Task success |
| `websearch_env` | Web search tool harness | Tool-use | Task success |
| `finrl_env` | Financial markets / trading | Finance | PnL / Sharpe |
| `finqa_env` | Finance QA | Finance/QA | Verifier |
| `tbench2_env` | Wraps tau-bench 2 (tool-agent-user) | Tool-use dialog | tau-bench score |
| `grid_world_env` | Classical grid world | Classic RL | Distance/goal |
| `maze_env` | Maze navigation | Classic RL | Goal |
| `dm_control_env` | DeepMind control suite | Continuous control | Task reward |
| `unity_env` | Unity ML-Agents | Simulation | Custom |
| `carla_env` | CARLA driving sim | Autonomous driving | Custom |
| `sumo_rl_env` | Traffic-signal SUMO | Traffic | Throughput |
| `wildfire_env` | Wildfire simulation | Physical sim | Containment |
| `julia_env` | Julia code exec | Scientific code | Verifier |
| `kernrl` | GPU kernel writing | Perf code | Benchmark speedup |
| `dipg_safety_env` | Driver-in-the-loop safety | Safety | Safety metric |

### HF Spaces under `openenv/` (13 live)
https://huggingface.co/openenv - top likes:
- `coding-env` (13 likes), `echo-env` (6), `atari-env` (3), `openspiel-env` (3), `textarena-wordle` (1), `textarena-sudoku` (1), `repl-env` (1), plus `browsergym`, `chat`, `tb2`, `harfeast`, `vc_gemini`, `football-play-calling`.
- Datasets: 0. Models: 0. (Gap: no training datasets or RL-trained checkpoints published yet.)

---

## HF TRL + Custom Env Patterns (GRPO/PPO/DPO)

- Repo: https://github.com/huggingface/trl | 18.1k stars | v1.2.0 released Apr 17 2026
- GRPOTrainer: https://huggingface.co/docs/trl/main/en/grpo_trainer
- **Key API: `environment_factory`** - per-generation env instance, env must have `reset()` returning None or str (str appended to last user msg)
- Reference notebook wiring TRL GRPO + OpenEnv BrowserGym: https://github.com/huggingface/trl/blob/main/examples/notebooks/grpo_functiongemma_browsergym_openenv.ipynb (FunctionGemma + BrowserGym + OpenEnv)
- Modal GRPO+TRL coding-problem recipe: https://modal.com/docs/examples/grpo_trl
- DeepWiki overview of TRL-GRPO: https://deepwiki.com/huggingface/trl/5-group-relative-policy-optimization-(grpo)

## Unsloth Custom Training Patterns

- Repo: https://github.com/unslothai/unsloth
- Notebooks index: https://github.com/unslothai/notebooks (250+ notebooks)
- OpenEnv-integrated example in OpenEnv repo: `unsloth_2048.ipynb` (gpt-oss-20b GRPO training to beat 2048 on free Colab T4)
- Unsloth RL docs: https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide
- gpt-oss RL guide: https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning/tutorial-how-to-train-gpt-oss-with-rl
- Pattern: swap env + 3 reward heads (syntax/compile, anti-cheat/safety, task success) keeping the Unsloth+GRPO scaffold - this is the hackathon-friendly template.

---

## Adjacent Trending Envs (to understand the SOTA baseline)

| Project | GitHub | What | Why relevant |
|---|---|---|---|
| BrowserGym | https://github.com/ServiceNow/BrowserGym | Gym for web automation (MiniWoB, WebArena, VisualWebArena, WorkArena) | Already wrapped in OpenEnv - the web-agent baseline |
| WebArena | https://github.com/web-arena-x/webarena | 812 realistic web tasks (ecomm, forums, gitlab) | De-facto web benchmark |
| WebArena-Verified | https://github.com/ServiceNow/webarena-verified | Cleaned WebArena (Feb 2026 Docker images) | Preferred drop-in |
| OSWorld | https://os-world.github.io/ | 369 real desktop+web tasks | The "OS agent" north star |
| TextArena | https://github.com/LeonGuertler/TextArena | 74+ competitive text games, TrueSkill leaderboard | Already wrapped, rich multi-player RL |
| OpenSpiel | (DeepMind) | Game catalog | Already wrapped |
| AgentBench (ICLR'24) | https://github.com/THUDM/AgentBench | 8-env LLM-as-agent eval | Not yet in OpenEnv |
| tau-bench / tau2-bench | https://github.com/sierra-research/tau2-bench | Tool-agent-user dialog (retail, airline) | `tbench2_env` exists |
| Berkeley BFCL | https://gorilla.cs.berkeley.edu/leaderboard.html | Function-calling leaderboard | Not yet wrapped |
| SWE-Gym | https://github.com/SWE-Gym/SWE-Gym | 2438 SWE task instances (ICML'25), 32% SWE-Bench Verified | Not yet in OpenEnv - huge gap |
| SWE-smith | https://github.com/SWE-bench/SWE-smith | NeurIPS'25, scale SWE-agent data | Not wrapped |
| ALFWorld | (AgentQuest wrap) | Text household tasks | Classic, not wrapped |
| Reasoning-Gym | https://github.com/open-thought/reasoning-gym | NeurIPS'25 Spotlight procedural reasoning envs | Already wrapped |
| NVIDIA NeMo Gym | https://github.com/NVIDIA-NeMo/Gym | NVIDIA's competitor framework | Rival standard |
| axon-rl GEM | https://github.com/axon-rl/gem | Gym for agentic LLMs | Competitor |
| RAGEN / RAGEN-2 | https://github.com/RAGEN-AI/RAGEN | Stochastic-env LLM agent RL | Methods-paper |
| AgentGym-RL | https://github.com/WooooDyy/AgentGym-RL | Long-horizon multi-turn RL, beats o3/Gemini-2.5-Pro on 27 tasks | Methods+data |
| LlamaGym | https://github.com/KhoomeiK/LlamaGym | Fine-tune LLM agents online | Popular starter |
| AIO Sandbox (Mar 2026) | https://www.marktechpost.com/2026/03/29/... | Browser+shell+FS+MCP runtime | Could be wrapped as OpenEnv |

---

## Meta PyTorch Team's Public Signals about OpenEnv Direction

- Launch blog (Meta + HF, Oct 2025): https://huggingface.co/blog/openenv
- Practical evaluation blog (Calendar Gym tool use): https://huggingface.co/blog/openenv-turing
  - Finding: agents hit ~90% with explicit IDs, ~40% with NL descriptions; >50% of failures = malformed tool args. Implication: envs that test multi-step tool-arg correctness are valuable.
- InfoQ coverage: https://www.infoq.com/news/2025/11/hugging-face-openenv/
- Hackathon page: https://pytorch.org/event/openenv-ai-hackathon/ and https://www.scaler.com/school-of-technology/meta-pytorch-hackathon
- India Hackathon announcement (Tweet): https://x.com/PyTorch/status/2036276566372598162
- Explicit future work: Kubernetes provider, MCP tooling, ORS rewards, TorchForge integration, verl/SkyRL compat
- Ecosystem post (taxonomy, Mar 2026): https://leehanchung.github.io/blogs/2026/03/21/rl-environments-for-llm-agents/
- Industry framing: Turing, Scale, Patronus, Collinear, Semianalysis all have "RL environments" explainers (2026 is the year of env-as-a-product)

---

## What Domains are UNDER-REPRESENTED (our opportunity)

Looking at the 29 envs already shipped, the ORS/ComtradeBench signal, and adjacent trending work, these are clear gaps:

1. **Software engineering / PR-fixing** - no SWE-Gym/SWE-bench-style env in OpenEnv yet. `git_env` exists but is primitive. Wrapping SWE-Gym is high-impact.
2. **Healthcare / clinical / biomedical** - only `dipg_safety_env` (narrow). Clinical-decision, medication reconciliation, EHR-QA envs are absent.
3. **Legal / contract / compliance** - totally absent. Contract-redline, regulation-QA, due-diligence agents are a clean gap.
4. **Scientific research** - `julia_env` is code-only. No literature-review, experiment-design, lab-automation, or materials-science env.
5. **Multi-tool real SaaS tool-use** - `calendar_env` covers one API; no Slack/Gmail/Notion/Jira/Linear multi-tool workflows. tau-bench is synthetic.
6. **Cybersecurity / CTF / pentesting** - no CTF, no `terminal-bench`, no fuzzing/exploit env.
7. **Data engineering / SQL / analytics** - no Spider/BIRD-SQL or dbt/airflow-style env.
8. **ML engineering (MLAgentBench-style)** - no wrapped version. This is a known 9-task benchmark with prior expert trajectories.
9. **Robotics / embodied (beyond Unity+dm_control)** - no ManiSkill, RoboCasa, Habitat wrapper.
10. **Education / tutoring** - no Socratic-tutor env with student-model rollouts.
11. **Spreadsheet / Excel / Sheets reasoning** - major real-world workflow, absent.
12. **Mobile / Android agent (AndroidWorld, AppAgent)** - desktop is covered, mobile isn't.
13. **Negotiation / multi-agent markets** - `finrl_env` is single-agent. No bargaining/auction/game-theory env beyond OpenSpiel games.
14. **Creative (design, music, video editing)** - entirely absent.
15. **Translation / localization w/ style rubrics** - absent (LLM-judge reward is a good fit).

**Strongest "judge-pleasing" bets:** (a) SWE-Gym-style real bug-fixing env (plays to Meta FAIR's Code World Model story explicitly called out in launch blog), (b) multi-tool SaaS workflow env (builds on the Calendar-Gym Turing blog findings), (c) clinical/biomedical decision-support (huge societal angle, under-served), (d) mobile/AndroidWorld agent env (hot in 2025-26 research, no OpenEnv version).

---

## Reference Repos to Study (in priority order)

1. `envs/echo_env/` - minimal pattern, copy this skeleton. https://github.com/meta-pytorch/OpenEnv/tree/main/envs/echo_env
2. `envs/coding_env/` - external-tool (smolagents) integration. https://github.com/meta-pytorch/OpenEnv/tree/main/envs/coding_env
3. `envs/reasoning_gym_env/` - curriculum + verifiable reward pattern.
4. `envs/browsergym_env/` - wrapping an existing gym.
5. `envs/calendar_env/` - production-grade ACL + realistic tool use (the blog reference impl).
6. `examples/grpo_blackjack/` - end-to-end torchforge+GRPO example.
7. `unsloth_2048.ipynb` in OpenEnv repo - Unsloth+GRPO scaffolding to clone.
8. TRL notebook `grpo_functiongemma_browsergym_openenv.ipynb` - OpenEnv+TRL GRPO template.
9. Tutorial: https://github.com/meta-pytorch/OpenEnv/blob/main/tutorial/README.md
10. DeepWiki deep-dive: https://deepwiki.com/meta-pytorch/OpenEnv

---

## Key Sources

- https://github.com/meta-pytorch/OpenEnv
- https://huggingface.co/openenv
- https://huggingface.co/blog/openenv
- https://huggingface.co/blog/openenv-turing
- https://meta-pytorch.org/OpenEnv/
- https://github.com/huggingface/trl
- https://github.com/huggingface/trl/blob/main/examples/notebooks/grpo_functiongemma_browsergym_openenv.ipynb
- https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide
- https://pytorch.org/event/openenv-ai-hackathon/
- https://leehanchung.github.io/blogs/2026/03/21/rl-environments-for-llm-agents/
