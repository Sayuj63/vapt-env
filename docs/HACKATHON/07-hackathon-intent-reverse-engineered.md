# Reverse-Engineered Intent — The 4 Organizers of the Meta PyTorch OpenEnv Hackathon

Research date: 2026-04-20. Purpose: decode what each of the 4 organizers of the Meta PyTorch OpenEnv Hackathon (SF Mar 7-8 2026 → India Finale Apr 25-26 2026) actually want, so a finalist team can design a submission that advances all four agendas at once.

---

## Executive Summary — what each organizer really wants, in one sentence

- **Meta (FAIR + Superintelligence Labs / MSL).** Commoditize the agent-environment layer so Meta sets the de-facto standard for how RL-trained agents are built, then harvest community-built envs as free training data for Meta's closed frontier models (Muse Spark and successors) — while specifically closing the gap in **long-horizon agentic systems and coding workflows** that Meta itself has publicly admitted is its biggest weakness.
- **PyTorch Foundation.** Make PyTorch the anchor of the entire agentic-AI stack (RL post-training, distributed RL, inference, edge) so PyTorch remains the default framework as workloads shift from pre-training into RL/agents — where a JAX/TPU advantage could otherwise emerge. Spisak's 2026 priority is literally: "productize a PyTorch-native agentic and RL stack" and "drive global standardization around open RL environments."
- **Cerebral Valley.** Convert curated access to the hottest AI-lab launches into a four-way flywheel: (1) sponsorship fees from model labs, (2) deal-flow for the VCs CV programs as judges (Sequoia, Kleiner, Sapphire, Mayfield), (3) newsletter-subscriber growth for Newcomer's $19/mo business, (4) editorial power to name who gets anointed as the next "cracked founder."
- **Scaler School of Technology.** Use a Meta/PyTorch co-branded global event to cement SST's positioning as "India's Ivy League for the AI age," generate Meta/HuggingFace interview funnels for its own students, and create a defensible marketing moat against IITs in the 2026-27 NSET admission cycle.

---

## Meta (FAIR + Meta AI research agenda)

### The strategic context (what changed in 2025)

Three executive transitions reframe Meta's AI posture in the exact window OpenEnv launched:

- **Joelle Pineau**, head of FAIR since 2023, announced April 1 2025 she was leaving (last day May 30 2025). Led Llama, PyTorch. Joined Cohere as CAO Aug 2025.
- **Soumith Chintala**, PyTorch co-creator, announced Nov 6 2025 he was leaving Meta on Nov 17 2025. Became CTO of Thinking Machines Lab (Mira Murati's startup) Jan 2026.
- **Yann LeCun**, Chief AI Scientist, announced Nov 19 2025 he was leaving to found AMI Labs. Raised $1.03B at $3.5B pre-money in Mar 2026 to build world-model architectures. Publicly called the LLM-RL path "complete bullshit."
- **Alexandr Wang** (ex-Scale AI, brought in via $14.3B deal) now runs Meta Superintelligence Labs (MSL). Meta released **Muse Spark** (closed model) April 8 2026 — a strategic break from Meta's "open" history.

What's left after the exodus: the *productized* open-source AI stack — PyTorch, Llama, OpenEnv, TorchForge, Monarch — now reports into **Joe Spisak** (Product Director at MSL, leading PyTorch and Meta's Agentic platform). The research-vs-product tension at FAIR resolved in favor of product, with open-source as distribution.

This matters because OpenEnv is not a FAIR research project anymore — it is an MSL **ecosystem-control play**. The hackathon is not looking for research papers, it is looking for community-authored environments.

### What research direction OpenEnv is advancing

Three explicit signals from primary sources:

1. **Agent reliability in stateful, permissioned, production-grade systems** — not demo RL. From the Feb 12 2026 Meta/HF/Turing "OpenEnv in Practice" blog on Calendar Gym: "AI agents often perform impressively in controlled research settings, yet struggle when deployed in real-world systems where they must reason across multiple steps, interact with real tools and APIs, operate under partial information, and recover from errors in stateful, permissioned environments." The finding: agents hit ~90% with explicit IDs but only ~40% with NL descriptions, and >50% of failures were malformed tool args. This is the Meta-stated research gap.

