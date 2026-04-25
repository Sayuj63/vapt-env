# generate_plots.py - Quick Start Guide

Compare Random vs LLM agents on AISHA in 5 minutes.

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
pip install requests numpy matplotlib openai
```

### Step 2: Set Environment Variables (1 min)
```bash
export HF_TOKEN="hf_your_token_here"
export OPENAI_API_KEY="sk_your_key_here"
export API_BASE_URL="https://anshumanatrey-security-audit-env.hf.space"
export MODEL_NAME="gpt-4o-mini"
```

### Step 3: Run Script (2-3 min)
```bash
python generate_plots.py
```

### Step 4: View Results (1 min)
```bash
ls -lh plots/
open plots/reward_per_episode.png
open plots/cumulative_reward_curve.png
open plots/vulns_found.png
```

---

## 📊 What You Get

### 3 PNG Plots
1. **reward_per_episode.png** - Episode rewards comparison
2. **cumulative_reward_curve.png** - Cumulative rewards with uncertainty
3. **vulns_found.png** - Vulnerability detection rate

### Summary Table
```
Metric                   Random Agent         LLM Agent
----------------------------------------------------------------------
Avg Episode Reward       0.2341               0.4567
Avg Vulns Found          1.2 / 3              2.1 / 3
Best Episode Score       0.3500               0.6200
Reward Std Dev           0.0890               0.1234
Min Episode Score        0.1200               0.3100
LLM Improvement          95.1%
```

---

## 🔧 Configuration

### Change Number of Episodes
Edit line in script:
```python
config = Config(num_episodes=20)  # Default: 10
```

### Change LLM Model
```bash
export MODEL_NAME="claude-sonnet-4-6"  # or "gpt-4o-mini"
```

### Change Scenario
Edit line in script:
```python
config = Config(scenario_id="medium")  # Options: "easy", "medium", "hard"
```

### Change Output Directory
```bash
export PLOTS_DIR="./my_plots"
```

---

## 🎯 Expected Results

### Random Agent
- Avg Reward: 0.20-0.30
- Vulns Found: 1.0-1.5 / 3

### LLM Agent
- Avg Reward: 0.35-0.50
- Vulns Found: 1.5-2.5 / 3

### Improvement
- LLM is 50-100% better than random

---

## 🐛 Common Issues

### "Connection refused"
→ HF Space might be sleeping. Wait 30 seconds and retry.

### "Invalid API key"
→ Check OPENAI_API_KEY is set correctly.

### "plots/ directory not found"
→ Script creates it automatically. Check file permissions.

### "No plots generated"
→ Check script ran without errors. Look for error messages above.

---

## 📈 Interpreting Results

### Plot 1: Episode Rewards
- **X-axis**: Episode number (1-10)
- **Y-axis**: Total reward for that episode
- **Red dashed**: Random agent (baseline)
- **Blue solid**: LLM agent (your agent)
- **Goal**: Blue line should be above red line

### Plot 2: Cumulative Rewards
- **X-axis**: Step within episode
- **Y-axis**: Cumulative reward so far
- **Shaded bands**: ±1 standard deviation
- **Goal**: Blue line should rise faster than red

### Plot 3: Vulnerabilities Found
- **X-axis**: Episode number (1-10)
- **Y-axis**: Number of vulnerabilities found (0-3)
- **Orange bars**: Random agent
- **Green bars**: LLM agent
- **Goal**: Green bars should be taller

---

## 🚀 Next Steps

1. **Analyze results**: Do the plots show LLM is better?
2. **Try different models**: Change MODEL_NAME
3. **Try harder scenarios**: Change scenario_id to "medium" or "hard"
4. **Customize agents**: Modify agent logic in script
5. **Integrate with training**: Use metrics for hyperparameter tuning

---

## 📚 Full Documentation

See `GENERATE_PLOTS_README.md` for:
- Detailed configuration options
- Code structure explanation
- Metrics definitions
- Troubleshooting guide
- Learning outcomes

---

## 💡 Pro Tips

1. **First run?** Use default settings, just set API keys
2. **Want faster results?** Reduce num_episodes to 5
3. **Want more data?** Increase num_episodes to 20
4. **Want to debug?** Add print statements in agent code
5. **Want to compare models?** Run script twice with different MODEL_NAME

---

**Ready? Run `python generate_plots.py`! 🚀**
