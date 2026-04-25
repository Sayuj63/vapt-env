# Cerebral Valley Hackathon Patterns

> Research target: reverse-engineer what wins at CV-judged AI hackathons, in service of winning the Meta PyTorch OpenEnv Hackathon Grand Finale (Bangalore, Apr 25-26 2026).
> Finalist judging weights at stake: 40% Innovation, 30% Storytelling, 20% Reward Improvement, 10% Pipeline.

---

## What Wins at CV-Judged Events (Executive Summary)

Across 10+ CV-run hackathons (LlamaCon, Llama 3, GPT-5 Startup Hackathon, Built with Opus 4.6, Nano Banana, WeaveHacks, Mistral MCP, Gemini 3, OpenEnv SF), a remarkably consistent winner profile emerges:

1. **Real problem, real user on stage.** 1st-place projects almost always name a concrete, empathetic first user ("my 12-year-old daughter", "California ADU builders", "cardiology patients", "beta-test e-commerce clients getting +36% revenue"). CV judges reward "this is shipping to someone I can point to" over "this is theoretically cool".
2. **Domain specificity beats general AI demos.** Winners pick a narrow vertical (housing permits, A&E triage, geology reports, Jira+GitHub knowledge graphs, compliance/fraud) and go deep. Generic "chat with X" agents don't medal.
3. **Model-hero storytelling.** Winners explicitly demo a capability of the *sponsor's* model that wasn't possible before: 1M context for legal/permit PDFs, Llama 4 multimodal for CCTV, GPT-5's agentic loop for e-commerce, 15ms WASM inference for music. CV judges reward "this is the killer use-case for *your* model".
4. **Live, working demo with wow-factor moment.** Every CV winner has a single 15-30 second magic beat the pitch is built around (glasses naming a fruit and giving calories; MIDI keyboard spawning a generative band; CCTV detecting a defined event). Slide-heavy pitches lose.
5. **Hustle + narrative arc.** Solo founders or 2-4 person teams with a personal story (musician in Estonia, cardiologist in Belgium, lawyer in California, Seoul team flying in) win disproportionately. CV's judges (VCs, model-company PMs, journalists) reward "founder-market fit" visible in 3 minutes.
6. **Sponsor-bonus prizes go to deepest integration.** "Best Llama API Usage" (Geo-ML) went to the project that built a domain-specific language compiler on top of Maverick. Integrating many sponsor tools (W&B Weave for observability, Groq for inference speed, SambaNova, Fal, ElevenLabs, Nebius) is explicitly rewarded.

Implication for the OpenEnv Bangalore Grand Finale: the winning story is "we picked a domain nobody else would touch, post-trained a model in a novel RL environment, and shipped a reward curve that makes a Meta engineer say 'oh, that's the killer demo of OpenEnv'." Innovation (40%) + Storytelling (30%) means the pitch matters as much as the pipeline.

---

## Notable Winners (13 projects across CV events)

### 1. OrgLens - LlamaCon Hackathon 2025 (1st Place)
- **One-liner:** AI-powered internal expert-matching; maps Jira + GitHub + docs + resumes into a knowledge graph so you can find who inside your org knows X.
- **Team:** TheCl3m et al. (SF-based, indie builders).
- **GitHub:** https://github.com/TheCl3m/llama-hack
- **Demo video:** https://www.youtube.com/watch?v=9g9UH62sihk
- **Event:** LlamaCon Hackathon, SF, May 3-4 2025 (Meta + Cerebral Valley + SHACK15, 238 devs, 44 projects, $35K prize pool).
- **Why it won:** Real enterprise pain point (knowledge silos), ambitious multi-source data integration, "digital twin" interaction demo had an emotional beat. Used Llama API for embedding + reasoning across heterogeneous data. Tech stack: React, Tailwind, Django, GitHub API, Llama API.
- **Sponsor alignment:** Deep Llama API usage across retrieval + ranking + chat.

### 2. Compliance Wizards - LlamaCon Hackathon 2025 (2nd Place)
- **One-liner:** AI transaction fraud analyzer with email alerts and a voice-AI assistant for reporting.
- **GitHub:** https://github.com/michaelwaves/llamacon-hackathon
- **Why it won:** Used Llama's multimodal capability to ingest client info + news; clear enterprise-safety vertical; live voice-assistant demo was the wow moment.