2. **Code World Models + agentic coding** — CWM (arxiv 2510.02387, Meta FAIR, 32B open-weights, Oct 2025). CWM was mid-trained on observation-action trajectories from Python interpreter and agentic Docker envs, then multi-task RL in verifiable coding/math/SWE envs. 65.8% on SWE-bench Verified. This is the *flagship paper* OpenEnv's launch blog explicitly references: "Replicate state-of-the-art methods like Code World Models." Translation: Meta wants OpenEnv to become the default training substrate for CWM-successor models.

3. **Environments as the scaling axis of RL post-training** — from Burtenshaw (HF) OpenEnv scaling blog: "RL post-training is bottlenecked by environment throughput, not compute. When training with GRPO or running large-scale evaluations, you need thousands of concurrent episodes." OpenEnv is Meta's bet that the next frontier-model bottleneck is env throughput, not GPUs.

### What Meta gains by commoditizing agent environments

- **Free training data at scale.** Every community-submitted env becomes a training substrate for Meta's closed Muse Spark + successors. Meta said explicitly in its Q1 2026 earnings: "We continue to invest in areas with current performance gaps, specifically long-horizon agentic systems and coding workflows." OpenEnv is the crowdsourcing layer for that.
- **Lock-in via format.** Gymnasium-style `reset/step/state` + MCP action schema + Docker packaging becomes the standard *Meta controls the spec of*. Same playbook as PyTorch: win by being the community default; capture the value downstream via Llama/Muse Spark.
- **Neutralize the JAX/TPU threat in RL.** Agents/RL are the part of the stack Google could have flipped. By making OpenEnv the neutral open-source interface (PyTorch Foundation-governed, Linux-Foundation-housed), Meta defangs a Google-native competitor.
- **Undercut OpenAI/Anthropic.** OpenAI has no published agent-env framework. Anthropic's agent SDK is closed. If the community defaults to OpenEnv, any model vendor that doesn't speak OpenEnv is a second-class citizen in the RL ecosystem.

### Why this is strategic vs. OpenAI/Anthropic/Google

| Rival | Their move | Meta's counter via OpenEnv |
|---|---|---|
| OpenAI | Agents SDK (closed) + Custom GPTs | OpenEnv is open + MCP-compatible → the *inference-time* and *training-time* environment is the same object |
| Anthropic | MCP (won the tool protocol layer) | OpenEnv RFC 003/004 integrate MCP — Meta didn't fight the protocol, they wrapped it |
| Google | JAX + Gemini + large tool-use footprint | OpenEnv is PyTorch-native; shifts agent training back onto PyTorch; Google would have to port to OpenEnv or build a JAX variant from behind |

### OpenEnv RFC roadmap signals (what the framework is heading toward)

- **RFC 001** Core abstractions (Environment/Agent/Task) — base spec.
- **RFC 002** Env spec, packaging, isolation — Docker + FastAPI contract.
- **RFC 003** MCP tool support (landed v0.2.x) — Meta chose to align with Anthropic's MCP rather than compete.
- **RFC 004** Actions-as-tool-calls + **trajectory/delayed rewards** — the inflection. Moves OpenEnv from single-step RL toward long-horizon agentic RL with sparse rewards. This is where Meta wants community contributions.
- **RFC 005** Agentic harness integration.
- **Open ORS (Open Reward Standard)** issue #468 — community-standardized reward primitives. Meta wants reward-shaping to be a standard.
- **Open: ComtradeBench env PR #527** — proof the project accepts community envs.

Implication for our submission: an env with **trajectory rewards**, **MCP tool interface**, and **reward shaping that can be upstreamed as an ORS primitive** checks every RFC box simultaneously.

### Named Meta/HF humans with public OpenEnv footprints

