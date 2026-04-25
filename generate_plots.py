#!/usr/bin/env python3
"""
AISHA Agent Comparison Script
==============================

Compares two agents on the SecurityAuditEnv:
1. Random Agent - picks random valid actions
2. Greedy LLM Agent - uses Claude Sonnet 4.6 or GPT-4o-mini via OpenAI client

Generates 3 publication-quality plots and a summary table.
"""

import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import requests
from pathlib import Path

# ============================================================================
# SECTION 1: CONFIGURATION & SETUP
# ============================================================================

@dataclass
class Config:
    """Configuration for the comparison."""
    api_base_url: str = "https://anshumanatrey-security-audit-env.hf.space"
    hf_token: str = ""
    model_name: str = "claude-sonnet-4-6"  # or "gpt-4o-mini"
    num_episodes: int = 10
    max_steps_per_episode: int = 30
    scenario_id: str = "easy"
    plots_dir: str = "./plots"
    dpi: int = 150
    
    def __post_init__(self):
        """Load from environment variables."""
        self.hf_token = os.environ.get("HF_TOKEN", self.hf_token)
        self.api_base_url = os.environ.get("API_BASE_URL", self.api_base_url)
        self.model_name = os.environ.get("MODEL_NAME", self.model_name)
        
        # Create plots directory
        Path(self.plots_dir).mkdir(parents=True, exist_ok=True)

# ============================================================================
# SECTION 2: DATA MODELS
# ============================================================================

class SecurityAuditAction:
    """Action for the Security Audit environment."""
    
    def __init__(self, action_type: str, tool_name: Optional[str] = None, 
                 arguments: Optional[Dict[str, Any]] = None):
        self.action_type = action_type
        self.tool_name = tool_name
        self.arguments = arguments or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API."""
        return {
            "action_type": self.action_type,
            "tool_name": self.tool_name,
            "arguments": self.arguments
        }

class SecurityAuditObservation:
    """Observation from the environment."""
    
    def __init__(self, data: Dict[str, Any]):
        self.tool_output = data.get("tool_output", "")
        self.available_tools = data.get("available_tools", [])
        self.discovered_hosts = data.get("discovered_hosts", [])
        self.discovered_services = data.get("discovered_services", {})
        self.findings_submitted = data.get("findings_submitted", 0)
        self.steps_remaining = data.get("steps_remaining", 0)
        self.message = data.get("message", "")
        self.done = data.get("done", False)
        self.reward = data.get("reward", 0.0)
        self.current_phase = data.get("current_phase", "reconnaissance")
        self.metadata = data.get("metadata", {})

@dataclass
class EpisodeMetrics:
    """Metrics for a single episode."""
    episode_num: int
    total_reward: float = 0.0
    cumulative_rewards: List[float] = field(default_factory=list)
    vulnerabilities_found: int = 0
    steps_taken: int = 0
    actions_taken: List[str] = field(default_factory=list)

@dataclass
class AgentMetrics:
    """Aggregated metrics for an agent."""
    agent_name: str
    episodes: List[EpisodeMetrics] = field(default_factory=list)
    
    @property
    def avg_episode_reward(self) -> float:
        """Average reward per episode."""
        if not self.episodes:
            return 0.0
        return np.mean([e.total_reward for e in self.episodes])
    
    @property
    def avg_vulns_found(self) -> float:
        """Average vulnerabilities found per episode."""
        if not self.episodes:
            return 0.0
        return np.mean([e.vulnerabilities_found for e in self.episodes])
    
    @property
    def best_episode_reward(self) -> float:
        """Best episode reward."""
        if not self.episodes:
            return 0.0
        return max(e.total_reward for e in self.episodes)
    
    @property
    def episode_rewards(self) -> List[float]:
        """List of all episode rewards."""
        return [e.total_reward for e in self.episodes]
    
    @property
    def cumulative_reward_curves(self) -> List[List[float]]:
        """Cumulative reward curves for all episodes."""
        return [e.cumulative_rewards for e in self.episodes]

# ============================================================================
# SECTION 3: ENVIRONMENT CLIENT
# ============================================================================

class SecurityAuditEnv:
    """Client for the Security Audit Environment."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.episode_id = None
    
    def reset(self, scenario_id: str = "easy") -> SecurityAuditObservation:
        """Reset the environment."""
        url = f"{self.base_url}/reset"
        payload = {"scenario_id": scenario_id}
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            self.episode_id = data.get("episode_id")
            obs_data = data.get("observation", {})
            return SecurityAuditObservation(obs_data)
        except Exception as e:
            print(f"Error resetting environment: {e}")
            raise
    
    def step(self, action: SecurityAuditAction) -> Tuple[SecurityAuditObservation, float, bool]:
        """Execute one step."""
        url = f"{self.base_url}/step"
        payload = action.to_dict()
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            obs_data = data.get("observation", {})
            observation = SecurityAuditObservation(obs_data)
            reward = data.get("reward", 0.0)
            done = data.get("done", False)
            return observation, reward, done
        except Exception as e:
            print(f"Error stepping environment: {e}")
            raise

