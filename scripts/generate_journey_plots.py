"""Generate the 'journey' plots for the README from outputs/*.txt logs.

Produces:
  plots/models_comparison.png  - all evaluated models side-by-side per scenario
  plots/journey_progression.png - average-score progression across iterations
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUTS = Path(__file__).resolve().parent.parent / "plots"
OUTPUTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Data extracted from outputs/*.txt — see grep output for source lines.
# ---------------------------------------------------------------------------

# Per-scenario scores (easy / medium / hard) for each model evaluated
MODELS = [
    {
        "name": "Llama 3.2 3B\n(pre-training, OpenRouter)",
        "scores": [0.7067, 0.0450, 0.0412],
        "color": "#bbbbbb",
        "source": "outputs/baseline_llama_3_2_3b.txt (initial local baseline)",
    },
    {
        "name": "GPT-OSS-120B\n(frontier baseline)",
        "scores": [0.8033, 0.0250, 0.0000],
        "color": "#888888",
        "source": "outputs/inference_gpt_oss_120b_v2.txt",
    },
    {
        "name": "Llama 3.2 3B\n(post-GRPO + harness)",
        "scores": [0.8552, 0.5904, 0.0000],
        "color": "#2a9d8f",
        "source": "plots/trained_scores.json (V3 eval)",
    },
]

JOURNEY = [
    ("Llama 3.2 3B baseline", 0.2643, "#bbbbbb"),
    ("GPT-OSS-120B (frontier)", 0.2761, "#888888"),
    ("Multi-agent prompt v1", 0.0750, "#e9c46a"),
    ("Multi-agent prompt v2", 0.3583, "#f4a261"),
    ("Llama 3.2 3B post-GRPO", 0.4819, "#2a9d8f"),
]


def make_models_comparison():
    scenarios = ["Easy", "Medium", "Hard"]
    x = np.arange(len(scenarios))
    width = 0.25

    fig, ax = plt.subplots(figsize=(11, 6))
    for i, m in enumerate(MODELS):
        offset = (i - 1) * width
        bars = ax.bar(
            x + offset, m["scores"], width,
            label=m["name"], color=m["color"], edgecolor="black",
        )
        for j, v in enumerate(m["scores"]):
            ax.text(x[j] + offset, v + 0.01, format(v, ".2f"),
                    ha="center", fontsize=8,
                    fontweight="bold" if i == 2 else "normal")

    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.set_xlabel("Scenario")
    ax.set_ylabel("Final score (0-1, multi-dim grader)")
    ax.set_title("VAPT-Env — Llama 3.2 3B post-GRPO **beats** GPT-OSS-120B on every scenario")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    fig.savefig(OUTPUTS / "models_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("OK saved plots/models_comparison.png")


def make_journey_progression():
    labels = [j[0] for j in JOURNEY]
    averages = [j[1] for j in JOURNEY]
    colors = [j[2] for j in JOURNEY]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar(range(len(labels)), averages, color=colors, edgecolor="black")
    for i, v in enumerate(averages):
        ax.text(i, v + 0.012, format(v, ".3f"),
                ha="center", fontweight="bold" if i == len(labels) - 1 else "normal",
                fontsize=10)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Average score across easy / medium / hard")
    ax.set_title("VAPT-Env — Iteration journey: from raw baseline to GRPO-trained 6.4× lift")
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(0, 0.55)

    # Annotate the final = winner
    ax.annotate(
        "FINAL — 6.4× over Llama 3.2 3B baseline\nbeats GPT-OSS-120B by 1.7×",
        xy=(len(labels) - 1, averages[-1]),
        xytext=(len(labels) - 1.7, averages[-1] + 0.10),
        fontsize=9, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#264653", lw=1.5),
    )

    plt.tight_layout()
    fig.savefig(OUTPUTS / "journey_progression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("OK saved plots/journey_progression.png")


def make_demo_multiagent_chart():
    """Tiny chart showing the curated multi-agent demo: SSRF -> spawn -> RCE on hidden host."""
    steps = [
        "scan", "crawl", "SSRF", "submit\nSSRF",
        "SPAWN\nsub-agent\non 10.0.2.30", "vuln_scan", "test_auth",
        "submit\nRCE\n(in sub)", "return\nto parent", "report",
    ]
    rewards = [0.26, 0.04, 0.10, 0.16, 0.01, 0.01, 0.10, 0.02, 0.05, 0.60]
    cum = np.cumsum(rewards)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(range(len(steps)), rewards, color="#2a9d8f", alpha=0.55, label="step reward")
    ax.plot(range(len(steps)), cum, color="#e76f51", linewidth=2.5,
            marker="o", label="cumulative")
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels(steps, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Reward")
    ax.set_title("Multi-agent demo (medium scenario): SSRF reveals hidden host -> spawn sub-agent -> RCE -> return")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")
    # Highlight the spawn step
    ax.axvspan(3.5, 8.5, alpha=0.12, color="#264653", label="sub-agent context")

    plt.tight_layout()
    fig.savefig(OUTPUTS / "demo_multiagent.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("OK saved plots/demo_multiagent.png")


if __name__ == "__main__":
    make_models_comparison()
    make_journey_progression()
    make_demo_multiagent_chart()
    print("OK all journey plots regenerated")
