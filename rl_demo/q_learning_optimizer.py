"""
Educational Reinforcement Learning Demonstration: Q-Learning Path Optimizer
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import random
import numpy as np

# Syllabus Educational Module: Q-Learning for Step-by-Step Learning Path Optimization

STATES = [
    "Foundational (Beginner)",
    "Core Programming (Intermediate)",
    "Applied AI/ML (Advanced)",
    "Production & Cloud (Industry Ready)"
]

ACTIONS = [
    "Study Python & Core DSA",
    "Build Web & Database App",
    "Train Supervised ML Models",
    "Implement Deep Neural Networks",
    "Deploy Containerized API to Cloud",
    "Complete Full-Stack Capstone Project"
]

# Transition Dynamics & Reward Matrix
# Format: (next_state_idx, expected_reward)
ACTION_TRANSITIONS = {
    0: {  # Foundational
        0: (1, 10.0),   # Studying Python progresses to Core
        1: (0, 3.0),    # Web is a bit early
        2: (0, -2.0),   # ML without Python is hard
        3: (0, -5.0),   # DL is too advanced
        4: (0, -5.0),   # Cloud is too advanced
        5: (0, -10.0)   # Capstone too early
    },
    1: {  # Core Programming
        0: (1, 2.0),    # Reviewing Python
        1: (1, 8.0),    # Web is helpful
        2: (2, 12.0),   # Perfect time for ML
        3: (1, 4.0),    # DL without ML
        4: (2, 7.0),    # Cloud is good
        5: (1, 2.0)
    },
    2: {  # Applied AI/ML
        0: (2, 1.0),
        1: (2, 5.0),
        2: (2, 6.0),
        3: (3, 14.0),   # DL transitions to Industry Ready
        4: (3, 15.0),   # Cloud/Deployment transitions to Industry Ready
        5: (3, 18.0)    # Capstone gives high reward
    },
    3: {  # Production & Cloud
        0: (3, 1.0),
        1: (3, 4.0),
        2: (3, 5.0),
        3: (3, 8.0),
        4: (3, 10.0),
        5: (3, 25.0)    # Capstone mastery
    }
}

class QLearningPathOptimizer:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2, episodes=300):
        self.alpha = alpha      # Learning Rate
        self.gamma = gamma      # Discount Factor
        self.epsilon = epsilon  # Exploration Rate
        self.episodes = episodes
        self.num_states = len(STATES)
        self.num_actions = len(ACTIONS)
        self.q_table = np.zeros((self.num_states, self.num_actions))
        self.episode_rewards = []
        
    def train(self):
        """Train Q-Table across episodes."""
        random.seed(42)
        np.random.seed(42)
        
        for ep in range(self.episodes):
            current_state = 0  # Start at Beginner
            total_reward = 0
            steps = 0
            
            while current_state < self.num_states - 1 and steps < 10:
                # Epsilon-Greedy Action Selection
                if random.random() < self.epsilon:
                    action = random.randint(0, self.num_actions - 1)
                else:
                    action = int(np.argmax(self.q_table[current_state]))
                    
                next_state, reward = ACTION_TRANSITIONS[current_state][action]
                
                # Q-Value Bellman Update
                best_next_action_q = np.max(self.q_table[next_state])
                td_target = reward + self.gamma * best_next_action_q
                td_error = td_target - self.q_table[current_state, action]
                self.q_table[current_state, action] += self.alpha * td_error
                
                total_reward += reward
                current_state = next_state
                steps += 1
                
            self.episode_rewards.append(round(total_reward, 2))
            
    def get_optimal_path(self):
        """Extract optimal sequence of actions from Q-table."""
        path = []
        curr_state = 0
        visited = set()
        
        while curr_state < self.num_states and curr_state not in visited:
            visited.add(curr_state)
            best_action_idx = int(np.argmax(self.q_table[curr_state]))
            action_name = ACTIONS[best_action_idx]
            q_val = round(float(self.q_table[curr_state, best_action_idx]), 3)
            next_state, expected_rew = ACTION_TRANSITIONS[curr_state][best_action_idx]
            
            path.append({
                "step": len(path) + 1,
                "current_state": STATES[curr_state],
                "recommended_action": action_name,
                "q_value": q_val,
                "expected_reward": expected_rew,
                "next_state": STATES[next_state]
            })
            if curr_state == next_state or next_state == self.num_states - 1:
                break
            curr_state = next_state
            
        return path

    def get_q_table_dataframe(self):
        import pandas as pd
        df = pd.DataFrame(
            np.round(self.q_table, 2),
            index=STATES,
            columns=ACTIONS
        )
        return df

def run_rl_simulation(episodes=300, alpha=0.1, gamma=0.9):
    agent = QLearningPathOptimizer(alpha=alpha, gamma=gamma, episodes=episodes)
    agent.train()
    path = agent.get_optimal_path()
    q_df = agent.get_q_table_dataframe()
    return {
        "optimal_path": path,
        "q_table": q_df.to_dict(),
        "episode_rewards": agent.episode_rewards[::max(1, len(agent.episode_rewards) // 30)],
        "episodes_total": episodes
    }

if __name__ == "__main__":
    res = run_rl_simulation()
    print("=== Optimal Learning Path Identified by Q-Learning ===")
    for step in res["optimal_path"]:
        print(f"Step {step['step']}: At [{step['current_state']}] -> Take '{step['recommended_action']}' (Q: {step['q_value']}) -> Result: [{step['next_state']}]")
