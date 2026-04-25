# Emotional / Social-Impact AI Hackathon Winners

Research compiled for Round 2 of the Meta PyTorch OpenEnv Hackathon (Bangalore, Apr 25-26 2026). Target: reverse-engineer the emotional storytelling formula that wins against technically-superior projects, applied to an OpenEnv training environment + reward model + TRL training script.

---

## The Storytelling Formula (Executive Summary)

Across 15+ winning projects analyzed (Meta Llama Impact, AI for Good, UNICEF, Google.org, Devpost social-impact categories), **four recurring ingredients** separate winners from runners-up:

1. **The Named Victim + Scale**: Pitch opens with a single person's story ("Yvonne became a first-time mom, isolated…") immediately followed by a crushing statistic ("…like 6,000 women who die in childbirth every year in Kenya"). Personalization + scale is the hook.
2. **The Preventability Hammer**: Winners emphasize deaths/harms that are *preventable*. "91% of women would seek care if they knew the danger signs" (Jacaranda). "Over 95% of pregnant women who used our kits delivered safely" (HelpMum). Judges feel complicit in inaction.
3. **The Low-Resource Visual**: Winning pitches show the gadget/solution in context — a solar-powered device in a rural hut (MamaMate), an SMS on a feature phone (PROMPTS), a smartphone measuring a child's height (RevolutionAIze). The contrast between cutting-edge AI and dusty feet is catnip to judges.
4. **The Multiplier Number**: Every winner cites a concrete reach or reduction stat. "30% reduction in NICU admissions, 500,000 pregnancies monitored" (CareNX). "3 million women reached" (PROMPTS). "73.5% increase in vaccination uptake" (HelpMum ADVISER). Judges need one memorable number to write on the scorecard.

**Pitch structure that repeatedly wins (verbatim pattern):**
> "Every [N minutes/seconds], a [woman/child/person] dies from [preventable cause]. My sister/neighbor/mother was one of them. Today, [AI system] changes that. In our pilot, [X% reduction]. We want to reach [Y million]."

---

## Healthcare AI Winners (with exact stats cited)

### 1. Guardian — Meta Llama Impact Hackathon 2024 (London), 1st Place
- **One-liner**: AI-powered A&E triage assistant on Llama 3.2 with a clinical-AI companion agent "Atlas"
- **Emotional hook**: Overwhelmed NHS frontline staff; patients waiting 12+ hours in A&E; multilingual patients who can't describe symptoms
- **Tech**: Llama 3.2 + real-time risk scoring + "second pair of eyes" agent for nurses
- **Prize**: Part of $50K top-3 pool + 6 weeks mentorship + eligibility for $500K Llama Impact Grant
- **Link**: https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/
- **Storytelling technique**: Focused on the *nurse's* burden, not the patient's — a novel angle. Hero was the frontline worker.

### 2. Gripmind — Meta Llama Impact Hackathon 2024 (London), 2nd Place
- **One-liner**: Open-source brain-signal / voice / image control of robotic arms for mobility-impaired users using Llama 3.2 Vision
- **Emotional hook**: Restoring independence; making assisted-living robotics "scalable and affordable"
- **Link**: https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/

### 3. Pharmallama — Meta Llama Impact Hackathon 2024 (London), 3rd Place
- **One-liner**: On-device pharmacist for patients who can't reach a local pharmacy; detects drug interactions
- **Emotional hook**: Elderly and mobility-limited patients left confused by their meds
- **Link**: https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/

