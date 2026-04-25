# generate_plots.py - AISHA Agent Comparison Script

Standalone Python script that compares two agents on the SecurityAuditEnv:
1. **Random Agent** - picks random valid actions each step
2. **Greedy LLM Agent** - uses Claude Sonnet 4.6 or GPT-4o-mini via OpenAI client

Generates 3 publication-quality matplotlib plots and a summary table.

---

## 📋 Features

✅ **Two Agent Types**
- Random Agent: Baseline for comparison
- LLM Agent: Uses OpenAI API (Claude Sonnet 4.6 or GPT-4o-mini)

✅ **10 Episodes Per Agent**
- Collects total reward per episode
- Tracks cumulative reward over steps
- Counts vulnerabilities found

✅ **3 Publication-Quality Plots**
- `reward_per_episode.png` - Episode rewards comparison
- `cumulative_reward_curve.png` - Cumulative rewards with std dev bands
- `vulns_found.png` - Vulnerability detection rate

✅ **Summary Table**
- Average episode reward
- Average vulnerabilities found
- Best episode score
- Improvement percentage

✅ **Clean Output**
- 150 DPI PNG files
- Tight layout, labeled axes with units
- Saved to `./plots/` folder
- Professional styling

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests numpy matplotlib openai
```

### 2. Set Environment Variables

```bash
# Required
export HF_TOKEN="your_huggingface_token"
export OPENAI_API_KEY="your_openai_api_key"

# Optional (defaults provided)
export API_BASE_URL="https://anshumanatrey-security-audit-env.hf.space"
export MODEL_NAME="gpt-4o-mini"  # or "claude-sonnet-4-6"
```

### 3. Run the Script

```bash
python generate_plots.py
```

### 4. Check Results

```bash
ls -lh plots/
# reward_per_episode.png
# cumulative_reward_curve.png
# vulns_found.png
```

---

## 📊 Output Files

### Plot 1: reward_per_episode.png
**Episode Reward Comparison**

- **X-axis**: Episode (1-10)
- **Y-axis**: Total Reward (0.0 - 1.0)
- **Red dashed line**: Random Agent
- **Blue solid line**: LLM Agent
- **Title**: "AISHA: Episode Reward — Random vs LLM Agent"

Shows how each agent performs across 10 episodes.

### Plot 2: cumulative_reward_curve.png
**Cumulative Reward Over Steps**

- **X-axis**: Step (within episode)
- **Y-axis**: Cumulative Reward
- **Red dashed line**: Random Agent (averaged across 10 episodes)
- **Blue solid line**: LLM Agent (averaged across 10 episodes)
- **Shaded bands**: ±1 standard deviation
- **Title**: "AISHA: Cumulative Reward Over Steps"

Shows how reward accumulates during an episode, with uncertainty bands.

### Plot 3: vulns_found.png
**Vulnerability Detection Rate**

- **X-axis**: Episode (1-10)
- **Y-axis**: Vulnerabilities Found / Total (3)
- **Orange bars**: Random Agent
- **Green bars**: LLM Agent
- **Title**: "AISHA: Vulnerability Detection Rate"

Shows how many vulnerabilities each agent finds per episode.

---

## 📋 Summary Table

```
======================================================================
AISHA AGENT COMPARISON SUMMARY
======================================================================

Metric                   Random Agent         LLM Agent
----------------------------------------------------------------------
Avg Episode Reward       0.2341               0.4567
Avg Vulns Found          1.2 / 3              2.1 / 3
Best Episode Score       0.3500               0.6200
Reward Std Dev           0.0890               0.1234
Min Episode Score        0.1200               0.3100
LLM Improvement          95.1%
======================================================================
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | (required) | HuggingFace token |
| `OPENAI_API_KEY` | (required) | OpenAI API key |
| `API_BASE_URL` | `https://anshumanatrey-security-audit-env.hf.space` | Environment URL |
| `MODEL_NAME` | `gpt-4o-mini` | LLM model to use |

