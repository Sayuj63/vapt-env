# Public Hackathon Platform Winners (AI Agents)

_Research compiled April 2026 for Meta PyTorch OpenEnv Hackathon Grand Finale (Bangalore, Apr 25-26 2026)._
_Round 2 themes: Multi-Agent Interactions, Long-Horizon Planning, World Modeling, Self-Improvement, Wild Card._
_Judging: 40% Innovation, 30% Storytelling, 20% Reward Improvement, 10% Pipeline._

---

## What Wins on Public Platforms (Executive Summary)

Across DevPost, Devfolio, MLH, lablab.ai, and adjacent platforms in 2025–2026, a reproducible pattern emerges for which AI-agent projects take home top prizes:

1. **Story beats novelty.** Nearly every grand-prize winner (EcoLafaek, Edu.AI, DreamOps, RiskWise, Province) opens with a concrete, emotionally legible pain point — waste in Timor-Leste, Brazilian education inequity, 3 AM on-call debugging, supply chain shocks, IRS Form 1040. The model is always a means; the problem is the hook.
2. **Multi-agent architectures are now table stakes.** A single-agent chatbot is almost never a winner in 2025-26. Winners compose 3-7 specialized agents (planner / researcher / verifier / executor) with a coordinator. Judges reward visible role separation.
3. **Polished 3-minute demo video.** DevPost data shows winners spend ~30% of their effort on video storytelling. Vertical narrative (problem → agent reasoning trace → outcome) dominates. Screen-recorded "thinking" traces convert well.
4. **Production-grade plumbing wins tiebreakers.** AgentCore, ADK, Semantic Kernel, LangGraph, MCP — use of sponsor infrastructure correctly and creatively is how you leap from top 50 to top 3.
5. **Quantifiable metric improvement.** Winners report numbers: "30-60 min → 2-5 min debug time" (DreamOps), "100% accuracy on Form 1040" (Province), "~24% on ARC-AGI-2" (NVARC). This directly maps to OpenEnv's "Reward Improvement" criterion.
6. **Training vs. prompting is rare but wins heavily when present.** Most DevPost winners just call APIs. The minority who actually fine-tune (NVARC, DAMCS, Tiny Recursive Model) win research-credibility prizes disproportionately. OpenEnv hackathon's training mandate is a defensible moat.
7. **Personal / indie-feeling projects beat enterprise demos** on lablab.ai and Devfolio; the reverse is true for AWS/Google/Microsoft hackathons where enterprise polish wins.

---

## DevPost Winners

### 1. EcoLafaek — AWS AI Agent Global Hackathon 2025 (1st Place)
- **One-liner:** Citizen-led waste mapping in Timor-Leste powered by an autonomous multi-modal agent.
- **Domain:** Environmental / civic tech, emerging markets.
- **Link:** https://aws-agent-hackathon.devpost.com/submissions/818816-ecolafaek
- **Hackathon page:** https://aws-agent-hackathon.devpost.com/updates/38140
- **Approach:** Amazon Bedrock Nova-Pro + AgentCore tool chaining. Multi-modal reasoning classifies waste images, generates real-time pollution-hotspot data visualizations.
- **Why it won:** Emotional story ("waste in my country"), real citizens as users, concrete civic impact, showcased AgentCore's tool-orchestration correctly. Judged at AWS re:Invent 2025.
- **Prize:** Share of $45K USD pool (1st place).

### 2. AegisAgent — AWS AI Agent Global Hackathon 2025 (2nd Place)
- **One-liner:** Multi-agent insurance-claim auditor built entirely in AWS Kiro.
- **Link:** https://aws-agent-hackathon.devpost.com/submissions/818110-aegisagent-an-insurance-claim-app-fully-developed-by-kiro
- **Approach:** Kiro + Bedrock ensemble with semantic-indexed evidence curation, policy interpreter agent, compliance-reasoning agent.
- **Why it won:** "Built entirely in Kiro" narrative — demo-as-proof-of-toolchain.