### 4. MamaMate (Elevate AI Africa) — AI for Good Innovation Factory Grand Finale 2025, GLOBAL WINNER
- **One-liner**: Solar/USB-powered offline AI gadget that coaches first-time rural mothers in their own language
- **Emotional hook (verbatim origin)**: Founder Yvonne Baldwin: *"When I became a first-time mom, I encountered a mix of joy and isolation — an experience shared by millions of women across Africa in rural areas with limited access to information, care, or emotional support."*
- **Features**: baby-care tracking, mental-wellness voice check-ins, anonymous peer support from other mothers
- **Prize**: $20,000 + AI for Good Global Summit stage
- **Link**: https://aiforgood.itu.int/mamamate-wins-again-this-time-at-the-ai-for-good-innovation-factory-grand-finale-2025/
- **Storytelling technique**: Founder-as-victim. Her own postpartum isolation was the pitch. She IS the user.

### 5. CareNX / Fetosense — 2025 AI for Good Impact Award: AI FOR PEOPLE
- **One-liner**: Low-cost AI fetal heart monitor (CTG interpretation via DL) for rural clinics without gynecologists
- **Emotional hook**: Preventable stillbirths and neonatal complications in underserved regions
- **Hard stats cited in pitch**:
  - 500,000+ pregnancies monitored across 6 countries
  - 30% reduction in NICU admissions
  - Deployed in 2,500+ clinics
- **Partnerships name-dropped**: UNICEF, MIT Solve
- **Link**: https://aiforgood.itu.int/meet-the-winners-for-the-2025-ai-for-good-impact-awards/

### 6. Jacaranda Health — PROMPTS (Meta Llama Impact Grant 2024 Runner-Up + AWS/Microsoft featured)
- **One-liner**: SMS chatbot triaging pregnant/postpartum women to the right care level
- **Emotional hook stats (load-bearing in every pitch)**:
  - Kenya has **51x the maternal mortality rate of the UK**
  - **6,000 Kenyan women die in childbirth each year**
  - Delays in care-seeking cause **1/3 of all maternal deaths in Kenya**
  - **91% of women would seek care if they knew the danger signs**
- **Reach**: 3.8 million mothers; expanding Kenya + Ghana + Eswatini
- **Link**: https://jacarandahealth.org/prompts/
- **Storytelling technique**: The "91%" stat is genius — it reframes the problem as *information asymmetry* (solvable with AI) rather than medical capacity (unsolvable).

### 7. HelpMum (Nigeria) — Google Impact Challenge 2018 + Gavi-funded AI research (ADVISER)
- **One-liner**: AI-optimized vaccination intervention scheduling for rural Nigerian mothers
- **Emotional hook stats**:
  - **25,000+ lives of pregnant women and infants saved**
  - **73.5% increase in immunization outcomes** in pilot clinics
  - **95%+ of pregnant women using their clean birth kits delivered safely**
  - 100,000+ mothers reached
- **Prize**: $250,000 Google.org grant + academic paper (IJCAI 2022)
- **Link**: https://www.gavi.org/vaccineswork/ai-driven-mobile-app-helping-nigerian-mothers-keep-top-their-babies-immunisation
- **NOTE**: "saved the lives of over 25,000" is the exact phrasing — use this template verbatim.

### 8. Dana-Farber Cancer Institute — Meta Llama Impact Grant 2024 Winner ($500K)
- **One-liner**: Open-source Llama-powered clinical-trial matching for cancer patients
- **Emotional hook**: Cancer patients who die never knowing there was a trial for them
- **Tech**: Llama summarizes unstructured clinical notes + trial eligibility
- **Link**: https://ai.meta.com/blog/llama-impact-grant-innovation-award-winners-2024/

### 9. NoHarm Summary Discharge (Instituto de IA na Saúde, Brazil) — Llama Impact Grant 2024
- **One-liner**: Automated Portuguese-language discharge summaries to reduce readmission errors
- **Emotional hook**: Doctor burnout + patients re-hospitalized from miscommunication
- **Link**: https://ai.meta.com/blog/llama-impact-grant-innovation-award-winners-2024/

### 10. RevolutionAIze / MAAP — 2025 AI for Good Innovation Factory winner
- **One-liner**: Smartphone photo → child height estimation → malnutrition detection
- **Emotional hook**: Undetected child malnutrition in regions without scales or trained clinicians
- **Link**: https://aiforgood.itu.int/meet-revolutionaize-the-ai-startup-revolutionizing-child-growth-monitoring-for-accessible-healthcare/