- **Joe Spisak** (Product Director, MSL). The decision-maker on what OpenEnv becomes. Public 2026 goals: "productize a PyTorch-native agentic and RL stack; drive global standardization around open RL environments."
- **Sanyam Bhutani** (Partner Engineer, Meta; co-author of launch blog).
- **Davide Testuggine, Zach Wentz, Pierre Andrews, Hamid Shojanazeri, Pankit Thapar, Emre Guven** (Meta contributors on launch blog).
- **Lewis Tunstall (lewtun)** (HF; TRL lead; co-author of both launch + Turing blogs).
- **Ben Burtenshaw** (HF; OpenEnv scaling, environments like Visual Memory and Spreadsheet env; TRL integration author).
- **Christian Washington, Ankit Jasuja, Santosh Sah** (Turing Inc; Calendar-Gym authors).

These are the people whose public preferences you're optimizing for.

---

## PyTorch Foundation

### Role in the hackathons

- PyTorch Foundation is the neutral-governance host: it blesses events with the PyTorch brand, co-publishes blogs, programs conference-floor talks, and manages the RFC process for OpenEnv.
- Matt White (Executive Director): "The goal for 2026 is clear: make the PyTorch Foundation the go-to foundation for open source AI, a place where researchers, engineers, developers, and learners can find trusted projects, neutral governance, high-quality education, and a global community that welcomes participation."
- 2026 events include 3 PyTorch Conferences (San Jose, Paris, Beijing) + 3 PyTorch Days (India Feb 7, Dubai, China) — OpenEnv hackathon fits this global-developer-education strategy.

### How agent-envs benefit PyTorch adoption

- 2025-2026 is the tipping point where workloads shift from pre-training (where PyTorch/JAX parity exists) into **RL post-training + agentic inference** (where PyTorch has no incumbent moat). If PyTorch doesn't own this layer, JAX or a new framework could capture it.
- Joe Spisak (Meta, writing in PyTorch Foundation 2025 review): "PyTorch's strategic value is no longer about being 'just' a deep learning library; it's about anchoring a modular, community-driven, multi-hardware stack that spans the entire AI lifecycle."
- Luca Antiga (Lightning AI CTO, TAC Chair): "In 2026, PyTorch's footprint is going to grow both wide (training, inference, RL, agentic AI) and deep (out-of-core accelerators, kernel authoring, distributed infrastructure)."

### PyTorch's umbrella expansion is the tell

PyTorch Foundation expanded in 2025 to absorb: **vLLM** (inference), **DeepSpeed** (distributed training), **Ray** (distributed compute). This is the foundation explicitly becoming the AI OS, not just a tensor lib. OpenEnv is the next entry.

### JAX competitive angle

Officially PyTorch Foundation doesn't name JAX. But the structural play is clear:
- JAX has TPU-native advantages for training.
- OpenEnv + TorchForge + Monarch are built for RL-scale distribution on *any* hardware (NVIDIA, AMD, TPUs). Joe Spisak: "Our differentiation comes from openness and interoperability: a thriving developer community and first-class support for heterogeneous hardware."
- The PyTorch Foundation welcomed 16 new members in 2025 including Snowflake, Dell, Qualcomm. Every one of them is a "not-Google" infrastructure company. The coalition shape is: everyone-who-isn't-Google vs. Google's TPU+JAX stack.

### Signal from PyTorch Conference 2025 (Oct 22-24)

Meta launched 6 PyTorch-native projects at the conference simultaneously: ExecuTorch 1.0, TorchForge, Monarch, TorchComms, Helion, and OpenEnv. This is a *coordinated* stack-level offensive, not a set of independent projects. OpenEnv is the environment layer; TorchForge is the RL trainer; Monarch is distributed orchestration. The hackathon tests the whole stack in the community's hands.

---

## Cerebral Valley

### Business model (based on Newcomer disclosures + public partner list)

Cerebral Valley is run by **Eric Newcomer** (ex-Bloomberg reporter, runs Newcomer.co newsletter), co-founded with Volley's Max Child and James Wilsterman. Revenue > $1M/yr, profitable. Multiple revenue lines:

1. **Newsletter subscriptions** at $19/mo (5th most successful in Tech category on beehiiv).
2. **Sponsorship fees** for the flagship Cerebral Valley AI Summit + hackathons. Returning sponsors: Oracle OCI, HP, Lambda, Samsung Next, Amazon Alexa Fund, Mayfield, Obvious Ventures. New/partner tier: Sapphire Ventures, Latham & Watkins (law firm), Kleiner Perkins, Crusoe, Alkeon Capital, Pear VC.
3. **Corporate-partnership hackathons** where the sponsor (Anthropic, OpenAI, Google DeepMind, Mistral, Meta, Snowflake) pays CV to run a curated applicant-vetted hackathon — CV contributes the approved-applicant community and newsletter amplification.
4. **Deal flow surface for VC judges** — the ecosystem trade: Sequoia's Alfred Lin, Kevin Weil (OpenAI), Kanu Gulati, L.M. Braswell (GPT-5 hackathon judges) get first look at founders. Ali Ghodsi and Naveen Rao literally met at CV and that turned into Databricks' $1.3B MosaicML acquisition.

### What they gain beyond visible fees

- **First-look rights, not equity.** There is no public evidence CV takes equity. The value CV provides VCs is *earlier deal flow* than Y Combinator, plus the editorial power to write about the founders afterward.
- **Applicant vetting power.** The Claude Code Feb 2026 hackathon: 500 devs selected from 13,000 applications = 3.8% acceptance. That scarcity signal is itself a CV product.
- **Editorial anointing.** CV's beehiiv newsletter features "Emergent Behavior" / "cracked founders" — a winner featured in CV newsletter is instantly valuable in SF fundraising conversations.
- **Recurring sponsor lock-in.** Anthropic, Google, OpenAI, Meta, Mistral all ran CV hackathons in a ~18-month window. CV becomes the default "launch partner" for model launches.

### Judge-roster pattern (across CV events)

- **Model-lab hackathons** (Claude Code, GPT-5 Startup, LlamaCon, Gemini 3, Mistral MCP): judges are the **model's own PM/research leads** (Boris Cherny, Cat Wu, Jason Bigman, Lydia Hallie, Ado Kukic, Thariq Shihpar for Claude Code; Kevin Weil for GPT-5; Joe Spisak / Sanyam Bhutani for OpenEnv; Google DeepMind for Nano Banana).
- **VC seat on panel** is standard: Alfred Lin (Sequoia), Kanu Gulati, L.M. Braswell, partners from Mayfield/Kleiner/Sapphire rotate through.
- **Infra sponsor seat:** Fleet AI, Unsloth, Lambda, W&B appear as judge/mentor infra partners at OpenEnv SF.
- **Editorial seat:** Newcomer himself or CV staff present at finale pitches.

Implication for Bangalore finale: judges will likely include Meta's Spisak/Bhutani/Testuggine, HF's Tunstall/Burtenshaw, possibly Scaler execs (Saxena/Singh), and PyTorch Foundation rep. Same preference-vector as SF event.

### CV's preferences (what they publicly amplify)

- Real human at the center of the pitch (domain-expert builder, named first user).
- Domain-specific agents/envs, not generic chat demos.
- Live demo with a wow-moment.
- Sponsor's newest capability front-and-center.
- International / unexpected-background teams celebrated.
- Emotional arc + one technical brag per pitch.

(Full detail in round2/research/02-cerebral-valley-patterns.md — this is the strongest reverse-engineered signal we have.)

---

## Scaler School of Technology

### Why Scaler is the India host

SST was founded by **Abhimanyu Saxena and Anshuman Singh** (IIIT Hyderabad alums, also founders of InterviewBit + Scaler Academy). SST opened its 4-year undergraduate program (CS + AI) in Bangalore in 2023 with the explicit positioning: "India's Ivy League for the AI age." Scaler raised $76.5M across 3 rounds. SST's 4-year cost is ~₹24-25L; avg placement package ~21.6 LPA; first placement cycle (2025) placed 96% of interns at stipends averaging ₹30,000 with top at ₹200,000.

The Meta-hosted hackathon is SST's **biggest-ever brand-marketing leverage event**. Primary goals:

1. **Position SST above IITs for AI-specific positioning.** SST doesn't have IIT's legacy brand. What it *can* have: "the only undergrad school in India that co-hosts a Meta/PyTorch global hackathon finale on its campus." That's the NSET 2026-27 admission-cycle pitch.
2. **Convert hackathon into a direct placement funnel.** Press release language is explicit: winners get "direct interview opportunities with AI hiring teams at Meta and Hugging Face." Meta/HF interviews at SST's doorstep is exactly what justifies the ₹24L tuition to parents.
3. **Validate SST's "AI-native curriculum" rebrand.** Scaler announced in early 2026 that it was "India's first fully AI-native tech career platform" after spending months talking to 1,200+ hiring companies. Hosting a Meta RL hackathon is the proof point.
4. **Build a research-adjacent brand.** SST's students have already won Smart India Hackathon 2025 (₹1.5L from 68,766 teams), National GeoAI Hackathon at IIT Bombay, ICPC placements. Hosting OpenEnv is the capstone — a signal SST runs at international research-conference tempo.

### Pattern: is this Scaler's first such event?

- Not the first hackathon, but the **first with a global tier-1 AI lab as co-host**. SST runs monthly internal + external hackathons. Hosting the India Grand Finale of a Meta/PyTorch global series is the escalation.
- The CV→Scaler handoff pattern is the template. Expect this to recur: SST as the India host for future PyTorch Foundation global events. That's exactly why the event page says "organised by Scaler School of Technology in collaboration with Meta, Hugging Face, and PyTorch" — Scaler is *authoring* this relationship, not just hosting.

### What Scaler gains that isn't visible

- **Recruitment moat.** Every student photographed at the event, every project pushed to Meta's eval pipeline, every Meta-badge photo op, becomes a marketing asset.
- **Mentor-network building.** On-campus engagement with Meta + HF engineers creates durable mentor relationships for SST students.
- **Optics vs. IITs on AI.** IITs don't have a Meta-branded RL hackathon finale on their campuses. SST does. The "70,000 developers registering, 200+ problem statements from Meta" framing is positioning-as-content.
- **First-look at external RL talent** for SST's own Masters-in-AI pipeline (announced 2025-26).

### What Scaler wants from the submission

Scaler wants **submissions that are Meta-blessed, SST-student-authored, and India-relevant**. A submission that solves an India-specific problem (Indian languages, UPI/DigiLocker tool-use, transport/traffic envs, rural-healthcare triage) while being technically rigorous is *ideal for Scaler* because it generates press they can use in admissions marketing: "An SST team built an RL env for India's AADHAAR-linked benefits and got hired by Meta."

---

## Cross-Organizer Synthesis — the "perfect submission" profile

Put the 4 preference vectors together, and a single profile emerges. The submission that wins needs all 7 of these:

1. **A new RL environment, not a new model.** Meta and PyTorch Foundation explicitly want envs (the bottleneck); Cerebral Valley and Scaler want demos judges can point at. Build an env, post-train on it to prove the env works, ship the training curve as the hero screenshot.

2. **Long-horizon, multi-step, stateful, permissioned — with trajectory rewards.** Checks Calendar-Gym Turing blog, RFC 004, and Meta's stated product gap ("long-horizon agentic systems"). Short-horizon / single-step / dense-reward envs are the opposite of what they want.

3. **MCP tool interface as the action schema.** Checks RFC 003 (Anthropic-compatible). Signals ecosystem fluency. Every action an MCP tool call with typed params.

4. **A domain Meta FAIR wouldn't reach alone.** CV's bonus-prize formula. India-native: Indian languages, UPI tool-use, DigiLocker + AADHAAR workflow agents, Indian-tax-code reasoning, Indian-legal-code QA, rural-telemedicine triage, regional-transport routing. Scaler also wants this for admissions-marketing.

5. **A training curve screenshot that a Meta engineer will tweet.** Reward-improvement curve + a short demo video. Clip-worthy 15-30 second "magic" moment.