# ============================================================================
# SECTION 4: LLM AGENT
# ============================================================================

class LLMAgent:
    """Greedy LLM agent using OpenAI client."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not set. LLM agent may not work.")
    
    def encode_observation(self, obs: SecurityAuditObservation) -> str:
        """Convert observation to text for model input."""
        parts = [
            f"Current Phase: {obs.current_phase}",
            f"Discovered Hosts: {', '.join(obs.discovered_hosts) if obs.discovered_hosts else 'None'}",
            f"Discovered Services: {json.dumps(obs.discovered_services) if obs.discovered_services else 'None'}",
            f"Findings Submitted: {obs.findings_submitted}",
            f"Steps Remaining: {obs.steps_remaining}",
            f"Last Message: {obs.message[:100]}",
        ]
        return "\n".join(parts)
    
    def generate_action(self, obs: SecurityAuditObservation) -> SecurityAuditAction:
        """Generate action from observation using LLM."""
        obs_text = self.encode_observation(obs)
        
        prompt = f"""You are a security auditor analyzing a target network.

Current Observation:
{obs_text}

Available Actions:
1. list_tools - Get available security tools
2. use_tool - Execute a security tool (requires tool_name and arguments)
3. submit_finding - Report a vulnerability
4. generate_report - End the audit

Based on the current phase and discovered information, choose the BEST next action.
Respond with ONLY a valid JSON object, no other text:

{{
  "action_type": "list_tools" | "use_tool" | "submit_finding" | "generate_report",
  "tool_name": "network_scan" | "service_fingerprint" | "web_crawl" | "vulnerability_scan" | null,
  "arguments": {{"host": "192.168.1.1"}} or {{"title": "...", "host": "...", "severity": "..."}} or {{}}
}}

