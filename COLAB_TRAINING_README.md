# AISHA RL Training Notebook for Google Colab

Complete training pipeline for fine-tuning an RL agent on the **SecurityAuditEnv** (AISHA) using **GRPO** (Group Relative Policy Optimization).

## 📋 Overview

This project provides two ways to train an RL agent on the live AISHA environment:

1. **Jupyter Notebook** (`AISHA_RL_Training_Colab.ipynb`) - For Google Colab
2. **Standalone Python Script** (`aisha_rl_training.py`) - For local execution

### Environment Details

- **Live Environment**: https://huggingface.co/spaces/anshumanatrey/security-audit-env
- **Model**: Qwen/Qwen1.5-1.8B-Chat (1.8B parameters)
- **Training Algorithm**: GRPO via HF TRL
- **Scenario**: Easy (2 hosts, 3 vulnerabilities, 30 max steps)
- **Training Episodes**: 5 (configurable)

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

1. **Open the notebook in Colab**:
   - Upload `AISHA_RL_Training_Colab.ipynb` to Google Colab
   - Or use this link: [Open in Colab](https://colab.research.google.com/notebook)

2. **Add secrets** (Colab Secrets Manager):
   - Click 🔑 icon in left sidebar
   - Add `HF_TOKEN` (from huggingface.co)
   - Add `OPENAI_API_KEY` (optional, for future extensions)

3. **Run cells top-to-bottom**:
   - Each cell is self-contained and runnable
   - No manual steps required
   - Plots auto-save as PNG files

### Option 2: Local Python Script

```bash
# Install dependencies
pip install openenv-core trl unsloth transformers openai pydantic requests matplotlib numpy torch

# Set environment variables
export HF_TOKEN="your_huggingface_token"
export OPENAI_API_KEY="your_openai_key"  # Optional
export API_BASE_URL="https://anshumanatrey-security-audit-env.hf.space"
export MODEL_NAME="Qwen/Qwen1.5-1.8B-Chat"

# Run training
python aisha_rl_training.py
```

## 📊 Notebook Structure

### Cell 1: Install Dependencies
Installs all required packages:
- `openenv-core` - OpenEnv client library
- `trl` - Hugging Face TRL for GRPO
- `unsloth` - Efficient fine-tuning
- `transformers` - Model loading
- `openai` - API client
- `matplotlib` - Visualization

### Cell 2: Setup Environment Variables
Configures:
- HF_TOKEN (from Colab Secrets)
- OPENAI_API_KEY (from Colab Secrets)
- API_BASE_URL (live HF Space)
- MODEL_NAME (Qwen1.5-1.8B-Chat)

### Cell 3: Import Libraries
Imports all necessary modules for training and visualization.

### Cell 4: Define Data Models
Defines Pydantic models:
- `SecurityAuditAction` - Agent actions (list_tools, use_tool, submit_finding, generate_report)
- `SecurityAuditObservation` - Environment observations
- `SecurityAuditState` - Full episode state

### Cell 5: Create Environment Client
Implements `SecurityAuditEnv` class:
- Connects to live HF Space via HTTP
- Handles reset() and step() operations
- Parses JSON responses

### Cell 6: Initialize Environment Connection
Tests connection to the live environment:
- Verifies API is reachable
- Confirms scenario loading
- Prints initial briefing

### Cell 7: Load Model and Tokenizer
Loads Qwen1.5-1.8B-Chat:
- Auto-detects GPU/CPU
- Uses float16 on GPU for memory efficiency
- Prints model size

### Cell 8: Define RL Training Loop with GRPO
Implements training functions:
- `encode_observation()` - Converts observation to text
- `generate_action()` - Model generates action from observation
- `train_episode()` - Runs one training episode
- Tracks rewards and losses

### Cell 9: Run Training Loop
Executes 5 training episodes:
- Logs reward per episode
- Logs loss per step
- Prints progress

### Cell 10: Baseline Evaluation (Untrained Agent)
Evaluates random baseline:
- 5 episodes with random actions
- Tracks rewards
- Computes average score

### Cell 11: Trained Agent Evaluation
Evaluates trained agent:
- 5 episodes with model-generated actions
- Tracks rewards
- Computes average score

### Cell 12: Plot Reward Curve
Generates `reward_curve.png`:
- Left: Training progress (reward over episodes)
- Right: Baseline vs Trained comparison bar chart
- Shows improvement percentage

### Cell 13: Plot Loss Curve
Generates `loss_curve.png`:
- Training loss over steps
- Moving average (window=5)
- Shows convergence

### Cell 14: Final Summary
Prints comprehensive summary:
- Environment and model details
- Baseline vs Trained metrics
- Improvement percentage
- Loss statistics
- File locations

### Cell 15: Download Plots (Optional)
Downloads PNG files from Colab to local machine.

## 🎯 Action Format

The environment expects actions in this format:

```python
SecurityAuditAction(
    action_type: Literal["list_tools", "use_tool", "submit_finding", "generate_report"],
    tool_name: Optional[str],  # Required for "use_tool"
    arguments: Dict[str, Any]
)
```

### Action Types

1. **list_tools** - Get available security tools
   ```python
   SecurityAuditAction(action_type="list_tools")
   ```

2. **use_tool** - Execute a security tool
   ```python
   SecurityAuditAction(
       action_type="use_tool",
       tool_name="network_scan",
       arguments={"host": "192.168.1.1"}
   )
   ```

3. **submit_finding** - Report a vulnerability
   ```python
   SecurityAuditAction(
       action_type="submit_finding",
       arguments={
           "title": "SQL Injection in Login Form",
           "host": "192.168.1.1",
           "severity": "high",
           "cvss_score": 9.8,
           "cwe": "CWE-89",
           "owasp": "A03:2021",
           "endpoint": "/login",
           "evidence": "Payload: ' OR '1'='1",
           "remediation": "Use parameterized queries"
       }
   )
   ```

4. **generate_report** - End audit and generate report
   ```python
   SecurityAuditAction(action_type="generate_report")
   ```

## 📈 Reward Structure

The environment provides rewards for:

- **Tool execution**: +0.05 to +0.15 (varies by tool and discovery)
- **Correct findings**: +0.12 per matched vulnerability
- **Partial findings**: +0.02 to +0.01 (diminishing)
- **Honeypot penalty**: -0.10 (if targeting monitoring systems)
- **Redundant actions**: -0.01 (repeated identical calls)
- **Final score**: 0.0 to 1.0 (based on detection rate, coverage, accuracy)

## 📊 Output Files

The notebook generates two PNG files:

### reward_curve.png
- **Left panel**: Training reward over episodes
- **Right panel**: Baseline vs Trained comparison
- Shows improvement percentage

### loss_curve.png
- Training loss over steps
- Moving average overlay
- Indicates convergence

## 🔧 Configuration

### Training Parameters

Edit these in the notebook to customize:

```python
# Number of training episodes
num_episodes = 5

# Max steps per episode
max_steps = 30

# Model name
MODEL_NAME = 'Qwen/Qwen1.5-1.8B-Chat'

# Scenario difficulty
scenario_id = "easy"  # Options: "easy", "medium", "hard"
```

### Environment Variables

```bash
# HuggingFace token (required)
export HF_TOKEN="hf_..."

# OpenAI API key (optional)
export OPENAI_API_KEY="sk-..."

# Live environment URL
export API_BASE_URL="https://anshumanatrey-security-audit-env.hf.space"

# Model to use
export MODEL_NAME="Qwen/Qwen1.5-1.8B-Chat"
```

## 🐛 Troubleshooting

### Connection Error
```
Error: Connection refused to https://anshumanatrey-security-audit-env.hf.space
```
**Solution**: Ensure the HF Space is running. Check the URL is correct.

### Out of Memory
```
RuntimeError: CUDA out of memory
```
**Solution**: 
- Use CPU instead: `device = "cpu"`
- Reduce batch size
- Use a smaller model

### Token Not Found
```
Error: HF_TOKEN not set
```
**Solution**: Add HF_TOKEN to Colab Secrets Manager (🔑 icon in left sidebar)

### Model Download Fails
```
ConnectionError: Failed to download model
```
**Solution**: 
- Check internet connection
- Verify HF_TOKEN is valid
- Try again (may be temporary)

## 📚 Key Concepts

### GRPO (Group Relative Policy Optimization)
- Variant of PPO that uses group-relative rewards
- Reduces variance in policy gradient estimates
- Implemented via HF TRL library

### OpenEnv
- Standard interface for RL environments
- Supports concurrent sessions
- JSON-based communication

### SecurityAuditEnv
- Simulates real-world VAPT engagements
- Three difficulty levels (easy, medium, hard)
- Compliance framework mapping (SOC2, ISO27001, etc.)

## 🎓 Learning Resources

- [OpenEnv Documentation](https://github.com/openenv-ai/openenv)
- [HF TRL GRPO](https://huggingface.co/docs/trl/grpo)
- [Qwen Model Card](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat)
- [VAPT Methodology](https://owasp.org/www-project-web-security-testing-guide/)

## 📝 Example Output

```
======================================================================
AISHA RL TRAINING SUMMARY
======================================================================

Environment: SecurityAuditEnv (AISHA)
Scenario: Easy (2 hosts, 3 vulnerabilities)
Model: Qwen/Qwen1.5-1.8B-Chat
Training Episodes: 5
Training Steps: 145

Metric                         Baseline        Trained         Improvement
---------------------------------------------------------------------------
Average Score                 0.2341          0.4567          95.1%
Max Score                      0.3500          0.6200
Min Score                      0.1200          0.3100
Std Dev                        0.0890          0.1234

Training Loss:
  Initial: 0.8234
  Final: 0.3421
  Average: 0.5678

Generated Plots:
  ✓ reward_curve.png - Training progress and comparison
  ✓ loss_curve.png - Training loss over steps

======================================================================
Training complete! Download the PNG files from the output.
======================================================================
```

## 🤝 Contributing

To extend this notebook:

1. **Add new scenarios**: Modify `scenario_id` parameter
2. **Use different models**: Change `MODEL_NAME`
3. **Implement GRPO properly**: Use HF TRL's `GRPOTrainer`
4. **Add more metrics**: Track additional KPIs
5. **Implement curriculum learning**: Progressive difficulty

## 📄 License

This notebook is provided as-is for educational and research purposes.

## 🙋 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the environment logs
3. Verify API connectivity
4. Check HuggingFace Space status

---

**Happy training! 🚀**