6. **A named first user.** CV-style pitch opening. "We built this because [name] — a [specific domain role] — can't currently do X." Avoid generic personas.

7. **Upstream-contribution framing.** Open PR to OpenEnv repo. Propose a reward primitive for the ORS issue #468. Mention the RFC-004 compatibility. Signal: "we are not leaving this at the hackathon; we're shipping this into the framework." PyTorch Foundation and Meta both reward this behavior publicly.

### The ideal-submission sentence (that hits all 4 organizers simultaneously)

> "We built an OpenEnv-compatible RL environment for **[India-specific long-horizon tool-use domain]** with **MCP-compatible trajectory rewards**, post-trained **gpt-oss-20b** with **Unsloth+TRL GRPO** on free Colab, and our Meta CWM-style verifier shows a **+X%** improvement curve — here's our 20-second demo of [named first user] using it, and here's the PR upstreaming the env + a reward primitive to the OpenEnv repo."

That sentence is designed to make:
- Meta say: "this advances long-horizon agentic systems and coding workflows, our stated gap"
- PyTorch Foundation say: "this is exactly the RL post-training + community-env standardization we want"
- Cerebral Valley say: "real user, sponsor model + sponsor stack, clip-worthy demo, India-hustle narrative"
- Scaler say: "India-specific, SST-student-authored, Meta/HF-eligible hire"

---

## What Meta Would Want to See That It Hasn't Yet (the gap we can fill)

Cross-referencing the 29 envs already in OpenEnv with FAIR's research agenda and MSL's publicly stated gaps yields a clear underserved quadrant:

1. **Long-horizon SaaS multi-tool workflows** — Calendar-Gym is *one* API. Nothing yet covers Slack+Gmail+Notion+Jira+Linear together. Meta's Q1 2026 earnings said "long-horizon agentic systems" is their gap. This is the highest-signal gap.
2. **India-specific tool-use domains** — zero envs wrap UPI, DigiLocker, AADHAAR, Setu, IRCTC, Zerodha-style Indian financial APIs. Given Scaler's India hosting, an India-native env is both CV-pleasing (international hustle) and strategically unclaimed.
3. **SWE-Gym-style real bug-fixing env** — explicitly referenced in the CWM paper as the training target, not in OpenEnv yet. Direct FAIR-agenda alignment.
4. **Clinical/biomedical decision-support with permissioned EHR-like state** — `dipg_safety_env` is narrow; no realistic ACL-permissioned clinical env.
5. **Spreadsheet / Excel reasoning env** — Burtenshaw already hinted at a Spreadsheet env; there's framework-author interest but no production-grade env. Spreadsheet = long-horizon + tool-use + structure-aware = an ideal CWM-training target.
6. **Mobile/AndroidWorld agent env** — desktop covered (browsergym/openapp), mobile absent. Hot research area, zero OpenEnv presence.
7. **Cybersecurity / CTF env with MCP tools** — nothing yet. Natural long-horizon tool-use target.
8. **Mechanistic-interpretability eval-as-env** — Team AAA won Llama 3 with this thesis. Safety-eval-as-RL-env is an orthogonal axis no one's pursued.

The strongest bet combining all axes: **India-SaaS-multi-tool env** (e.g., DigiLocker + UPI + IRCTC workflow), **MCP-compatible**, **trajectory-reward**, with a **permissioned state model** following Calendar-Gym's design. This is a single submission that is Meta's stated gap + Scaler's India positioning + CV's "domain-specific beats generic" + PyTorch Foundation's "community-contributed env."

---

## Hackathon Circuit Pattern Analysis (what consistently wins across Meta events 2024-2026)

Looking at **Llama 3 Hackathon (May 2024)**, **Llama Impact Hackathons (London 2024, Pan-LATAM 2025, Bengaluru 2024, Sub-Saharan Africa 2025)**, **LlamaCon 2025 (May 2025)**, **OpenEnv SF (Mar 2026)**, **Unsloth×PyTorch×AMD RL Envs Hackathon (Oct 2025)**, **AgentX-AgentBeats OpenEnv Challenge track (Mar 2026)**:

### What Meta consistently rewards

1. **Real domain, not demo-ware.** Llama Impact winner Guardian (A&E triage). LlamaCon winner OrgLens (enterprise knowledge graph). Meta Llama 3 winner OpenGlass (physical DIY hardware).
2. **Showcases the *newest* Meta capability.** LlamaCon 2025: Llama 4 multimodal is the hero feature, so CCTV (multimodal video) and Geo-ML (multimodal reasoning) win. OpenEnv's "newest capability" is MCP actions + trajectory rewards — submissions need to show *those*.
3. **Open-source contribution as part of the pitch.** Meta loves winners who upstream. Llama Impact winners routinely apply to Llama Impact Grants afterward.
4. **Social-good/impact angle.** Llama Impact program explicitly prioritizes "healthcare, clean energy, social mobility." Even in commercial events, impact framing bonus-scores.
5. **Mechanistic/interpretability depth.** Team AAA winning Llama 3 with activation-layer jailbreak defense — the rare "research-paper-style" winner, signals Meta rewards technical depth.

### What winners get post-event

- Llama Impact Hackathon London 2024: top 3 teams split **$50K** + **6 weeks of technical mentorship** + eligibility for regional/global grants.
- Llama Impact Grants: up to **$500K** per grant, $300K for runner-up.
- LlamaCon 2025: no explicit mentorship path advertised but several winners subsequently absorbed into Meta's extended network (Waddle/Gentoo grew into a company with US subsidiary, 6 months after winning OpenAI's hackathon).
- OpenEnv India (Apr 2026): "direct interview opportunities" with Meta + HF AI teams. Official Meta certificates.
- OpenEnv Challenge (AgentX-AgentBeats): winners published on **PyTorch blog** + HF credits. Public research-visibility reward.

### Research questions Meta is implicitly sourcing answers to via the community

Across the RFC list + the Calendar-Gym findings + the CWM paper's gaps, Meta is effectively asking the community:

1. What reward structures work for long-horizon, sparsely-rewarded agentic tasks? (RFC 004 + ORS)
2. What's the right way to express real-world tool permissions/ACLs as env state? (Calendar-Gym)
3. Can we scale environment throughput to 10K+ concurrent episodes on commodity infra? (Burtenshaw scaling blog)
4. What envs produce transferable agentic skills, not just env-specific overfitting?
5. What does a mobile/GUI-native env look like in OpenEnv's idiom?
6. How do we train reward models that generalize across environments (the ORS pitch)?

A submission that explicitly answers one of these (even partially) punches far above its demo weight.

### What they would DISLIKE even if technically strong

- **A generic "chat-with-docs" RAG demo.** Zero alignment; every CV event has shown these don't win.
- **A new model without a new environment.** Meta has models. They want envs.
- **A model trained in a non-PyTorch stack** (pure JAX, pure TF). Kills PyTorch Foundation alignment.
- **A closed/proprietary env.** Contradicts the "open" in OpenEnv. PyTorch Foundation neutrality requires BSD-3-or-similar-compatible licensing.
- **A deep fine-tune without reward-curve evidence.** Judging weight 20% is literally reward improvement.
- **An env that doesn't work out-of-the-box.** OpenEnv spec is strict — if your Docker container doesn't respond to `reset/step/state`, demo fails.
- **Slide-heavy pitches.** CV explicitly penalizes.
- **A solo narrative without a real user.** Even solo-builder winners have named first users (Elisa's daughter, CrossBeam's contractors).

---

## Appendix: Quotes / Sources

### Verbatim quotes to reference in the pitch

