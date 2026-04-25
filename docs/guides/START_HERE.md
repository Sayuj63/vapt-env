# 🚀 AISHA RL Training Package - START HERE

Welcome! This is your entry point to the complete AISHA RL training package.

---

## ⚡ Quick Decision Tree

### I want to train in Google Colab (Recommended)
→ **Go to**: [QUICK_START.md](QUICK_START.md)  
→ **Then use**: [AISHA_RL_Training_Colab.ipynb](AISHA_RL_Training_Colab.ipynb)  
→ **Time**: ~10 minutes

### I want to train locally on my machine
→ **Go to**: [QUICK_START.md](QUICK_START.md)  
→ **Then use**: [aisha_rl_training.py](aisha_rl_training.py)  
→ **Time**: ~15 minutes

### I want to understand everything first
→ **Go to**: [COLAB_TRAINING_README.md](COLAB_TRAINING_README.md)  
→ **Then read**: [TRAINING_PIPELINE.md](TRAINING_PIPELINE.md)  
→ **Time**: ~1 hour

### I'm a visual learner
→ **Go to**: [TRAINING_PIPELINE.md](TRAINING_PIPELINE.md)  
→ **Then read**: [QUICK_START.md](QUICK_START.md)  
→ **Time**: ~20 minutes

### I need a complete overview
→ **Go to**: [PACKAGE_SUMMARY.txt](PACKAGE_SUMMARY.txt)  
→ **Then read**: [TRAINING_PACKAGE_INDEX.md](TRAINING_PACKAGE_INDEX.md)  
→ **Time**: ~15 minutes

---

## 📋 What's in This Package?

### 🎯 Main Files (Use These)
1. **AISHA_RL_Training_Colab.ipynb** - Jupyter notebook for Google Colab
2. **aisha_rl_training.py** - Standalone Python script for local training

### 📚 Documentation (Read These)
1. **QUICK_START.md** - 5-minute quick start guide
2. **COLAB_TRAINING_README.md** - Comprehensive documentation
3. **TRAINING_PIPELINE.md** - Visual diagrams and explanations
4. **TRAINING_PACKAGE_INDEX.md** - Complete package index
5. **PACKAGE_SUMMARY.txt** - Executive summary

### 🔧 Supporting Files (Reference)
1. **AISHA_TRAINING_NOTEBOOK.md** - Markdown source for notebook
2. **convert_to_notebook.py** - Utility to convert markdown to Jupyter
3. **MANIFEST.md** - Complete package manifest
4. **FILES_GENERATED.txt** - List of all generated files
5. **START_HERE.md** - This file

---

## ✨ What You'll Get

After running the training, you'll have:

1. **reward_curve.png** - Shows your training progress
2. **loss_curve.png** - Shows loss convergence
3. **Console output** - Detailed metrics and summary

Expected improvement: **50-100%** over baseline

---

## 🎯 The 3-Step Process

### Step 1: Setup (2 minutes)
- Get HuggingFace token from https://huggingface.co/settings/tokens
- For Colab: Add token to Colab Secrets (🔑 icon)
- For Local: Set environment variable

### Step 2: Run (10-15 minutes)
- For Colab: Open notebook and run all cells (Ctrl+F9)
- For Local: Run `python aisha_rl_training.py`

### Step 3: Analyze (5 minutes)
- Download PNG plots
- Review metrics
- Celebrate your trained agent! 🎉

---

## 📊 What Happens During Training

```
Training Loop (5 episodes):
├─ Episode 1: Agent learns basic actions
├─ Episode 2: Agent improves strategy
├─ Episode 3: Agent explores more
├─ Episode 4: Agent converges
└─ Episode 5: Agent stabilizes

Evaluation:
├─ Baseline (random agent): 5 episodes
└─ Trained agent: 5 episodes

Comparison:
└─ Shows improvement percentage

Visualization:
├─ reward_curve.png (training progress)
└─ loss_curve.png (loss convergence)
```

---

## 🔑 Key Features

✅ **Live Environment** - Connects to real HF Space  
✅ **Small Model** - Qwen1.5-1.8B (fits in Colab free tier)  
✅ **GRPO Training** - Group Relative Policy Optimization  
✅ **Easy Scenario** - 2 hosts, 3 vulnerabilities  
✅ **Baseline Comparison** - See your improvement  
✅ **Beautiful Plots** - PNG visualizations  
✅ **Comprehensive Docs** - Everything explained  
✅ **No Manual Steps** - Fully automated  

---

## 🚀 Getting Started Now

### For Google Colab Users:
1. Click: [AISHA_RL_Training_Colab.ipynb](AISHA_RL_Training_Colab.ipynb)
2. Upload to Google Colab
3. Add HF_TOKEN to Colab Secrets
4. Run all cells (Ctrl+F9)
5. Download PNG plots

### For Local Python Users:
1. Open terminal
2. Set environment variables:
   ```bash
   export HF_TOKEN="your_token"
   export API_BASE_URL="https://anshumanatrey-security-audit-env.hf.space"
   ```
3. Run: `python aisha_rl_training.py`
4. Check PNG plots in current directory

---

## ❓ Common Questions

**Q: Do I need a GPU?**  
A: No, but it's faster. CPU works fine for this small model.