### 3. Province — AWS AI Agent Global Hackathon 2025 (3rd Place)
- **One-liner:** Turn tax filing into a conversation; autonomous FormMapping pipeline hits 100% on Form 1040.
- **Link:** https://aws-agent-hackathon.devpost.com/submissions/828293-province
- **Approach:** Multi-agent architecture on Bedrock + Claude 3.5 Sonnet. One agent parses intent, another traverses form DAG, a third validates against IRS rules.
- **Why it won:** Headline metric ("100% accuracy"), universally hated problem, crisp multi-agent architecture diagram.

### 4. SalesShortcut — ADK Hackathon 2025 (Grand Prize)
- **One-liner:** Autonomous SDR: an AI sales rep team that generates leads, researches them, writes proposals, and does outreach.
- **Link:** https://devpost.com/software/salesshortcut
- **Builders:** Merdan Durdyyev, Sergazy Nurbavliyev.
- **Approach:** Google ADK multi-agent SDR system — Lead Hunter, Researcher, Proposal Writer, Outreach agents, coordinator.
- **Why it won:** Unambiguous business value, clear agent-role separation (judges love it), end-to-end demo video.
- **Hackathon:** 10,400+ participants, 62 countries, 477 projects, 1,500+ agents.

### 5. Edu.AI — ADK Hackathon 2025 (Latin America Regional Winner)
- **One-liner:** Democratizes Brazilian education with agents that grade essays, build personalized study plans, and create mock exams.
- **Link:** https://devpost.com/software/edu-ai-multi-agent-educational-system-for-brazil
- **Builder:** Giovanna Moeller.
- **Why it won:** Localized problem (ENEM/Brazil), solo builder with strong narrative, multi-agent pedagogy framing.

### 6. GreenOps — ADK Hackathon 2025 (Asia Pacific Regional Winner)
- **One-liner:** Autonomous FinOps/GreenOps team that continuously audits, forecasts, and optimizes cloud infrastructure for carbon.
- **Link:** https://devpost.com/software/greenops-gzp4aj
- **Builders:** Aishwarya Nathani, Nikhil Mankani.
- **Why it won:** Sustainability angle + measurable cost/carbon savings — ideal judging-criteria bait.

### 7. Nexora-AI — ADK Hackathon 2025 (EMEA Regional Winner)
- **One-liner:** Personalized education platform with interactive lessons, visuals, quizzes, and smart AI tutor.
- **Link:** https://devpost.com/software/teachai-upzofa

### 8. Particle Physics Agent — ADK Hackathon 2025 (Honorable Mention #1)
- **One-liner:** Converts natural language into validated Feynman diagrams using real physical laws and high-fidelity data.
- **Link:** https://devpost.com/software/particle-physics-agent
- **Why it matters for OpenEnv:** Best example of a "world-modeling" winner — the agent operates inside a formally-verified physics environment. This is the template for Round 2's World Modeling theme.

### 9. TradeSageAI — ADK Hackathon 2025 (Honorable Mention #2)
- **Link:** https://devpost.com/software/tradesage-ai
- **Approach:** ADK + Agent Engine + Cloud Run + Vertex AI for multi-agent trading hypothesis evaluation.

### 10. Bleach — ADK Hackathon 2025 (Honorable Mention #3)
- **One-liner:** Visual AI-agent builder: describe agents in English, design visually, test instantly.
- **Link:** https://devpost.com/software/bleach-7tqdmo
- **Why interesting:** Meta-level — an agent that builds agents.

### 11. RiskWise — Microsoft AI Agents Hackathon 2025 (Best Overall, $20K)
- **One-liner:** Global supply-chain risk analyzer spotting port delays, geopolitical events before they cascade.
- **GitHub issue:** https://github.com/microsoft/AI_Agents_Hackathon/issues/526
- **Hackathon:** https://microsoft.github.io/AI_Agents_Hackathon/winners/
- **Stack:** Python + React/Next.js + Azure AI Agent Service + Semantic Kernel + SQL.
- **Why it won:** Enterprise-grade B2B use case, Semantic Kernel showcase, timely (supply-chain stress news cycle).

### 12. Apollo: Deep Research Meta Agent — Microsoft AI Agents Hackathon 2025 (Best C# Agent, $5K)
- **GitHub issue:** https://github.com/microsoft/AI_Agents_Hackathon/issues/681
- **Approach:** Multi-agent orchestration with self-reflective RAG. Coordinator spawns expert sub-agents.
- **Why it matters for OpenEnv:** Self-reflection loop directly maps to the "Self-Improvement" theme.