- Clem Delangue (HF CEO, Oct 2025): "The next wave of AI will be defined not just by open models, but by open environments."
- Joe Spisak (Meta, PyTorch Foundation 2025 retrospective): "Productize a PyTorch-native agentic and RL stack... drive global standardization around open RL environments."
- Joe Spisak: "PyTorch's strategic value is no longer about being 'just' a deep learning library; it's about anchoring a modular, community-driven, multi-hardware stack that spans the entire AI lifecycle."
- Matt White (PyTorch Foundation ED, 2026): "Make the PyTorch Foundation the go-to foundation for open source AI."
- OpenEnv launch blog: "Agentic environments define everything an agent needs to perform a task: the tools, APIs, credentials, execution context, and nothing else."
- OpenEnv + Turing Calendar-Gym blog (Feb 2026): "Agents achieved close to 90% success on tasks with explicit calendar identifiers, but success dropped to roughly 40% when the same tasks were phrased using natural language descriptions... more than half of errors stemmed from malformed tool arguments or incorrect ordering."
- Meta Q1 2026 earnings: "We continue to invest in areas with current performance gaps, specifically long-horizon agentic systems and coding workflows."
- Ben Burtenshaw (HF): "RL post-training is bottlenecked by environment throughput, not compute."

### Primary sources (linked)

- OpenEnv launch blog: https://huggingface.co/blog/openenv
- OpenEnv-Turing Calendar-Gym blog: https://huggingface.co/blog/openenv-turing
- OpenEnv scaling blog (Burtenshaw): https://huggingface.co/blog/burtenshaw/openenv-scaling
- Meta PyTorch-native agentic stack blog: https://ai.meta.com/blog/introducing-pytorch-native-agentic-stack/
- PyTorch Foundation 2025 year-in-review: https://pytorch.org/blog/pytorch-foundation-in-2025-a-year-in-review/
- PyTorch Conference 2025 schedule: https://pytorchconference.sched.com/
- OpenEnv Hackathon SF (CV event page): https://cerebralvalley.ai/e/openenv-hackathon-sf
- OpenEnv Hackathon SF (PyTorch event page): https://pytorch.org/event/openenv-hackathon-sf/
- OpenEnv India / Scaler event page: https://www.scaler.com/school-of-technology/meta-pytorch-hackathon
- OpenEnv India PyTorch event page: https://pytorch.org/event/openenv-ai-hackathon/
- AgentX-AgentBeats OpenEnv Challenge: https://pytorch.org/event/agentx-agentbeats-competition-agentic-rl-and-environments-workshop/
- AgentX-AgentBeats announcement: https://rdi.berkeley.edu/agentx-agentbeats.html
- OpenEnv RFC 004 (actions-as-tool-calls + trajectory rewards): https://github.com/meta-pytorch/OpenEnv/blob/main/rfcs/004-actions-as-tool-calls.md
- CWM paper: https://arxiv.org/abs/2510.02387
- CWM GitHub: https://github.com/facebookresearch/cwm
- Cerebral Valley hackathons hub: https://cerebralvalley.ai/hackathons
- Cerebral Valley newsletter: https://cerebralvalley.beehiiv.com/
- Newcomer on CV: https://www.newcomer.co/p/meet-the-cerebral-valley-heavy-weights
- Joelle Pineau departure: https://www.cnbc.com/2025/04/01/metas-head-of-ai-research-announces-departure.html
- Soumith Chintala departure tweet: https://x.com/soumithchintala/status/1986503070734557568
- Yann LeCun AMI Labs: https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/
- Muse Spark release: https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html
- Scaler School of Technology main page: https://www.scaler.com/school-of-technology
- Scaler SIH 2025 win / student outcomes: https://www.scaler.com/school-of-technology/campus-life
- Scaler AI-native announcement: https://www.tribuneindia.com/news/advertorial-disclaimer/scaler-becomes-indias-first-fully-ai-native-tech-career-platform-finds-only-19-of-engineers-are-truly-ai-ready
- Llama Impact Hackathon London: https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/
- Llama Impact Grants page: https://llama.meta.com/llama-impact-grants/
- LlamaCon 2025 recap: https://ai.meta.com/blog/llamacon-hackathon/
- Meta Llama 3 Hackathon recap: https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/
- Ecosystem taxonomy (Mar 2026): https://leehanchung.github.io/blogs/2026/03/21/rl-environments-for-llm-agents/
- Kalinga coverage of India hackathon: https://kalinga.ai/openenv-ai-hackathon-india-2026/