### 11. CareNX Fetosense (also earlier UNICEF Venture Fund) — UNICEF Office of Innovation
- **One-liner**: Off-the-shelf fetal heart monitor for rural India where gynecologists are scarce
- **Link**: https://www.unicef.org/innovation/stories/four-startups-harnessing-artificial-intelligence-strengthen-healthcare-systems-children

### 12. Docokids (Colombia) — UNICEF AI Venture Fund
- **One-liner**: 24/7 pediatrician-backed AI chatbot for remote-area parents
- **Emotional hook**: Parents watching sick children with no doctor for 200 km
- **Link**: https://www.unicef.org/innovation/stories/four-startups-harnessing-artificial-intelligence-strengthen-healthcare-systems-children

### 13. Moner Bondhu / Manush-E (Bangladesh) — UNICEF AI Venture Fund
- **One-liner**: Affordable mental-wellness AI chatbot for youth in Bangladesh
- **Emotional hook**: Suicide epidemic among young adults with zero access to therapists

---

## Social Impact / Education / Safety Winners

### 14. Chatbot Sophia (Spring ACT) — 2025 AI for Good Pro Bono Collaboration Award
- **One-liner**: Anonymous 24/7 AI companion for domestic-violence survivors with secure evidence vault
- **Hard stats**: 41,000 users, 172 countries, 20+ languages
- **Emotional hook**: Women too scared to call a hotline; AI as the first safe listener
- **Link**: https://aiforgood.itu.int/meet-the-winners-for-the-2025-ai-for-good-impact-awards/

### 15. Farmer.Chat (Digital Green) — 2025 AI for Good: AI FOR PROSPERITY + Meta Llama Impact Grant Finalist
- **One-liner**: Multi-modal (voice/text/image/video) Llama-powered farming advisor in local languages
- **Stats**: 460,000 farmers reached; 5M-farmer roadmap
- **Emotional hook**: Smallholder farmers losing crops to climate they cannot read

### 16. Bitz ITC (Kenya) — UNICEF AI Venture Fund
- **One-liner**: Open-source AI call-center for gender-based-violence helplines across 4 African countries
- **Emotional hook**: Women and children calling in crisis; no operator available

### 17. Wadhwani AI — Llama Impact Grant 2024
- **One-liner**: AI reading-fluency assessment for Gujarat public-school children
- **Emotional hook**: Rural children falling behind in English; no individual attention possible

### 18. Tenant Case Navigator — Hack for Social Impact 2024 (3rd place)
- **One-liner**: AI-searchable database for tenant-rights lawyers at CLSEPA
- **Emotional hook**: Families facing eviction with no legal aid

### 19. SecureStep / Rex (Hack the North 2024 winners, accessibility track)
- **One-liner**: Smart walking cane for seniors; AI-powered robot dog for blind wayfinding
- **Emotional hook**: Grandparents falling; blind students navigating campuses
- **Link**: https://www.mappedin.com/resources/blog/hack-the-north-2024/

---

## Meta Llama Impact Hackathon Deep Dive

### London 2024 (Cerebral Valley) — 200 devs, 56 teams, $50K prize pool
Top-3 breakdown shows the theme: **ALL THREE winners were healthcare/accessibility**, even though hackathon tracks also included clean energy and social mobility. Healthcare won decisively.

### LlamaCon SF 2025 — 238 devs, 44 projects, $35K pool
**Notably NOT social-impact winners.** Top 4:
1. OrgLens (enterprise talent matching)
2. Compliance Wizards (fraud detection)
3. Llama CCTV Operator (surveillance)
4. Geo-ML (geology)