### 13. Konveyor — Microsoft AI Agents Hackathon 2025 (Best Python Agent)
- **GitHub issue:** https://github.com/microsoft/AI_Agents_Hackathon/issues/645
- **One-liner:** Captures tribal knowledge as agents answer team queries contextually.

### 14. ModelProof: Sentinel AI Chat — Microsoft AI Agents Hackathon (Best JS/TS Agent)
- **GitHub issue:** https://github.com/microsoft/AI_Agents_Hackathon/issues/517
- **Approach:** Dual-LM consistency check — two models cross-validate each other's output for hallucinations, bias, toxicity.
- **Why it matters for OpenEnv:** Cross-agent verification is a reward-signal design pattern — use this for multi-agent interaction Round 2 theme.

### 15. WorkWizee — Microsoft AI Agents Hackathon (Best Copilot Agent)
- **GitHub issue:** https://github.com/microsoft/AI_Agents_Hackathon/issues/587
- **One-liner:** Automates incident management in Microsoft Teams (Jira / ServiceNow / Confluence integrations).

### 16. Everything Claude Code (ECC) — Anthropic Hackathon 2025 Winner
- **GitHub:** https://github.com/affaan-m/everything-claude-code
- **Builder:** Affaan Mustafa (solo) — won the Anthropic × Forum Ventures hackathon in ~8 hours.
- **One-liner:** Turns Claude Code into a "professional development engine" — skills, instincts, memory, continuous learning, security scanning.
- **Why it won:** Meta-tool for agent harness performance. Story: "a solo builder stacking compound tools." 140K+ stars.
- **Prize:** $15,000 in API credits.

---

## Devfolio Winners

### 17. DreamOps — Warpspeed 2025 (Lightspeed India, Bengaluru, June 21-22 2025) — Grand Prize
- **Hackathon:** https://warpspeed2025.devfolio.co/
- **Recap:** https://devfolio.co/blog/warpspeed-2025-recap/
- **Team:** SkySingh04, IncyJ4, harshkg23, Himanshu Singh.
- **One-liner:** AI agent that triages and resolves late-night programming issues, cutting debug time from 30-60 min to 2-5 min.
- **Why it won:** Relatable pain (3 AM on-call), clear metric (~15x speedup), lived-experience storytelling. Post-hack spun into product "Riquell Ops".
- **Prize:** Share of $12K+ pool.
- **Theme:** Agentic AI (24-hour offline). Sponsors: Sarvam AI (voice/multilingual stack), Bhindi AI.

### 18. Likeminds — Agentic Multi-Social Semantic Network — Global Agent Hackathon May 2025 (Grand Prize $5K)
- **Hackathon:** https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025
- **Winners list:** https://www.agno.com/blog/global-agent-hackathon-winners
- **PR:** https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025/pull/84
- **Builders:** Guaming & Vaibhav.
- **Approach:** Full-stack Agno-powered semantic graph across social networks; autonomous agents collaborate across dynamic systems.

### 19. Superwizard AI — Global Agent Hackathon May 2025 (2nd Place $2K)
- **PR:** https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025/pull/125
- **Builder:** Amirul Hamizan.
- **One-liner:** Chrome extension that turns web commands into magic — agentic browser automation.

### 20. Beifong — Global Agent Hackathon May 2025 (3rd Place $1K + BrowserUse Grand Prize $2.5K)
- **Builder:** Arun.
- **One-liner:** Curated information & podcasts agent.
- **Why interesting:** Double-dipped — won category + partner bounty. Teaches the strategy of targeting multiple tracks.

### 21. TripCraft AI — Global Agent Hackathon May 2025 (3rd Place $1K)
- **Builder:** Amit Wani.
- **One-liner:** Travel-planning multi-agent system.

### 22. github-potpie-agno-agent — Global Agent Hackathon May 2025 (Potpie Grand Prize)
- **Builder:** Arnav.
- **Approach:** Agno + Potpie + Groq — parses repos, answers code questions, generates deep repo insights via interactive playground.

---