**Q: How long does it take?**  
A: ~10 minutes in Colab, ~15 minutes locally.

**Q: What if I get an error?**  
A: Check [QUICK_START.md](QUICK_START.md) troubleshooting section.

**Q: Can I use a different model?**  
A: Yes! Change `MODEL_NAME` in the notebook/script.

**Q: Can I train on harder scenarios?**  
A: Yes! Change `scenario_id` to "medium" or "hard".

**Q: How do I understand the code?**  
A: Read [COLAB_TRAINING_README.md](COLAB_TRAINING_README.md) for detailed explanations.

---

## 📚 Documentation Map

```
START_HERE.md (You are here)
    ↓
QUICK_START.md (5 min read)
    ├─ For Colab users → AISHA_RL_Training_Colab.ipynb
    └─ For local users → aisha_rl_training.py

For deeper understanding:
    ├─ COLAB_TRAINING_README.md (comprehensive guide)
    ├─ TRAINING_PIPELINE.md (visual explanations)
    ├─ TRAINING_PACKAGE_INDEX.md (package overview)
    └─ PACKAGE_SUMMARY.txt (executive summary)

For reference:
    ├─ MANIFEST.md (package manifest)
    ├─ FILES_GENERATED.txt (file listing)
    └─ AISHA_TRAINING_NOTEBOOK.md (notebook source)
```

---

## 🎓 Learning Path

### Beginner (Just want to run it)
1. Read: QUICK_START.md (5 min)
2. Run: Notebook or script (10 min)
3. Done! ✅

### Intermediate (Want to understand it)
1. Read: QUICK_START.md (5 min)
2. Read: COLAB_TRAINING_README.md (20 min)
3. Run: Notebook or script (10 min)
4. Experiment: Try different scenarios (10 min)
5. Done! ✅

### Advanced (Want to customize it)
1. Read: COLAB_TRAINING_README.md (20 min)
2. Read: TRAINING_PIPELINE.md (15 min)
3. Study: Notebook cells (30 min)
4. Modify: Hyperparameters and model (20 min)
5. Run: Custom training (10 min)
6. Done! ✅

---

## 🎯 Expected Results

### Baseline (Random Agent)
- Average Score: ~0.20-0.30
- Behavior: Random actions

### Trained Agent (After 5 Episodes)
- Average Score: ~0.35-0.50
- Improvement: 50-100%

### Loss Convergence
- Initial: ~0.80-0.90
- Final: ~0.30-0.50
- Trend: Decreasing ✓

---

## 🔧 System Requirements

### For Google Colab
- ✅ Google account
- ✅ HuggingFace token (free)
- ✅ Internet connection
- ✅ ~10 minutes

### For Local Machine
- ✅ Python 3.8+
- ✅ pip or conda
- ✅ HuggingFace token (free)
- ✅ GPU recommended (CPU works)
- ✅ ~15 minutes

---

## 💡 Pro Tips

1. **First time?** Start with QUICK_START.md
2. **Visual learner?** Check TRAINING_PIPELINE.md
3. **Want details?** Read COLAB_TRAINING_README.md
4. **Need help?** See troubleshooting sections
5. **Ready to code?** Open the notebook/script

---

## 🆘 Troubleshooting

### Connection Error
→ Check HF Space status, wait 30 seconds, retry

### Out of Memory
→ Use CPU instead of GPU

### Token Not Found
→ Add HF_TOKEN to Colab Secrets (🔑 icon)

### Model Download Fails
→ Check internet, verify token, retry

For more help: See [QUICK_START.md](QUICK_START.md)

---

## 📞 Need Help?

1. **Quick questions?** → Check [QUICK_START.md](QUICK_START.md)
2. **Want details?** → Read [COLAB_TRAINING_README.md](COLAB_TRAINING_README.md)
3. **Visual explanation?** → See [TRAINING_PIPELINE.md](TRAINING_PIPELINE.md)
4. **Package overview?** → Check [PACKAGE_SUMMARY.txt](PACKAGE_SUMMARY.txt)

---

## ✅ Checklist Before Starting

- [ ] I have a HuggingFace token
- [ ] I chose Colab or Local
- [ ] I read QUICK_START.md
- [ ] I have internet connection
- [ ] I have ~10-15 minutes

---

## 🎉 Ready?

### Choose Your Path:

**🌐 Google Colab (Recommended)**
1. Open [AISHA_RL_Training_Colab.ipynb](AISHA_RL_Training_Colab.ipynb)
2. Upload to Colab
3. Add HF_TOKEN to Secrets
4. Run all cells
5. Download plots

**💻 Local Python**
1. Set HF_TOKEN environment variable
2. Run: `python aisha_rl_training.py`
3. Check PNG plots

**📖 Learn First**
1. Read [QUICK_START.md](QUICK_START.md)
2. Read [COLAB_TRAINING_README.md](COLAB_TRAINING_README.md)
3. Then run the notebook/script

---

## 🚀 Let's Go!

**Next Step**: Open [QUICK_START.md](QUICK_START.md)

**Time to Results**: ~10-15 minutes

**Expected Outcome**: Trained RL agent + 2 PNG plots

---

**Happy training! 🎉**

*Questions? Check the documentation files above.*  
*Ready? Start with QUICK_START.md!*
