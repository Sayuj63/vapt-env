# Meta / PyTorch / OpenEnv Hackathon Winners (Global)

> Research target: winning projects from Meta / PyTorch / OpenEnv / Llama / Agent-RL hackathons globally (2024-2026), to inform a winning strategy for the Meta PyTorch OpenEnv Hackathon × SST Grand Finale in Bangalore (Apr 25-26 2026).
> Scope: Extends beyond the 5 SF OpenEnv winners (Calendar, REPL, CARLA, TB2, Reasoning Gym) already captured in Round 1.

---

## Executive Summary — Patterns Across Winners

Across 20+ events reviewed, winners cluster around a small number of repeatable patterns:

1. **Hardware / real-world hook beats pure software.** OpenGlass ($20 smart glasses, Llama 3 Hackathon SF 2024) and the SO-100 laundry-folding robot (LeRobot Worldwide 2025) won by pairing a cheap physical artifact with a slick AI demo. For OpenEnv: bolt the env to a camera, a sensor, or an actual keyboard/shell process.
2. **"Concrete societal pain → LLM" storytelling wins Impact tracks.** Guardian (NHS triage, London), CurePharma AI (rural Indian pharmacies on WhatsApp), Tachiwin (indigenous languages). Each judge could re-tell the story in one sentence. Translate this to OpenEnv: choose a pain (farmer's crop pricing, rural A&E triage, ATC handoffs) and build the env around it.
3. **Multi-agent / adversarial structure wins "Innovation" judging.** Deb8 (AIs debate each other, 3rd AI judges), Compliance Wizards (risk + voice assistant), MarketForge. The SST 40% innovation weight strongly rewards this.
4. **Environment creators beat environment users.** The Unsloth / PyTorch / AMD November 2025 hackathon was won by @osiris for *creating new* Julia/Ruby/Zig RL envs (not just training on existing ones). Same pattern expected at SST: don't train on Wordle — ship a novel env.
5. **Binary, verifiable rewards beat shaped rewards.** HF's own TRL+OpenEnv docs admit "binary rewards (1.0 for success, 0.0 otherwise) gave cleaner training signals." Winners avoid fiddly reward shaping.
6. **Short demo loop.** Immersia (~5 min to create & play a full generative adventure), OpenGlass (5-second capture cadence), Atlas (live patient intake) — every winning demo can be restarted in under a minute on stage.
7. **Pretty ≠ winning. Pipeline does.** The SF OpenEnv theme "Calendar / REPL / CARLA / TB2 / Reasoning Gym" were all *pipelines you can train into*. Judges reward reward-curve graphs, not slide decks.
8. **LATAM / Impact tracks: accessibility + language + WhatsApp** consistently place top 3 (CurePharma, CivicFix, Aarogya, Tachiwin). This is a known pattern for a Bangalore audience.

### Direct tactical implications for SST Bangalore (Apr 25-26 2026)

- Round 2 themes (Multi-Agent, Long-Horizon, World Modeling, Self-Improvement, Wild Card) map cleanly onto Patterns 3, 5, 7. Best pick: an env that is simultaneously multi-agent **and** self-improving (agents generate new tasks for each other) — mirrors Berkeley AgentBeats' "green evaluator vs purple solver" motif that is currently winning.
- 40% Innovation + 30% Storytelling = 70% is narrative/novelty. The reward curve (20%) is table stakes but small. Lead with story.
- $200 compute budget + Unsloth/TRL favors 1-3B models on Wordle/Sudoku-style envs. Avoid >7B unless you have a strong reason.

---

## Event 1: Meta Llama 3 Hackathon (San Francisco, May 11-12 2024)

Co-hosted by Cerebral Valley + SHACK15. 51 projects in 24 hours, $10K+ prize pool. The breakout hackathon that launched the modern Meta x Cerebral Valley partnership.

### 1st Place — OpenGlass (by BasedHardware / Nik Shevchenko)
- **Description:** Turn any glasses into AI-powered smart glasses for $20 of hardware.
- **Problem:** Commercial smart glasses cost $300+; democratize wearable AI.
- **Technical approach:** Seeed XIAO ESP32-S3 Sense camera + EEMB LP502030 battery. Captures 1 image / 5 seconds, constant audio transcription. moondream VLM for scene understanding, Llama 3 for Q&A over the running memory log.
- **GitHub:** https://github.com/BasedHardware/OpenGlass (thousands of stars)
- **Why it won:** Sub-$20 BOM + working live demo + an obvious "why didn't anyone do this sooner" hook. 1,500 pre-order waitlist by Monday morning. Meta's AI team tweet-endorsed it within 48 hours.
- **Takeaway for OpenEnv:** Physical artifact + low BOM + instant demo loop.

### 2nd Place — Deb8
- **Description:** AI debate arena — two Llama-based agents debate Lincoln-Douglas style, a third AI judge scores.
- **Why it won:** Multi-agent + adversarial + built-in reward signal (judge score). This is *exactly* the shape of a winning OpenEnv submission.
- **GitHub:** Repo not reliably located; check https://metallama3.devpost.com/project-gallery for submission.

### 3rd Place — Team AAA (Activation Ablation Augmentation)
- **Description:** Interpretability / safety — neutralize activation layers in Llama 3 to suppress unwanted outputs.
- **Why it won:** Only research-y submission in the top 3; judges rewarded depth over polish.
- **GitHub:** Submission via Devpost gallery (not centrally indexed).

### Notable non-podium
- **SixthSense:** Ray-Ban Meta integration for bookmarking real-world content.
- **Hound:** RAG for law enforcement / anti-human-trafficking.
- **Mongoose Miner:** Code-generation platform.
- **Feycher, Joe CRM:** Customizable agents. All at https://metallama3.devpost.com/project-gallery.

---

## Event 2: Meta Llama Impact Hackathon (London, November 2024)

Co-hosted by Cerebral Valley. 200+ developers, 56 teams, Llama 3.2, themes: healthcare / clean energy / social mobility. $50K shared among top 3 + 6 weeks mentorship + eligibility for Llama Impact Grants (up to $500K).

### 1st Place — Guardian (tool: "Atlas")
- **Description:** AI triage assistant for NHS A&E departments.
- **Problem:** A&E waiting times; uneven triage by junior staff.
- **Technical approach:** Llama 3.2 for patient intake NLU, multilingual translation, real-time risk scoring. "Second pair of eyes" framing for clinicians.
- **Why it won:** NHS is a stress-tested, universally-understood pain. The demo told a complete patient-arrival-to-triage story in under 3 minutes.
- **GitHub:** Not publicly linked in Meta's announcement. Likely private given clinical focus.

### 2nd Place — Gripmind (powered by Groq)
- **Description:** Robotic arm controlled by brain signals / voice / images for assisted living.
- **Technical approach:** Llama 3.2 Vision + EEG input → robotic arm control.
- **Why it won:** Accessibility theme + multi-modal + physical artifact on stage.

### 3rd Place — Pharmallama
- **Description:** On-device pharmacy consultation; flags conflicting drugs.
- **Why it won:** On-device emphasis (privacy) + concrete use case.

### Finalists
- **ClimaticAI** (smart-home energy optimization)
- **Team WinAmp** (sustainable eating)
- **The GoodPath** (multilingual career development)

- **Source:** https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/

---

## Event 3: Meta Llama Hackathon India — Bengaluru (2024, Reskilll + Meta)

270+ participants. Llama 3 + WhatsApp APIs. Themes: AI for Societal Good / Build on WhatsApp.

### 1st — CurePharma AI ($3K)
- Personalized medication info in regional languages, prescription scanning, WhatsApp ordering via e-pharmacies. Rural/underserved focus.

### 2nd — CivicFix ($2K)
- WhatsApp bot for citizens to report potholes / broken streetlights via voice note or photo. AI classifies and prioritizes for local authorities.

### 3rd — Evalssment ($1K)
- AI-graded assignments + personalized feedback for teachers.

### Best All-Women Team — Aarogya Assist / SheBuilds ($1K)
- Multilingual WhatsApp healthcare aggregator (meds, lab reports, insurance).

**GitHub:** None publicly linked by Meta's announcement. Pattern: Indian Meta hackathon winners skew WhatsApp + regional language + accessibility. Directly relevant for Bangalore 2026.

- **Source:** https://ai.meta.com/blog/llama-hackathon-india/

---

## Event 4: LlamaCon Hackathon (San Francisco, May 3-4 2025)

Meta x Cerebral Valley x SHACK15. 238 attendees, 44 projects, $35K prizes. First event using Llama 4 (Maverick + Scout).

### 1st — OrgLens
- **Description:** AI expert-matching system; ingests Jira/GitHub/docs/resumes, builds knowledge graph, routes questions to the right internal expert.
- **Stack:** React + Tailwind + Django, GitHub API, Llama API.
- **Why it won:** B2B pain, clean enterprise demo, knowledge-graph visualization was the "wow" moment.

### 2nd — Compliance Wizards
- Multimodal transaction fraud analyzer; email alerts + AI voice assistant for end-user reporting. Uses Llama 4 multimodal to search news + upload client info.

### 3rd — Llama CCTV Operator (Agajan Torayev)
- **Description:** Describe a surveillance event in plain English → system watches CCTV for it; no fine-tuning required.
- **Stack:** Llama 4 multimodal; samples every 5 frames.
- **GitHub:** https://github.com/torayeff/llamacon-hackathon-2025-sf

### Best Llama API Usage — Geo-ML (William Davis)
- 3D geological model generation from 400-page reports. Uses Llama 4 Maverick's long context + multimodal text-image.

### Notable Submissions with Public Repos
- **EchoFrame** — video-based learning/content analysis on Llama 4. https://github.com/shrutiudupa26/LlamaConHackathon-EchoFrame

- **Source:** https://ai.meta.com/blog/llamacon-hackathon/

---

## Event 5: Meta Llama 3.3 Hackathon (Oslo, February 2025)

Cerebral Valley + Meta. Nordic AI engineers. $30K+ in cash & hardware prizes. Organizer: Ola Tørudbakken.

- **Public winners list:** Not yet indexed in searchable sources; Cerebral Valley event page is live but gallery is gated. Event page: https://cerebralvalley.ai/e/meta-llama-hackathon-oslo-41193aea
- **Gap documented:** No public winner repos found for Oslo. Likely the same pattern as other CV events (industrial / enterprise tilt).

---

## Event 6: Llama 4 Hackathon (Seattle, June 21-22 2025)

Cerebral Valley + Meta. Llama 4 focus.

- **Gap documented:** No public winners located in searchable sources. Cerebral Valley page: https://cerebralvalley.ai/e/llama-4-hackathon-seattle-c8f62261. No Devpost / no Meta blog recap found.

---

## Event 7: Llama Impact Pan-LATAM Hackathon (2025, Online via lablab.ai)

1,034 participants, 114 teams, 48 final projects. Tracks: Education & Culture / Economic Development / On-Device Deployment. Prizes: $3K / $1.5K / $500.

### 1st — Tachiwin Indigenous Languages Translator
- **Description:** Llama 3.1 fine-tuned for Mexican indigenous languages (e.g. Tutunakú). Preservation + equity framing.
- **Submission page:** https://lablab.ai/ai-hackathons/hackathon-llama-impact-pan-latam-es/tachiwin/tachiwin-indigenous-languages-translator
- **Why it won:** Cultural mission + measurable translation BLEU improvement + on-device deployment narrative.
- **GitHub:** Not linked on lablab; may be in Devpost sub-page.

---

## Event 8: Llama Impact Hackathon Rome (Nov 29 – Dec 1 2024)

- **Gap documented:** lablab page lists the event but winners stream (https://www.youtube.com/watch?v=Ho-FuKUZYQU) wasn't transcribed and no blog recap was indexed. No public winner names located.

---

## Event 9: OpenEnv Hackathon SF (Cerebral Valley x Meta x PyTorch Foundation, March 7-8 2026)

Reference event for SST Bangalore. $100K+ prize pool across 5 RL / agentic orchestration themes. **Top 5 winners already documented in Round 1: Calendar, REPL, CARLA, TB2, Reasoning Gym.** This event seeded the Hugging Face `openenv` org with 90+ community spaces.

### Community/Gallery signal (from the Agentic RL Hackathon SF 2026 collection)
A collection of 100+ environments built around the event. Notable submissions (indicative of what the judging room liked aesthetically, even when not top-5):
- **HarFeast Env** (openenv-community) — simulated farming env with action-based control. https://huggingface.co/spaces/openenv-community/harfeast-env
- **Football Play-Calling Environment** (afletcherstudent) — play-calling simulation. https://huggingface.co/spaces/afletcherstudent
- **OpenRange** (blocks3k) — multi-agent cybersecurity simulation.
- **Executive Inbox Environment (RL)** (hoony) — simulated email/meeting env.
- **NegotiateEnv** (KushalAdhyaru) — B2B SaaS contract negotiations.
- **Multi-Agent MarketForge** (kenmandal) — multi-commodity market sim.
- **Kube SRE Gym** (openenv-community) — SRE/ops commands. https://huggingface.co/spaces/openenv-community
- **Medagentbench Env** — FHIR / primary-care EHR actions.
- **SentinelOps Arena** — cybersecurity sim with AI agents.
- **Auditron** (shapiron) — fraud detection in procurement auctions.
- **KantBench** — game-theory sims with AI opponents.
- **Office OS** (HarshalH) — GTM strategy RL sim.
- **OmniBench Aegis Env** (AGIreflex) — reproducible multi-domain benchmark.
- **GardenRL** — hydroponic farming sim.
- **RANS Spacecraft Navigation** — spacecraft control.
- **VarahaWildFireDroneReliefTrainingSim** — wildfire drone RL benchmark.

**Collection link:** https://huggingface.co/collections/openenv (search "Agentic RL Hackathon SF 2026")
**Signal:** The pool skews toward *professional / enterprise world modeling* (SRE, EHR, contracts, auctions, procurement fraud). Personal-life envs (calendar, inbox) and sim-game envs (football, KantBench) also placed. A differentiated Bangalore submission: pick a **professional world-modeling domain underrepresented in the SF gallery** (e.g. Indian logistics, agri-commodity, UPI fraud, telemedicine triage) and lean into it.

---

## Event 10: Unsloth × PyTorch × AMD RL Environments Hackathon (November 2025)

The event most structurally similar to SST Bangalore. Challenge: create new OpenEnv environments + train with GRPO on limited compute (mirrors $200 budget + Unsloth constraint).

### 1st — @osiris — "GRPO on Julia / Ruby / Zig RL environments"
- **Description:** Trained a multi-language 3B coder LM with GRPO across three under-represented programming language envs (Julia, Ruby, Zig).
- **Writeup:** https://medium.com/@yogeshsingla481/training-a-multi-language-3b-coder-lm-with-reinforcement-learning-grpo-f37577d5e5f7
- **Why it won:** Judges' words: "went above and beyond in terms of creativity and implementation." Contrast: other entries were game envs (PacMan, survival island). Winner built *useful, novel envs* that a real developer might use.
- **Takeaway (critical for SST):** The judging bar is "did you create a genuinely new, useful env?" Not "did you beat benchmarks on an existing env?"

---

## Event 11: AgentX – AgentBeats Competition (Berkeley RDI, Fall 2025 – May 2026)

Not strictly a hackathon, but a rolling competition co-sponsored by **PyTorch (Meta) + Hugging Face + Unsloth** via the "OpenEnv Challenge" custom track — $10K in HF credits + PyTorch blog publication. Paradigm: "green" evaluator agents vs. "purple" competing agents. $1M+ total prizes. 1,300+ teams.

### Phase 1 Winner (Multiagent Evaluation) — MAizeBargAIn / "Meta-Game Negotiation Assessor"
- **Team:** PhD students Gabriel Smithline + Chris Mascioli (Strategic Reasoning Group).
- **Description:** An evaluator agent that generates negotiation meta-games and scores purple agents on strategic reasoning.
- **Why it won:** Novelty of evaluator-as-agent paradigm; strong game-theory grounding.
- **Source:** https://strategicreasoning.org/srg-team-is-a-winner-in-the-agentx-agentbeats-competition/
- **Takeaway:** "Your env is an agent that generates tasks" is a powerful framing and maps directly onto SST's **Self-Improvement** theme.

---

## Event 12: Gradio Agents & MCP Hackathon (HuggingFace, June 2-10 2025)

Online, $16,500 prizes. Adjacent to OpenEnv (HF-native, Gradio + MCP).

### Agentic Demo Showcase Winner — LLMGameHub / Immersia
- **Description:** Generative adventure game — describe a world, pick a hero + genre, play a ~5-minute LLM-driven adventure with dynamic first-person images (Gemini) and adaptive music (Lyria).
- **HuggingFace Space:** https://huggingface.co/spaces/Agents-MCP-Hackathon/LLMGameHub
- **Website:** https://www.immersia.fun/
- **Demo video:** https://youtu.be/pQfP9lA1QUM
- **Stack:** LangGraph + LangChain state graph, 4 agents (Story / Image / Music / State), Redis, async parallelism for zero-latency scene transitions.
- **Why it won:** Multi-agent orchestration + genuinely delightful demo + short loop (5 min to ending) + technical depth (async parallel generation).
- **Writeup:** https://huggingface.co/blog/kikikita/immersia-ai-games
- **Direct SST analogue:** A "world modeling (personal)" env where agents generate mini-worlds a player (or another agent) must navigate.

### Other notable submissions in collection
Router MCP, MatchMaiker, FlowLab, RASS (Retrieval Augmented Simple Syndication), Misty Climate, AI Stylist, BuyVerse, LLM Game Master, Financial Multi-Agent, Chess Agent, WellBe+ Assistant.
Full collection: https://huggingface.co/collections/Agents-MCP-Hackathon/ai-6836e0569f66509b48bc32bf

---

## Event 13: LeRobot Worldwide Hackathon (June 14-15 2025, HuggingFace)

250+ teams, 3,000 hackers, 44 countries. Local + online. Not pure OpenEnv but closest cousin (HF-native RL / imitation learning event).

### US 1st / Global 2nd — Laundry & Pills Robot (Pranav Saroha, 16, + Shaan Patel, 19)
- **Description:** SO-100 bimanual robotic arms fold T-shirts + sort pills.
- **Technical approach:** Imitation + RL. 50 training episodes, 4-camera setup. Models: π0 (pi-zero) base, SmolVLA, ACT. 70% success rate during the hackathon → 85% post-event.
- **HuggingFace:** Team released datasets and models on HF. See https://huggingface.co/LeRobot-worldwide-hackathon
- **Why it won:** Real grandfather story ("I wanted to help my grandfather manage his pills"). Tangible physical demo on stage. Elderly-care framing.
- **Coverage:** https://theaiinnovator.com/team-behind-ai-robot-that-folds-laundry-wins-hackathon/ , https://lightning.ai/blog/lerobot-hackathon-winners

### All-winners HF Space
https://huggingface.co/spaces/LeRobot-worldwide-hackathon/all-winners

---

## Event 14: RAISE Your HACK 2025 (lablab.ai + Groq + Meta)

6,247 participants, 922 teams. Global, online. $150K+ prize pool. Required Groq API + ≥1 Llama model.

- **Public per-track winner names:** lablab.ai article referenced but behind Cloudflare when fetched.
- **Pattern signal:** Winners consistently pair Groq (for speed) + Llama (for reasoning). For OpenEnv Bangalore, the analogue is Unsloth (speed) + Llama 3.1/3.2 (reasoning) on whichever env you ship.
- **Gap:** Full winners list wasn't retrievable. https://lablab.ai/blog/raise-your-hack-summary-2025

---

## Event 15: PyTorch Dendritic Optimization Hackathon (PerforatedAI, PyTorch Conference Week 2025)

$18,500 prize pool. Not an RL hackathon but a PyTorch-community co-branded event. Task: improve existing PyTorch projects with Perforated AI's dendritic optimization (accuracy/compression).

- **Winners:** Judged on accuracy and compression gains + model/dataset prevalence.
- **Submission repo:** https://github.com/PerforatedAI/PerforatedAI/tree/main/Examples/hackathonProjects — each PR = one submission.
- **Takeaway:** Unusual structure (PRs as submissions) — relevant only as inspiration for how OpenEnv community might grade env PRs.

---

## Event 16: NeurIPS 2024 Competition Track (relevant RL + multi-agent tracks)

16 competitions. Three relevant to the multi-agent / RL-env framing that SST Bangalore will judge:
- **MyoChallenge 2024** — neuromechanical dexterity (manipulation + locomotion tracks). Not public per-team results in the short window searched; historical winners come from ETH / MIT / academic labs.
- **Melting Pot → Multi-Agent Cooperation Challenge** — cooperative language-model agents in text environments. Direct relative of OpenEnv multi-agent theme.
- **Game Adaptation Challenge** — agents face changing game dynamics in a 1v1 format.

**Gap:** Per-team winners for 2024 not fully indexed. **Pattern:** Every one of these is "build your env + submit your agent" — identical structure to OpenEnv. Melting Pot / Multi-Agent Cooperation is the closest precedent to a winning multi-agent OpenEnv submission.

---

## Event 17: NeurIPS 2025 PokéAgent Challenge

- "Competitive and Long-Context Learning at Scale" — Pokémon battles as RL benchmark.
- Paper: https://sethkarten.ai/data/NeurIPS_2025_PokeAgent_Challenge.pdf
- **Relevance:** Long-horizon planning benchmark that multiple teams have since ported as OpenEnv-compatible. The pattern — take a *well-known game* and wrap it as a long-horizon env — is a reliable hackathon shape. Atari and OpenSpiel envs already live in HF's openenv org.

---

## Cross-Event Patterns (What Actually Wins)

| Pattern | Evidence | Applied to SST Bangalore |
|---|---|---|
| Physical / tangible artifact | OpenGlass, Gripmind, LeRobot laundry bot | Bolt the env to a webcam or a real CLI |
| Sub-60-second reset demo | Immersia, OpenGlass, CCTV Operator | Rehearse a 45-sec loop |
| Story grounded in a real person's pain | Guardian (NHS), Laundry Bot (grandfather), CurePharma (rural patients) | Name the person in slide 1 |
| Multi-agent adversarial loop | Deb8, MarketForge, AgentBeats | Perfect for Multi-Agent Interactions theme |
| Evaluator-as-agent / self-improvement | AgentX MAizeBargAIn, Unsloth @osiris | Perfect for Self-Improvement theme |
| Novel env (not benchmark on existing) | Unsloth @osiris (Julia/Ruby/Zig), OpenEnv SF HarFeast etc. | Ship a truly new env, not Wordle derivative |
| Binary rewards | HF TRL docs on Wordle/Sudoku | Avoid reward shaping |
| Accessibility + local language + WhatsApp | CurePharma, CivicFix, Tachiwin, Aarogya | Indian judges will reward this |
| Short LLM (1-3B) + Unsloth | Wordle runs at 1B; $200 compute budget | Don't pick a >7B model |
| Enterprise / professional world model | OrgLens, Kube SRE Gym, Medagentbench | Good for World Modeling (Professional) |

---

## GitHub Repos & HF Spaces Worth Studying Before Bangalore

### Primary OpenEnv infrastructure
- https://github.com/meta-pytorch/OpenEnv — the framework itself. Read `tutorial/01-environments.md` and `tutorial/04-training.md`.
- https://github.com/huggingface/trl — `examples/scripts/openenv/wordle.py` is the canonical GRPO + OpenEnv example.
- https://github.com/huggingface/openenv-course — HF's official onboarding course.
- https://github.com/TextArena/TextArena — Wordle/Sudoku/Snake/Tic-Tac-Toe text games that OpenEnv wraps.
- https://huggingface.co/openenv — the canonical env hub (Echo, REPL, Chat, Coding, Atari, OpenSpiel, BrowserGym, TB2, Wordle, Sudoku).

### Gallery / studied patterns
- https://huggingface.co/spaces/openenv-community — community envs (HarFeast farming, Kube SRE Gym, Medagentbench, SentinelOps, Bio Experiment, etc.).
- https://huggingface.co/collections/Agents-MCP-Hackathon/ai-6836e0569f66509b48bc32bf — Gradio/MCP winners with clear documentation.
- https://huggingface.co/spaces/LeRobot-worldwide-hackathon/all-winners — LeRobot winners page.

### Individual winning projects (reverse-engineer)
- **OpenGlass (hardware + VLM + Llama):** https://github.com/BasedHardware/OpenGlass
- **Llama CCTV Operator (multimodal frame sampling):** https://github.com/torayeff/llamacon-hackathon-2025-sf
- **EchoFrame (Llama 4 video):** https://github.com/shrutiudupa26/LlamaConHackathon-EchoFrame
- **Immersia / LLMGameHub (multi-agent narrative):** https://huggingface.co/spaces/Agents-MCP-Hackathon/LLMGameHub
- **Unsloth @osiris writeup (GRPO + multi-lang code env):** https://medium.com/@yogeshsingla481/training-a-multi-language-3b-coder-lm-with-reinforcement-learning-grpo-f37577d5e5f7

### Documentation / reference
- Meta Llama 3 Hackathon gallery (51 projects): https://metallama3.devpost.com/project-gallery
- TRL + OpenEnv integration docs: https://huggingface.co/docs/trl/en/openenv
- OpenEnv evaluating tool-using agents (Turing post): https://huggingface.co/blog/openenv-turing

---

## Documented Gaps (Honest)

- **No public winners list** for: Meta Llama Hackathon Oslo (Feb 2025), Llama 4 Hackathon Seattle (Jun 2025), Llama Impact Hackathon Rome (Dec 2024). Cerebral Valley keeps galleries partially private.
- **No Meta Connect hackathon** was found for 2024 or 2025 — Connect is a product event, not a hackathon.
- **No Meta AI / FAIR community challenges** with public submissions have been indexed in 2024-2026 beyond AgentBeats. FAIR tends to release benchmarks (e.g. DiPLOMat, Meta-World, Habitat challenges) through NeurIPS competitions rather than standalone hackathons.
- **No Meta PyTorch OpenEnv edition** in London, NYC, Tokyo, Paris, Berlin, Seoul, Singapore, Toronto, Austin, or Boston was announced as of Apr 20 2026. Only SF (March 2026) and Bangalore (April 2026) exist.
- **NeurIPS 2024 competition per-team winners** not fully indexed in the search window; deeper scraping of neurips.cc archives recommended if needed.