## MLH / University / Research Hackathon Winners

### 23. DAMCS — UC Berkeley LLM Agents MOOC Hackathon 2025 (Decentralized & Multi-Agents Track, 1st Place)
- **Hackathon:** https://rdi.berkeley.edu/llm-agents-hackathon/
- **DevPost:** https://uc-berkeley-rdi-llm-agents.devpost.com/
- **Team:** Dr Marie Siew (SUTD) + Roblox researchers + academic collaborators.
- **Full title:** "LLM-Powered Decentralized Generative Agents with Adaptive Hierarchical Knowledge Graph for Cooperative Planning."
- **Approach:** Graph-based memory + structured communication protocol between agents. Agents cooperate to play Crafter (2D Minecraft-style env) multi-agent extension.
- **Why it's the most relevant for OpenEnv Round 2:**
  - Uses a real RL-style sandbox environment (Crafter) — template for OpenEnv.
  - Multi-agent + long-horizon planning + world-modeling all converge.
  - Published as research, not just demo — judges valued reward curves.
- **Attendance:** 3,000+ students, 127 countries.

### 24. ThreadFinders — UC Berkeley LLM Agents MOOC Hackathon 2025 (Applications Track, 2nd Place)
- **Team:** SoftServe employees.
- **One-liner:** System of interconnected GCP-hosted agents that search for missing people.
- **Why it won:** Social-impact story + complete GCP architecture.

### 25. NVARC — Kaggle ARC Prize 2025 (1st Place on Public Leaderboard)
- **Kaggle:** https://www.kaggle.com/competitions/arc-prize-2025
- **Results analysis:** https://arcprize.org/blog/arc-prize-2025-results-analysis
- **Blog:** https://developer.nvidia.com/blog/nvidia-kaggle-grandmasters-win-artificial-general-intelligence-competition/
- **Team:** Ivan Sorokin, Jean-Francois Puget (NVIDIA Kaggle Grandmasters).
- **Approach:** 4B-param fine-tuned model + synthetic data + test-time training + TRM components. Trained with NVIDIA NeMo RL + NeMo Skills. Reaches ~24% on ARC-AGI-2 under contest constraints.
- **Why it's essential reading for Round 2:** Real training loop, real synthetic-data pipeline, real reward-driven improvement. Hits every judging criterion.

### 26. Tiny Recursive Model (TRM) — ARC Prize 2025 Paper Prize
- **Author:** Alexia Jolicoeur-Martineau.
- **Approach:** ~7M-param single-network recursive model with separate answer + latent states, deep supervised refinement.
- **Result:** ~45% on ARC-AGI-1, ~8% on ARC-AGI-2.
- **Why it won:** Elegance — proved small + recursive beats big + brute-force.

---

## HuggingFace Trending Agent Environments (2025-26)

These aren't "hackathon winners" in the DevPost sense, but they are the trending Spaces / repos that the OpenEnv judges will be familiar with and compared against.

### 27. OpenEnv Hub itself (by Meta × HuggingFace)
- **Org:** https://huggingface.co/openenv
- **Blog:** https://huggingface.co/blog/openenv
- **InfoQ coverage:** https://www.infoq.com/news/2025/11/hugging-face-openenv/
- **Launched:** Oct 23, 2025. Quarterly RFC cycles, spec stability by mid-2026.
- **Integrations:** TorchForge, verl, TRL, SkyRL.
- **Why it matters:** This is the very framework the Bangalore Grand Finale uses — study the official example envs to see what "good" looks like per Meta.

### 28. AgentRL (arXiv 2510.04206)
- **Paper:** https://huggingface.co/papers/2510.04206
- **One-liner:** Scaling Agentic RL with Multi-Turn, Multi-Task Framework — fully-asynchronous generation/training pipeline.
- **Why it matters:** Blueprint for "Reward Improvement" (20% of judging).

### 29. Forge (by MiniMax)
- **Blog:** https://huggingface.co/blog/MiniMax-AI/forge-scalable-agent-rl-framework-and-algorithm
- **One-liner:** Scalable agent RL framework supporting arbitrary agent scaffolds for massive-scale RL.

