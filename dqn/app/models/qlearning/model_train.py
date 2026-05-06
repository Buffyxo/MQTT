import torch
from models.qlearning.energy_environment import EnergyEnvironment
from models.qlearning.replay_buffer import ReplayBuffer
from models.qlearning.dqn import DQN
import random
import logging
import numpy as np

logger = logging.getLogger(__name__)


def train(dqn: DQN, env: EnergyEnvironment, buffer: ReplayBuffer, episodes: int = 1000):
    epsilon = 1.0
    epsilon_min = 0.1
    epsilon_decay = 0.995
    gamma = 0.95
    batch_size = 32
    TARGET_UPDATE_FREQ = 10

    optimizer = torch.optim.Adam(dqn.parameters(), lr=0.001)

    # Target network — same architecture, synced periodically
    target_dqn = DQN(input_size=18, output_size=5).to(dqn.device)
    target_dqn.load_state_dict(dqn.state_dict())
    target_dqn.eval()

    action_counts = {i: 0 for i in range(env.action_space.n)}

    for episode in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        loss = torch.empty([]).to(dqn.device)

        for step in range(24):
            # Epsilon-greedy
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = dqn.best_action(state)

            next_state, reward, done, truncated, info = env.step(action)
            buffer.push(state, action, reward, next_state, done)
            total_reward += reward
            action_counts[action] += 1

            # Train if buffer has enough
            if len(buffer) > batch_size:
                batch = buffer.sample(batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)

                states_t = torch.FloatTensor(np.array(states)).to(dqn.device)
                actions_t = torch.LongTensor(actions).to(dqn.device)
                rewards_t = torch.FloatTensor(rewards).to(dqn.device)
                next_states_t = torch.FloatTensor(np.array(next_states)).to(dqn.device)
                dones_t = torch.FloatTensor(dones).to(dqn.device)

                current_q = dqn(states_t).gather(1, actions_t.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    next_q = target_dqn(next_states_t).max(1)[0]
                target_q = rewards_t + gamma * next_q * (1 - dones_t)

                loss = torch.nn.functional.mse_loss(current_q, target_q)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            state = next_state
            if done:
                break

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        if episode % TARGET_UPDATE_FREQ == 0:
            target_dqn.load_state_dict(dqn.state_dict())

        if episode % 50 == 0:
            logger.info(
                f"Episode {episode} | Total Reward: {total_reward:.3f} "
                f"| Epsilon: {epsilon:.3f} | Loss: {loss.item():.4f}"
            )

    logger.info(f"Action distribution: {action_counts}")