Choose wisely to maximize vulnerabilities found and minimize wasted steps."""
        
        try:
            # Use OpenAI client pattern
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a security auditor. Respond with only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200,
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON from response
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    action_json = json.loads(response_text[json_start:json_end])
                    return SecurityAuditAction(
                        action_type=action_json.get("action_type", "list_tools"),
                        tool_name=action_json.get("tool_name"),
                        arguments=action_json.get("arguments", {})
                    )
            except json.JSONDecodeError:
                pass
        
        except Exception as e:
            print(f"LLM error: {e}")
        
        # Fallback to list_tools
        return SecurityAuditAction(action_type="list_tools")

# ============================================================================
# SECTION 5: RANDOM AGENT
# ============================================================================

class RandomAgent:
    """Random agent that picks random valid actions."""
    
    def generate_action(self, obs: SecurityAuditObservation) -> SecurityAuditAction:
        """Generate random action."""
        action_types = ["list_tools", "use_tool", "submit_finding"]
        action_type = random.choice(action_types)
        
        if action_type == "use_tool":
            tools = ["network_scan", "service_fingerprint", "web_crawl", "vulnerability_scan"]
            return SecurityAuditAction(
                action_type="use_tool",
                tool_name=random.choice(tools),
                arguments={"host": f"192.168.1.{random.randint(1, 10)}"}
            )
        elif action_type == "submit_finding":
            return SecurityAuditAction(
                action_type="submit_finding",
                arguments={
                    "title": f"Finding {random.randint(1, 100)}",
                    "host": f"192.168.1.{random.randint(1, 10)}",
                    "severity": random.choice(["low", "medium", "high"]),
                    "cvss_score": round(random.uniform(3.0, 9.8), 1),
                    "cwe": f"CWE-{random.randint(1, 1000)}",
                    "owasp": random.choice(["A01:2021", "A02:2021", "A03:2021"])
                }
            )
        else:
            return SecurityAuditAction(action_type="list_tools")

# ============================================================================
# SECTION 6: EPISODE RUNNER
# ============================================================================

def run_episode(agent, env: SecurityAuditEnv, agent_name: str, 
                episode_num: int, max_steps: int) -> EpisodeMetrics:
    """Run a single episode with an agent."""
    print(f"  {agent_name} Episode {episode_num + 1}/10", end=" ", flush=True)
    
    obs = env.reset(scenario_id="easy")
    metrics = EpisodeMetrics(episode_num=episode_num + 1)
    
    step = 0
    while not obs.done and step < max_steps:
        # Generate action
        action = agent.generate_action(obs)
        
        # Step environment
        obs, reward, done = env.step(action)
        
        # Track metrics
        metrics.total_reward += reward
        metrics.cumulative_rewards.append(metrics.total_reward)
        metrics.actions_taken.append(action.action_type)
        metrics.steps_taken += 1
        
        # Count vulnerabilities (from findings_submitted)
        metrics.vulnerabilities_found = obs.findings_submitted
        
        step += 1
    
    print(f"→ Reward: {metrics.total_reward:.4f}, Vulns: {metrics.vulnerabilities_found}")
    return metrics

# ============================================================================
# SECTION 7: PLOTTING
# ============================================================================

def plot_episode_rewards(random_metrics: AgentMetrics, llm_metrics: AgentMetrics, 
                        output_path: str, dpi: int = 150):
    """Plot 1: Episode rewards comparison."""
    plt.figure(figsize=(10, 6))
    
    episodes = list(range(1, len(random_metrics.episodes) + 1))
    random_rewards = random_metrics.episode_rewards
    llm_rewards = llm_metrics.episode_rewards
    
    plt.plot(episodes, random_rewards, 'r--', marker='o', linewidth=2, 
             markersize=8, label='Random Agent', alpha=0.8)
    plt.plot(episodes, llm_rewards, 'b-', marker='s', linewidth=2, 
             markersize=8, label='LLM Agent', alpha=0.8)
    
    plt.xlabel('Episode', fontsize=12, fontweight='bold')
    plt.ylabel('Total Reward (0.0 - 1.0)', fontsize=12, fontweight='bold')
    plt.title('AISHA: Episode Reward — Random vs LLM Agent', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.xticks(episodes)
    plt.ylim(0, max(max(random_rewards), max(llm_rewards)) * 1.1)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved {output_path}")
    plt.close()

def plot_cumulative_rewards(random_metrics: AgentMetrics, llm_metrics: AgentMetrics,
                           output_path: str, dpi: int = 150):
    """Plot 2: Cumulative reward curves with std dev bands."""
    plt.figure(figsize=(12, 6))
    
    # Get cumulative reward curves
    random_curves = random_metrics.cumulative_reward_curves
    llm_curves = llm_metrics.cumulative_reward_curves
    
    # Pad curves to same length
    max_len = max(max(len(c) for c in random_curves), max(len(c) for c in llm_curves))
    
    random_curves_padded = []
    for curve in random_curves:
        padded = list(curve) + [curve[-1]] * (max_len - len(curve))
        random_curves_padded.append(padded)
    
    llm_curves_padded = []
    for curve in llm_curves:
        padded = list(curve) + [curve[-1]] * (max_len - len(curve))
        llm_curves_padded.append(padded)
    
    # Compute mean and std
    random_mean = np.mean(random_curves_padded, axis=0)
    random_std = np.std(random_curves_padded, axis=0)
    
    llm_mean = np.mean(llm_curves_padded, axis=0)
    llm_std = np.std(llm_curves_padded, axis=0)
    
    steps = np.arange(len(random_mean))
    
    # Plot with shaded std dev bands
    plt.plot(steps, random_mean, 'r--', linewidth=2.5, label='Random Agent', alpha=0.8)
    plt.fill_between(steps, random_mean - random_std, random_mean + random_std, 
                     color='red', alpha=0.15)
    
    plt.plot(steps, llm_mean, 'b-', linewidth=2.5, label='LLM Agent', alpha=0.8)
    plt.fill_between(steps, llm_mean - llm_std, llm_mean + llm_std, 
                     color='blue', alpha=0.15)
    
    plt.xlabel('Step', fontsize=12, fontweight='bold')
    plt.ylabel('Cumulative Reward', fontsize=12, fontweight='bold')
    plt.title('AISHA: Cumulative Reward Over Steps', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved {output_path}")
    plt.close()

def plot_vulnerabilities_found(random_metrics: AgentMetrics, llm_metrics: AgentMetrics,
                              output_path: str, dpi: int = 150):
    """Plot 3: Vulnerability detection rate."""
    plt.figure(figsize=(10, 6))
    
    episodes = list(range(1, len(random_metrics.episodes) + 1))
    random_vulns = [e.vulnerabilities_found for e in random_metrics.episodes]
    llm_vulns = [e.vulnerabilities_found for e in llm_metrics.episodes]
    
    x = np.arange(len(episodes))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, random_vulns, width, label='Random Agent', 
                    color='#ff7f0e', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = plt.bar(x + width/2, llm_vulns, width, label='LLM Agent', 
                    color='#2ca02c', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.xlabel('Episode', fontsize=12, fontweight='bold')
    plt.ylabel('Vulnerabilities Found / Total (3)', fontsize=12, fontweight='bold')
    plt.title('AISHA: Vulnerability Detection Rate', fontsize=14, fontweight='bold')
    plt.xticks(x, episodes)
    plt.ylim(0, 3.5)
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved {output_path}")
    plt.close()

# ============================================================================
# SECTION 8: SUMMARY TABLE
# ============================================================================

def print_summary_table(random_metrics: AgentMetrics, llm_metrics: AgentMetrics):
    """Print summary table."""
    print("\n" + "=" * 70)
    print("AISHA AGENT COMPARISON SUMMARY")
    print("=" * 70)
    
    print(f"\n{'Metric':<25} {'Random Agent':<20} {'LLM Agent':<20}")
    print("-" * 70)
    
    # Average episode reward
    print(f"{'Avg Episode Reward':<25} {random_metrics.avg_episode_reward:<20.4f} {llm_metrics.avg_episode_reward:<20.4f}")
    
    # Average vulnerabilities found
    print(f"{'Avg Vulns Found':<25} {random_metrics.avg_vulns_found:<20.1f} / 3 {llm_metrics.avg_vulns_found:<20.1f} / 3")
    
    # Best episode score
    print(f"{'Best Episode Score':<25} {random_metrics.best_episode_reward:<20.4f} {llm_metrics.best_episode_reward:<20.4f}")
    
    # Std dev of rewards
    random_std = np.std(random_metrics.episode_rewards)
    llm_std = np.std(llm_metrics.episode_rewards)
    print(f"{'Reward Std Dev':<25} {random_std:<20.4f} {llm_std:<20.4f}")
    
    # Min episode score
    random_min = min(random_metrics.episode_rewards)
    llm_min = min(llm_metrics.episode_rewards)
    print(f"{'Min Episode Score':<25} {random_min:<20.4f} {llm_min:<20.4f}")
    
    # Improvement
    improvement = ((llm_metrics.avg_episode_reward - random_metrics.avg_episode_reward) / 
                   abs(random_metrics.avg_episode_reward)) * 100 if random_metrics.avg_episode_reward != 0 else 0
    print(f"{'LLM Improvement':<25} {improvement:>19.1f}%")
    
    print("=" * 70 + "\n")

# ============================================================================
# SECTION 9: MAIN
# ============================================================================

def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("AISHA AGENT COMPARISON")
    print("=" * 70)
    
    # Setup
    config = Config()
    print(f"\nConfiguration:")
    print(f"  Environment: {config.api_base_url}")
    print(f"  Scenario: {config.scenario_id}")
    print(f"  Episodes: {config.num_episodes}")
    print(f"  Max steps per episode: {config.max_steps_per_episode}")
    print(f"  LLM Model: {config.model_name}")
    print(f"  Output directory: {config.plots_dir}")
    
    # Initialize environment
    print(f"\nInitializing environment...")
    env = SecurityAuditEnv(base_url=config.api_base_url)
    
    # Test connection
    try:
        obs = env.reset(scenario_id=config.scenario_id)
        print(f"✓ Environment connected")
    except Exception as e:
        print(f"✗ Failed to connect to environment: {e}")
        return
    
    # Initialize agents
    print(f"\nInitializing agents...")
    random_agent = RandomAgent()
    llm_agent = LLMAgent(model_name=config.model_name)
    print(f"✓ Agents initialized")
    
    # Run random agent
    print(f"\n{'=' * 70}")
    print("RANDOM AGENT - Running 10 episodes")
    print("=" * 70)
    random_metrics = AgentMetrics(agent_name="Random Agent")
    for episode in range(config.num_episodes):
        metrics = run_episode(random_agent, env, "Random", episode, config.max_steps_per_episode)
        random_metrics.episodes.append(metrics)
    
    # Run LLM agent
    print(f"\n{'=' * 70}")
    print("LLM AGENT - Running 10 episodes")
    print("=" * 70)
    llm_metrics = AgentMetrics(agent_name="LLM Agent")
    for episode in range(config.num_episodes):
        metrics = run_episode(llm_agent, env, "LLM", episode, config.max_steps_per_episode)
        llm_metrics.episodes.append(metrics)
    
    # Generate plots
    print(f"\n{'=' * 70}")
    print("GENERATING PLOTS")
    print("=" * 70)
    
    plot_episode_rewards(random_metrics, llm_metrics, 
                        f"{config.plots_dir}/reward_per_episode.png", 
                        dpi=config.dpi)
    
    plot_cumulative_rewards(random_metrics, llm_metrics,
                           f"{config.plots_dir}/cumulative_reward_curve.png",
                           dpi=config.dpi)
    
    plot_vulnerabilities_found(random_metrics, llm_metrics,
                              f"{config.plots_dir}/vulns_found.png",
                              dpi=config.dpi)
    
    # Print summary
    print_summary_table(random_metrics, llm_metrics)
    
    print(f"✓ All plots saved to {config.plots_dir}/")
    print(f"✓ Comparison complete!")

if __name__ == "__main__":
    main()