### 30. Absolute Zero (Tsinghua)
- **Summary on HF Q2 2025 roundup:** https://huggingface.co/blog/vansin/hf-papers-25q3-top50
- **One-liner:** Models learn by *proposing and solving their own tasks* — no external data. SOTA on code + math reasoning.
- **Why it matters for Round 2's Self-Improvement theme:** Direct template. Agent proposes task → solves → trains on success signal. This is likely what the top Self-Improvement projects at Bangalore will echo.

### 31. ScienceBoard (HKU + Shanghai AI Lab)
- **One-liner:** Benchmark + environment for autonomous agents in scientific workflows (169 real tasks).
- **Why it matters for World Modeling theme:** A built domain env is the strongest World-Modeling pattern.

### 32. OpenEnv Turing Evaluation
- **Blog:** https://huggingface.co/blog/openenv-turing
- **One-liner:** Evaluating tool-using agents in real-world envs via OpenEnv.

### 33. OpenEnv Scaling Post
- **Blog:** https://huggingface.co/blog/burtenshaw/openenv-scaling
- **One-liner:** From free usage to thousands of concurrent environments — how the infra scales. Essential for the "Pipeline" 10% judging category.

---

## Other Notable Platform Winners

### 34. AURA — lablab.ai Recent Winner
- **Link:** https://lablab.ai/apps/recent-winners
- **One-liner:** Multi-agent AI guidance for industrial microtasks.

### 35. GameForge AI — lablab.ai
- **One-liner:** 4 specialized agents on a LangGraph pipeline turn any idea into a playable browser game in <60s.
- **Why it won:** Demo-is-the-product — you see a game materialize live.

### 36. Stylin' — lablab.ai
- **One-liner:** Two collaborating agents identify fashion from photo, find item at every price point, build 3 outfits in <30s.
- **Why it won:** Time-to-value is visible on screen.

### 37. Prism — lablab.ai
- **One-liner:** Agent that watches WhatsApp/Slack/Discord, extracts bugs/features/ideas, filters noise with product context.

### 38. Customer Support Agent — Kong Agentic AI Hackathon 2025 (Best Agentic Project)
- **Winners announcement:** https://konghq.com/blog/news/winners-of-kong-agentic-ai-hackathon
- **Team:** Shaik Mohammed Zakeer, Jayant Acharya, Tanmaiyee Vadloori.
- **Prize pool:** $10K.

### 39. Autonomous Security Auditor — Kong Agentic AI Hackathon 2025 (Best Solo Project)
- **Builder:** Sachin Ghumbre.
- **Why it won:** Solo builder, security vertical, clean demo.

### 40. kongversation-plugin — Kong Agentic AI Hackathon 2025 (Most Creative)

---

## Cross-Platform Patterns (Most Important Section)

Patterns that appear in >50% of 2025-26 winners:

1. **Coordinator-Workers architecture** (Apollo, SalesShortcut, Province, DAMCS, GameForge). A planner agent orchestrates 3-7 specialists.
2. **Long, visible reasoning traces in the demo video.** Judges watch the agent "think."
3. **Self-verification / dual-check patterns** (ModelProof, Apollo self-reflective RAG, DAMCS knowledge graphs). Critical for self-improvement storytelling.
4. **A named metric in the headline** (100%, ~24%, ~15x, <60s). Maps 1:1 to Reward Improvement judging.
5. **Emotional civic or personal hook** (EcoLafaek waste, Edu.AI Brazilian education, DreamOps 3am debugging, ThreadFinders missing people). Round 2's "Personal" world-modeling theme rewards this.
6. **Sponsored infra used non-trivially** (AgentCore orchestration, ADK regional envs, Semantic Kernel). For OpenEnv finale: show OpenEnv's state-persistence and multi-turn semantics being used in ways a simple tool-call can't replicate.
7. **Training, not just prompting, is a research-judge differentiator** (NVARC, TRM, DAMCS, Absolute Zero). This is where OpenEnv + TRL/Unsloth shines — most public DevPost winners skip this, but ARC-Prize-calibre judges punish submissions that don't actually train.
8. **Solo builders can win** (Giovanna Moeller on Edu.AI, Amirul Hamizan on Superwizard, Affaan Mustafa on ECC, David Babu on Energy Agent AI, Sachin Ghumbre on Kong). Don't let small team size be a blocker.
9. **Productize-in-demo.** Projects that show a path from hack → product (DreamOps → Riquell Ops) win trust.
10. **Regional / local problems travel well internationally** (EcoLafaek Timor-Leste, Edu.AI Brazil, Bhindi AI Indian use-cases at Warpspeed). For a Bangalore finale, leaning into an Indian problem is legitimate strategy.