### Script Parameters

Edit these in the `Config` class:

```python
config = Config(
    num_episodes=10,              # Episodes per agent
    max_steps_per_episode=30,     # Max steps per episode
    scenario_id="easy",           # Scenario difficulty
    plots_dir="./plots",          # Output directory
    dpi=150                       # Plot resolution
)
```

---

## 📊 Metrics Collected

### Per Episode
- **Total Reward**: Sum of all step rewards
- **Cumulative Rewards**: List of cumulative rewards at each step
- **Vulnerabilities Found**: Number of vulnerabilities submitted
- **Steps Taken**: Number of steps before episode ended
- **Actions Taken**: List of action types executed

### Aggregated
- **Average Episode Reward**: Mean of all episode rewards
- **Average Vulnerabilities Found**: Mean vulnerabilities per episode
- **Best Episode Reward**: Maximum episode reward
- **Reward Std Dev**: Standard deviation of episode rewards
- **Min Episode Score**: Minimum episode reward

---

## 🎯 Agent Behavior

### Random Agent
```python
# Picks random action each step
- 33% chance: list_tools
- 33% chance: use_tool (random tool, random host)
- 33% chance: submit_finding (random severity, CWE, OWASP)
```

### LLM Agent
```python
# Uses Claude Sonnet 4.6 or GPT-4o-mini
# Analyzes current observation:
#   - Current phase (reconnaissance, enumeration, exploitation)
#   - Discovered hosts and services
#   - Findings submitted so far
#   - Steps remaining
# 
# Chooses action to maximize:
#   - Vulnerabilities found
#   - Efficiency (minimize wasted steps)
```

---

## 🔄 Workflow

```
1. Initialize Environment
   └─ Connect to HF Space

2. Run Random Agent (10 episodes)
   ├─ Episode 1: Reset → Step → Step → ... → Done
   ├─ Episode 2: Reset → Step → Step → ... → Done
   └─ ...
   └─ Episode 10: Reset → Step → Step → ... → Done

3. Run LLM Agent (10 episodes)
   ├─ Episode 1: Reset → Step → Step → ... → Done
   ├─ Episode 2: Reset → Step → Step → ... → Done
   └─ ...
   └─ Episode 10: Reset → Step → Step → ... → Done

4. Generate Plots
   ├─ reward_per_episode.png
   ├─ cumulative_reward_curve.png
   └─ vulns_found.png

5. Print Summary Table
   └─ Metrics comparison
```

---

## 📈 Expected Results

### Random Agent
- **Avg Episode Reward**: ~0.20-0.30
- **Avg Vulns Found**: ~1.0-1.5 / 3
- **Behavior**: Random exploration

### LLM Agent
- **Avg Episode Reward**: ~0.35-0.50
- **Avg Vulns Found**: ~1.5-2.5 / 3
- **Behavior**: Strategic exploration

### Improvement
- **LLM vs Random**: 50-100% better average reward
- **Vulnerability Detection**: 30-50% better detection rate

---

## 🐛 Troubleshooting

### Connection Error
```
Error: Connection refused to https://anshumanatrey-security-audit-env.hf.space
```
**Solution**: 
- Check HF Space is running
- Wait 30 seconds and retry
- Verify API_BASE_URL is correct

### OpenAI API Error
```
Error: Invalid API key provided
```
**Solution**:
- Verify OPENAI_API_KEY is set correctly
- Check API key has sufficient credits
- Ensure API key is for the correct organization

### Out of Memory
```
Error: CUDA out of memory
```
**Solution**:
- This script doesn't use GPU, so shouldn't occur
- If it does, reduce num_episodes or max_steps_per_episode

### No Plots Generated
```
Error: plots/ directory not found
```
**Solution**:
- Script creates plots/ automatically
- Check file permissions
- Verify disk space available

---

## 📚 Code Structure

### Section 1: Configuration & Setup
- `Config` class with environment variable loading
- Plots directory creation