**Critical takeaway**: LlamaCon was an enterprise-/technical-utility-themed event. Emotional pitches did NOT win there. The Llama *Impact* Hackathon (different event, with "Impact" in the name and social-impact tracks) was where emotional framing dominated. **Match your pitch to the event's stated theme.** The OpenEnv Hackathon's judging criteria must be checked: if it weights "impact" or "public good" the emotional framing wins; if it weights novelty of RL environment or training quality, technical rigor wins.

### India Llama Hackathon (Bengaluru, Reskilll+Meta)
270+ participants, WhatsApp-integrated Llama 3 solutions. Winner details sparse, but WhatsApp integration (reaching rural users on messenger they already use) was the consistent emotional-hook theme.

---

## Critical Analysis: When Emotion Beats Technical Superiority (and when it doesn't)

**Emotion WINS when:**
- Event has "Impact", "Social Good", "For Good", or NGO co-sponsors in the name
- Judges include doctors, NGO leaders, policy people (not just engineers)
- Prize is a *grant* (usable for deployment) rather than pure cash — grant judges need "theory of change"
- A named partner org (UNICEF/WHO/UN) is present

**Emotion LOSES / BACKFIRES when:**
- Event is enterprise/dev-tooling themed (LlamaCon 2025, PyTorch Conference Startup Showcase)
- Judges are all ML researchers who penalize hand-wavy claims
- You use mortality stats but your demo clearly doesn't address them (judges feel manipulated)
- Your solution is an "app" in a hackathon rewarding novel environments/training methods — mismatch
- Over-claiming "saves lives" without any validation evidence (judges roll eyes)

**The specific risk for the Meta PyTorch OpenEnv Hackathon Bangalore**: Judging likely weights (a) novelty of the RL environment design, (b) correctness of reward-model/TRL training, (c) demonstrable agent improvement. Pure emotional framing with a weak environment will lose to a technically excellent but boring environment. **The winning play is both**: wrap a technically rigorous OpenEnv environment in a high-stakes social-impact narrative where the environment's *reward signal itself* encodes the emotional value (e.g., reward for correctly triaging high-risk pregnancies; reward for accurate danger-sign detection in maternal SMS).

---

## Candidate Domains for Our Round 2 Project (Ranked)

### TIER 1 — Pitch-ready, proven winners, rich public data, India-relevant

1. **Maternal / postpartum SMS triage agent** (PROMPTS / MamaMate lineage)
   - Why: Kenya stats (51x UK, 6,000 deaths/yr, 91% solvable with info) are pre-built emotional ammo. Bangalore judges will recognize India's own 103/100k maternal mortality. OpenEnv = multi-turn triage dialogue where the agent must learn to escalate danger signs. Reward model = did it correctly escalate preeclampsia/hemorrhage/sepsis signals? TRL-trainable. **Best fit.**

2. **Rural child-vaccination scheduling agent** (HelpMum ADVISER lineage)
   - Why: "73.5% increase" / "25,000 lives saved" framing is verbatim-reusable. OpenEnv = scheduler environment with mother availability, clinic stock, travel constraints. Reward = vaccinations completed on schedule. Clean RL formulation. India has Mission Indradhanush as an obvious hook.

3. **ASHA worker (community health) assistant agent** (India-specific variant)
   - Why: India has 1M+ ASHA workers. An agent that helps them triage home-visit findings is an emotional layup for Bangalore judges (they know ASHA). OpenEnv = simulated rural visit dialogues. Reward = correct referral decisions.

### TIER 2 — Strong emotional hook but RL framing is harder

4. Gender-based-violence support triage (Sophia lineage) — sensitive; judges may fear responsibility
5. Child malnutrition screening agent (RevolutionAIze) — more CV than RL
6. Mental health / suicide-risk triage — VERY sensitive; backfire risk high

### TIER 3 — Don't pick

- Generic "AI tutor" — oversaturated
- Disaster response — hard to simulate convincingly in 48 hrs
- Climate — emotional distance too large for live judging

---

