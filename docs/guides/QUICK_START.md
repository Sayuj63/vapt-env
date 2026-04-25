# AISHA RL Training - Quick Start Guide

## 🎯 5-Minute Setup

### Step 1: Open Notebook in Colab
1. Go to [Google Colab](https://colab.research.google.com)
2. Click "File" → "Open notebook"
3. Upload `AISHA_RL_Training_Colab.ipynb`

### Step 2: Add Secrets
1. Click 🔑 icon in left sidebar
2. Add `HF_TOKEN` (get from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
3. Add `OPENAI_API_KEY` (optional)

### Step 3: Run All Cells
```
Ctrl+F9  (or Cmd+F9 on Mac)
```
Or run cells individually from top to bottom.

### Step 4: Download Results
- `reward_curve.png` - Shows training progress
- `loss_curve.png` - Shows loss convergence

---

## 📊 What You'll Get

### Training Output
```
Episode 1/5
  Episode Reward: 0.3421
  Avg Loss: 0.5234
  Steps: 28

Episode 2/5
  Episode Reward: 0.4156
  Avg Loss: 0.4891
  Steps: 29
...
```

### Evaluation Output
```
Baseline Average Score: 0.2341
Trained Average Score: 0.4567
Improvement: 95.1%
```

### Generated Plots
- **reward_curve.png**: Training progress + comparison
- **loss_curve.png**: Loss convergence

---

## 🔧 Customization

### Change Training Episodes
```python
num_episodes = 10  # Default: 5
```

### Change Scenario Difficulty
```python
scenario_id = "medium"  # Options: "easy", "medium", "hard"
```

### Change Model
```python
MODEL_NAME = "Qwen/Qwen1.5-7B-Chat"  # Larger model (requires more VRAM)
```

---

## ⚡ Performance Tips

### For Colab Free Tier
- Use `num_episodes = 5` (default)
- Use `Qwen/Qwen1.5-1.8B-Chat` (default)
- Use `scenario_id = "easy"` (default)

### For Colab Pro
- Use `num_episodes = 10`
- Use `Qwen/Qwen1.5-7B-Chat`
- Use `scenario_id = "medium"`

### For Local GPU (RTX 3090+)
- Use `num_episodes = 20`
- Use `Qwen/Qwen1.5-32B-Chat`
- Use `scenario_id = "hard"`

---

## 🐛 Common Issues

### "Connection refused"
→ HF Space might be sleeping. Wait 30 seconds and retry.

### "CUDA out of memory"
→ Use CPU: Change `device = "cpu"` in Cell 7

### "HF_TOKEN not found"
→ Add it to Colab Secrets (🔑 icon)

### "Model download failed"
→ Check internet. Retry. May be temporary.

---

## 📈 Understanding Results

### Reward Curve
- **X-axis**: Training episode number
- **Y-axis**: Total reward for that episode
- **Red dashed line**: Baseline (random agent) average
- **Blue line**: Trained agent rewards
- **Goal**: Blue line should be above red line

### Loss Curve
- **X-axis**: Training step number
- **Y-axis**: Loss value
- **Red line**: Moving average
- **Goal**: Loss should decrease over time

### Summary Metrics
- **Baseline Avg Score**: Random agent performance
- **Trained Avg Score**: Your trained agent performance
- **Improvement %**: How much better your agent is

---

## 🚀 Next Steps

### After Training
1. Download the PNG plots
2. Review the summary metrics
3. Try different scenarios (medium, hard)
4. Experiment with different models

### Advanced
1. Implement proper GRPO with HF TRL
2. Add curriculum learning
3. Fine-tune hyperparameters
4. Deploy to production

---

## 📚 Files Included

| File | Purpose |
|------|---------|
| `AISHA_RL_Training_Colab.ipynb` | Main Jupyter notebook for Colab |
| `aisha_rl_training.py` | Standalone Python script |
| `COLAB_TRAINING_README.md` | Detailed documentation |
| `QUICK_START.md` | This file |
| `convert_to_notebook.py` | Markdown → Jupyter converter |

---

## 💡 Pro Tips

1. **First run**: Expect 5-10 minutes on Colab free tier
2. **Baseline matters**: Random agent gives you a baseline to beat
3. **Loss convergence**: Watch loss_curve.png to see if training is working
4. **Reproducibility**: Set seed for consistent results
5. **Monitoring**: Check reward_curve.png to spot overfitting

---

## 🎓 Learning Path

1. **Beginner**: Run notebook as-is, observe results
2. **Intermediate**: Modify hyperparameters, try different scenarios
3. **Advanced**: Implement GRPO properly, add custom rewards
4. **Expert**: Deploy to production, scale to multiple agents

---

## 📞 Support

- **Notebook issues**: Check COLAB_TRAINING_README.md
- **Environment issues**: Check HF Space status
- **Model issues**: Check HuggingFace model card
- **OpenEnv issues**: Check OpenEnv documentation

---

**Ready? Open the notebook and run Cell 1! 🚀**