### Section 2: Data Models
- `SecurityAuditAction` - Action representation
- `SecurityAuditObservation` - Observation representation
- `EpisodeMetrics` - Per-episode metrics
- `AgentMetrics` - Aggregated agent metrics

### Section 3: Environment Client
- `SecurityAuditEnv` - HTTP client for environment
- `reset()` - Reset environment
- `step()` - Execute action

### Section 4: LLM Agent
- `LLMAgent` - Uses OpenAI API
- `encode_observation()` - Convert observation to text
- `generate_action()` - Generate action from LLM

### Section 5: Random Agent
- `RandomAgent` - Picks random actions
- `generate_action()` - Generate random action

### Section 6: Episode Runner
- `run_episode()` - Run single episode with agent

### Section 7: Plotting
- `plot_episode_rewards()` - Plot 1
- `plot_cumulative_rewards()` - Plot 2
- `plot_vulnerabilities_found()` - Plot 3

### Section 8: Summary Table
- `print_summary_table()` - Print metrics

### Section 9: Main
- `main()` - Orchestrate everything

---

## 🎓 Learning Outcomes

After running this script, you'll understand:

1. **Agent Comparison** - How to benchmark agents
2. **Metrics Collection** - What to track during training
3. **Visualization** - How to create publication-quality plots
4. **LLM Integration** - How to use OpenAI API for decision-making
5. **Environment Interaction** - How to interact with OpenEnv

---

## 📝 Example Output

```
======================================================================
AISHA AGENT COMPARISON
======================================================================

Configuration:
  Environment: https://anshumanatrey-security-audit-env.hf.space
  Scenario: easy
  Episodes: 10
  Max steps per episode: 30
  LLM Model: gpt-4o-mini
  Output directory: ./plots

Initializing environment...
✓ Environment connected

Initializing agents...
✓ Agents initialized

======================================================================
RANDOM AGENT - Running 10 episodes
======================================================================
  Random Episode 1/10 → Reward: 0.2341, Vulns: 1
  Random Episode 2/10 → Reward: 0.2156, Vulns: 1
  Random Episode 3/10 → Reward: 0.2789, Vulns: 2
  ...

======================================================================
LLM AGENT - Running 10 episodes
======================================================================
  LLM Episode 1/10 → Reward: 0.4567, Vulns: 2
  LLM Episode 2/10 → Reward: 0.3891, Vulns: 2
  LLM Episode 3/10 → Reward: 0.5234, Vulns: 3
  ...

======================================================================
GENERATING PLOTS
======================================================================
✓ Saved ./plots/reward_per_episode.png
✓ Saved ./plots/cumulative_reward_curve.png
✓ Saved ./plots/vulns_found.png

======================================================================
AISHA AGENT COMPARISON SUMMARY
======================================================================

Metric                   Random Agent         LLM Agent
----------------------------------------------------------------------
Avg Episode Reward       0.2341               0.4567
Avg Vulns Found          1.2 / 3              2.1 / 3
Best Episode Score       0.3500               0.6200
Reward Std Dev           0.0890               0.1234
Min Episode Score        0.1200               0.3100
LLM Improvement          95.1%
======================================================================

✓ All plots saved to ./plots/
✓ Comparison complete!
```

---

## 🔗 Related Files

- `AISHA_RL_Training_Colab.ipynb` - Training notebook
- `aisha_rl_training.py` - Training script
- `COLAB_TRAINING_README.md` - Training documentation

---

## 📄 License

This script is provided for educational and research purposes.

---

## 🚀 Next Steps

1. **Run the script**: `python generate_plots.py`
2. **Analyze plots**: Open PNG files in image viewer
3. **Customize agents**: Modify agent logic
4. **Try different scenarios**: Change `scenario_id` to "medium" or "hard"
5. **Integrate with training**: Use metrics for hyperparameter tuning

---

**Ready to compare agents? Run `python generate_plots.py`! 🚀**