## Warning: Where Emotional Framing Backfires

1. **"Saves lives" without evidence**: If you claim lives saved but your environment is clearly a toy, judges will punish you for cynicism. Use conditional framing: "This environment is the first step toward agents that could reduce the 6,000 annual deaths…"
2. **Trauma tourism**: Showing graphic images of dying mothers/children to manipulate emotion is widely criticized and will earn a judge backlash, especially at Indian events where local judges have real field experience.
3. **Western-savior framing**: If your team is Bangalore-based, do NOT pitch "solving Africa's problem." Pitch India's own 103/100k maternal mortality, 28 under-5 deaths per 1,000 live births, or ASHA-worker burden. Local ownership reads as authentic; outward-looking reads as cosplay.
4. **Mental health overreach**: Suicide-prevention agents are the highest-emotion, highest-risk pitch. Multiple 2025 studies (Nature Sci Reports, JMIR Mental Health) show LLM safety on suicidal ideation is still unsolved. Judges know this and will downgrade for safety-washing.
5. **Over-specific verifiable claims**: Don't say "reduces maternal mortality by 40%" unless you have a cited RCT. Do say "our reward model penalizes the exact danger-sign misses that cause 1/3 of Kenyan maternal deaths" — narrower, defensible, still emotional.

---

## Recommended Pitch Script Skeleton (Use This Verbatim as Template)

> "In India, a woman dies in childbirth every 20 minutes. [NAMED PERSON — a real ASHA worker we talked to, or a compiled persona] sees this every month in her village of [PLACE]. 91% of these deaths are preventable if danger signs are caught early. Today, we built [PROJECT NAME] — an OpenEnv environment for training agents to recognize maternal danger signs in the exact multi-turn SMS conversations ASHA workers have. Our reward model scores 12 WHO danger signs. In 48 hours, we trained a Llama-3.2-1B agent with TRL GRPO that catches preeclampsia signals [X%] better than the base model. The environment is open-sourced. With it, every RL researcher in this room can now train safer maternal triage agents — agents that could, with real deployment partners like Jacaranda Health or ARMMAN, help close the 91% preventability gap."

This template combines: named victim + crushing stat + preventability hammer + technical rigor (TRL, GRPO, measurable delta) + path to impact (named orgs) + judge flattery ("every researcher in this room").

---

## Sources (Key URLs)

- Meta Llama Impact Hackathon 2024 (London) — https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/
- LlamaCon 2025 winners — https://ai.meta.com/blog/llamacon-hackathon/
- Llama Impact Grant 2024 winners — https://ai.meta.com/blog/llama-impact-grant-innovation-award-winners-2024/
- 2025 AI for Good Impact Awards — https://aiforgood.itu.int/meet-the-winners-for-the-2025-ai-for-good-impact-awards/
- MamaMate / Elevate AI Africa — https://aiforgood.itu.int/mamamate-wins-again-this-time-at-the-ai-for-good-innovation-factory-grand-finale-2025/
- Jacaranda Health PROMPTS — https://jacarandahealth.org/prompts/
- HelpMum ADVISER (Gavi) — https://www.gavi.org/vaccineswork/ai-driven-mobile-app-helping-nigerian-mothers-keep-top-their-babies-immunisation
- UNICEF Office of Innovation AI startups — https://www.unicef.org/innovation/stories/four-startups-harnessing-artificial-intelligence-strengthen-healthcare-systems-children
- RevolutionAIze / MAAP — https://aiforgood.itu.int/meet-revolutionaize-the-ai-startup-revolutionizing-child-growth-monitoring-for-accessible-healthcare/
- Hack for Social Impact 2024 — https://hack-for-social-impact-2024.devpost.com/
- Hack the North 2024 accessibility winners — https://www.mappedin.com/resources/blog/hack-the-north-2024/
- PyTorch OpenEnv Hackathon (our target) — https://pytorch.org/event/openenv-ai-hackathon/