### 3. Llama CCTV Operator - LlamaCon Hackathon 2025 (3rd Place)
- **Team lead:** Agajan Torayev
- **One-liner:** Zero-fine-tuning surveillance: describe the event in plain English, Llama 4 multimodal scans video every 5 frames and flags it.
- **GitHub:** https://github.com/torayeff/llamacon-hackathon-2025-sf/
- **Demo video:** https://www.youtube.com/watch?v=zPn4ogg4xM0
- **Why it won:** Directly showcased Llama 4's new multimodal capability against a physical, relatable domain; "no fine-tuning" is a classic CV-winning line because it proves the base model is the product.

### 4. Geo-ML - LlamaCon Hackathon 2025 (Best Llama API Usage)
- **Developer:** William Davis
- **One-liner:** Turns 400-page geology reports into a structured DSL that auto-generates 3D geological models (dig sites, mineral deposits).
- **GitHub:** https://github.com/williamjsdavis/geo-lm
- **Stack:** Llama 4 Maverick + GemPy
- **Why it won sponsor bonus:** This is the canonical "sponsor prize" archetype - the deepest, most creative use of the *specific* model (Maverick's reasoning) in a domain (geoscience) the sponsor would never have reached on their own.

### 5. OpenGlass - Meta Llama 3 Hackathon (1st Place, 2024)
- **One-liner:** $20 DIY smart glasses that identify what the wearer is looking at (fruits, calorie counts, etc.).
- **GitHub:** https://github.com/BasedHardware/openglass
- **Event:** Meta Llama 3 Hackathon hosted by Meta AI + Cerebral Valley + SHACK15, 1,200+ apps, 354 attendees, 51 projects in 24h.
- **Why it won:** The perfect CV demo - cheap hardware + live object recognition = visible "magic". The pitch literally had the presenter point glasses at fruit and read the calories aloud. Unbeatable storytelling hook.

### 6. Deb8 - Meta Llama 3 Hackathon (2nd Place)
- **One-liner:** Lincoln-Douglas debate arena where multiple LLMs argue and a 3rd-agent judge scores them.
- **Why it won:** Novel agent-orchestration pattern that doubles as model-evaluation entertainment; perfect for a model-company sponsor because it surfaces model behavior in a comparative way.

### 7. Team AAA (Activation Ablation Augmentation) - Meta Llama 3 Hackathon (3rd Place)
- **One-liner:** Mechanistic-interpretability attack/defense - new jailbreaks by neutralizing Llama 3 activation layers.
- **Why it won:** Technical-depth signal to AI-safety judges; demonstrated understanding of the model internals, not just the API. Rare "research" winner in a demo-heavy field.

### 8. CrossBeam - Built with Opus 4.6 Claude Code Hackathon (1st Place, Feb 2026)
- **Founder:** Michael T. Brown, a California attorney (personal injury + real estate).
- **One-liner:** Reads architectural plans + city correction letters + CA state law, auto-generates a professional response package for ADU permits.
- **GitHub:** https://github.com/mikeOnBreeze/cc-crossbeam
- **Event:** Virtual, Feb 10-16 2026, 500 devs selected from 13,000 apps, $100K API credits grand prize. Judges: Boris Cherny, Cat Wu, Thariq Shihpar, Lydia Hallie, Ado Kukic, Jason Bigman.
- **Why it won:** Lawyer (non-engineer) building a tool that saves builders weeks - ultimate "Claude Code unlocked a new class of builder" narrative. Opus 4.6's 1M context window was the enabling capability (whole permit packets in context). Aligned perfectly with Anthropic's messaging about expanding the builder pool.

### 9. Elisa - Built with Opus 4.6 (2nd Place)
- **Builder:** Jon McBee (Massachusetts dev).
- **One-liner:** Snap-together visual programming for kids; Claude spawns agents that produce real code behind the blocks. First user: his 12-year-old daughter.
- **Why it won:** Emotional hook + agent-orchestration showcase. The "my daughter is the first user" line is a textbook CV-winning storytelling move.

### 10. postvisit.ai - Built with Opus 4.6 (3rd Place)
- **Founder:** Michal Nedoszytko MD, PhD - a cardiologist in Belgium.
- **One-liner:** Turns a doctor visit transcript + medical records into personalized ongoing health guidance.
- **Why it won:** Domain expert as builder (high credibility), serious outcome ("improve treatment"), and a relatable empathy hook. CV loves MDs/lawyers/domain professionals shipping code.

### 11. Conductr - Built with Opus 4.6 ("Most Creative Opus 4.6 Exploration")
- **Builder:** Asep Bagja Priandana (Nanas Sound, Estonia; musician).
- **One-liner:** Play chords on a MIDI controller; Claude directs a 4-track generative band around you at ~15ms latency (C/WASM engine).
- **Demo:** https://www.youtube.com/watch?v=X6CqJoyj0kI
- **Why it won creative category:** Real-time human-AI collaboration, live-performance wow factor, and technical chops (custom WASM inference engine for latency). Exactly the profile for a "creative/exploration" bonus prize.

### 12. Waddle / Gentoo - OpenAI GPT-5 Startup Hackathon (1st Place, Aug 2025)
- **Team:** CEO Park Ji-hyuk + engineers Song Jin-tae, Han Sang-do, Hwang Tae-baek (Seoul-based, flew in).
- **One-liner:** "Digital salesperson" for e-commerce - detects shopper hesitation in real time and nudges to purchase using GPT-5's agentic loop.
- **Press:** PR Newswire, Yahoo Finance, Korea Tech Desk. Grew into Waddle Labs, launched US subsidiary Feb 2026.
- **Event:** SF, Aug 2025, 275 builders, 93 teams, 24-48 hours. Prize: DevDay tickets + $50K OpenAI credits + ~$85K in partner credits. Judges: Alfred Lin (Sequoia), Kevin Weil (OpenAI), Kanu Gulati, L.M. Braswell.
- **Why it won:** Beta results baked into the pitch ("+36% monthly revenue, +30% orders in beta") - "Reward Improvement" proven before judging. Clear revenue thesis, sharp vertical, international hustle narrative.

### 13. LifeTrace Timeline / ArtLens / ForgeOne - Nano Banana Hackathon (Sep 2025 winners)
- **Event:** Google DeepMind + Cerebral Valley, SF + global virtual, 48h, 50 winners sharing $400K in prizes ($5K Gemini credits + $1K Fal + $2K ElevenLabs each).
- **LifeTrace Timeline:** Converts phone location data into a personal diary (consumer emotional hook).
- **ArtLens:** Reimagines classical paintings as scenes from everyday reality (viral shareability).
- **ForgeOne:** Self-evaluating workflow that reviews and improves its own image outputs (agentic meta-loop).
- **Pattern:** CV rewarded projects that made Gemini 2.5 Flash Image feel magical in a consumer context, not enterprise ones.

---

## Pitch Style Patterns Observed

1. **Open with a human, not an architecture diagram.** OpenGlass opened by pointing glasses at fruit. Elisa opened with "my 12-year-old daughter used this." CrossBeam opened with a CA contractor's pain. Every winner opens with a human in the scene.
2. **The "impossible last year" line.** Winners explicitly call out what the sponsor's new model enabled: "1M context means I can fit the whole plan packet in one call" / "Llama 4 multimodal means no fine-tuning" / "GPT-5 agentic loop means a salesperson that converts." Judges (who are often the model's PMs) love this.
3. **One live demo beat, no slides around it.** The pitch structure that keeps appearing: 30s problem setup -> 60-90s live demo -> 30s traction/roadmap. Slide-only pitches consistently lose.
4. **Named first user.** "My daughter", "a cardiologist in Belgium", "a contractor in Riverside County", "beta clients with +36% revenue". Abstract personas never win.
5. **Technical credibility signal inside the demo.** Conductr dropped "15ms latency on C/WASM". Geo-ML dropped "DSL compiling to GemPy". Team AAA dropped "neutralizing activation layers". One technical brag, concrete and specific, inside the 3-minute pitch.
6. **International / unexpected backgrounds celebrated.** Estonia musician, Korean startup, Belgian cardiologist, Massachusetts solo dev, California lawyer. CV press-amplifies unusual-provenance winners.
7. **Close with a roadmap, not a thank-you.** Waddle closed with US expansion. CrossBeam closed with statewide housing-shortage framing. Pipeline (10% of judging weight here) is demonstrated by a one-line future story.