---

## Top GitHub Repos to Study

Repos directly useful as reference code / architecture patterns:

| Repo | Why |
|------|-----|
| https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025 | All 60+ submissions with READMEs. Gold mine of patterns. |
| https://github.com/microsoft/AI_Agents_Hackathon (issues #349, #517, #526, #587, #638, #645, #681) | All 7 Microsoft category winners. |
| https://github.com/affaan-m/everything-claude-code | Solo-builder hackathon winner template. |
| https://huggingface.co/openenv | Reference envs from Meta/HF themselves. |
| https://github.com/Sri-Krishna-V/awesome-adk-agents | Curated ADK examples — excellent starting-point templates. |
| https://github.com/huggingface/blog/blob/main/openenv.md | Canonical OpenEnv intro — align your framing with this doc. |
| https://github.com/dipanjanS/mastering-intelligent-agents-langgraph-workshop-dhs2025 | LangGraph multi-agent patterns (good cross-ref for architecture diagrams). |
| https://github.com/victordibia/designing-multiagent-systems | Theory / design patterns for multi-agent LLM systems. |

---

## Key Hackathons to Monitor (April-June 2026)

- **Ruya AI Hackathon 2026** — https://ruyaai-hackathon-2026.devpost.com/ — Self-Improving Agents theme. Direct thematic overlap with OpenEnv Round 2.
- **ARC Prize 2026 / ARC-AGI-3** — https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3 — Next iteration of the benchmark.
- **AI Engineer Code Summit (Nov 19-22 NYC)** — https://www.ai.engineer/code
- **AI Hackathon @ Berkeley 2026** — https://ai.hackberkeley.org/

---

## Sources

- https://aws-agent-hackathon.devpost.com/updates/38140-congratulations-to-the-winners-of-the-aws-ai-agent-global-hackathon
- https://cloud.google.com/blog/products/ai-machine-learning/adk-hackathon-results-winners-and-highlights/
- https://techcommunity.microsoft.com/blog/azuredevcommunityblog/ai-agents-hackathon-2025-%E2%80%93-category-winners-showcase/4415088
- https://www.agno.com/blog/global-agent-hackathon-winners
- https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025
- https://rdi.berkeley.edu/llm-agents-hackathon/
- https://uc-berkeley-rdi-llm-agents.devpost.com/
- https://developer.nvidia.com/blog/nvidia-kaggle-grandmasters-win-artificial-general-intelligence-competition/
- https://arcprize.org/blog/arc-prize-2025-results-analysis
- https://www.kaggle.com/competitions/arc-prize-2025
- https://huggingface.co/blog/openenv
- https://huggingface.co/openenv
- https://www.infoq.com/news/2025/11/hugging-face-openenv/
- https://huggingface.co/papers/2510.04206
- https://huggingface.co/blog/MiniMax-AI/forge-scalable-agent-rl-framework-and-algorithm
- https://huggingface.co/blog/burtenshaw/openenv-scaling
- https://huggingface.co/blog/openenv-turing
- https://huggingface.co/blog/vansin/hf-papers-25q3-top50
- https://warpspeed2025.devfolio.co/
- https://devfolio.co/blog/warpspeed-2025-recap/
- https://blog.pointblank.club/dreamops-to-riquell-ops-a-hackathon-win-to-product/
- https://lablab.ai/apps/recent-winners
- https://lablab.ai/blog/raise-your-hack-summary-2025
- https://konghq.com/blog/news/winners-of-kong-agentic-ai-hackathon
- https://github.com/affaan-m/everything-claude-code
- https://ruyaai-hackathon-2026.devpost.com/
- https://fetch-ai-hackathon.devpost.com/
- https://microsoft.github.io/AI_Agents_Hackathon/winners/