---

## Judges' Known Preferences

- **Alfred Lin (Sequoia, GPT-5 judge):** Publicly praised "teams that hustled their way across the world" and "made useful things in 48 hours". Implication: travel story + utility beats polish.
- **Kevin Weil (OpenAI):** Rewards teams that stress-test the newest model capability (agentic calls, long-horizon tool use).
- **Anthropic Claude Code judges (Boris Cherny, Cat Wu, Jason Bigman, Lydia Hallie, Ado Kukic, Thariq Shihpar):** Published evaluation axes: technical innovation, implementation quality, potential impact. Winners skewed heavily toward *non-engineer* builders (lawyer, cardiologist, musician) because that validates Claude Code's "expands the builder pool" thesis - the sponsor narrative matters.
- **Meta/Llama judging (LlamaCon 2025):** Deliberation ran over an hour; popular winning categories were video/multimodal, virtual AI agents, and mixture-of-experts demos - exactly where Meta wants Llama to be perceived as leading.
- **Cerebral Valley's own editorial lens (beehiiv newsletter):** Featured "Emergent Behavior" demos, first-time reveals, "cracked founders", and cutting-edge infra. CV's public writeups amplify winners that look like demo-day startups, not research papers.

---

## Bonus Prize Win Patterns

Sponsor bonus prizes ("Best Llama API Usage", "Most Creative Opus Exploration", "Best W&B Weave Integration", "Best Groq Inference", etc.) follow a distinct formula:

- **Push the sponsor's model into a domain they'd never reach alone.** Geo-ML (geology) won Best Llama API Usage precisely because Meta would never independently build a geoscience DSL.
- **Show integration depth, not breadth.** Don't namedrop 5 sponsors; use 1-2 of them at the core of the demo's capability (e.g., Groq for sub-100ms inference making the UX feel alive).
- **Use the sponsor's most differentiated capability.** Llama 4 multimodal for video (CCTV, Geo-ML). Opus 4.6 1M context for full-document ingest (CrossBeam). GPT-5 agentic loop for multi-step sales (Gentoo). Gemini 2.5 Flash Image iterative self-eval (ForgeOne).
- **Give the sponsor's PM a quotable demo moment.** Every bonus-prize winner has a 10-second clip the sponsor can tweet. Build for that clip.

For the OpenEnv Bangalore finale, the bonus-prize analog is the "Reward Improvement" 20% weight - the equivalent move is picking an RL environment + benchmark where your post-training curve is the screenshot a Meta engineer will put in a tweet. Make it clip-worthy.

---

## Sources

- LlamaCon Hackathon 2025 winners (Meta AI blog): https://ai.meta.com/blog/llamacon-hackathon/
- LlamaCon 1st place OrgLens demo video: https://www.youtube.com/watch?v=9g9UH62sihk
- LlamaCon 3rd place CCTV Operator demo: https://www.youtube.com/watch?v=zPn4ogg4xM0
- Meta Llama 3 Hackathon recap: https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/
- OpenGlass GitHub: https://github.com/BasedHardware/openglass
- Built with Opus 4.6 Hackathon page: https://cerebralvalley.ai/e/claude-code-hackathon
- CrossBeam (Opus 4.6 1st place): https://github.com/mikeOnBreeze/cc-crossbeam ; https://hadleylab.org/blogs/2026-03-22-the-lawyer-who-won
- Conductr (Opus 4.6 creative prize): https://www.youtube.com/watch?v=X6CqJoyj0kI
- OpenAI GPT-5 Startup Hackathon winner (Waddle/Gentoo): https://x.com/OpenAIDevs/status/1955774992043663418 ; https://koreatechdesk.com/waddle-gpt-5-hackathon-win-showcases-korean-ai-competitiveness-global-stage
- Nano Banana Hackathon (DeepMind + CV): https://cerebralvalley.ai/e/nano-banana ; https://edgespace.substack.com/p/google-deepmind-reveals-winners-of
- OpenEnv Hackathon SF (predecessor to Bangalore finale): https://cerebralvalley.ai/e/openenv-hackathon-sf ; https://pytorch.org/event/openenv-hackathon-sf/
- Bangalore finale: https://www.scaler.com/school-of-technology/meta-pytorch-hackathon
- CV hackathon gallery hub: https://hackathons.cerebralvalley.ai/
- CV newsletter (beehiiv): https://cerebralvalley.beehiiv.com/
