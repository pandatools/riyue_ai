from collections import deque
import random

import torch
import torch.nn as nn
import torch.optim as optim

from aim_game.game import game
from aim_game.rule import NumberObj


class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(5 + 12 + 1, 128),  # 5个骰子 + 13个计分类别状态 + 1个剩余回合数
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 12)  # 输出每个计分类别的 Q 值
        )

    def forward(self, state):
        return self.fc(state)
new_game = game()
obj = NumberObj()

def train_dqn(num_epochs=10000, batch_size=64):
    q_network = DQN()
    optimizer = optim.Adam(q_network.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    # 经验回放缓冲区
    replay_buffer = deque(maxlen=10000)
    gamma = 0.99  # 折扣因子
    total_reward = 0

    for epoch in range(num_epochs):
        new_game.game_init()

        while new_game.running:
            touzi = new_game.roll(5)
            state = torch.tensor(
                list(touzi) +
                new_game.game_state +
                [new_game.remain_rounds],
                dtype=torch.float32
            )

            # ε-贪心策略选择动作
            # if random.random() < 0.1:  # 探索
            #     action = random.choice([k for k,v in new_game.ways.items() if v is None])
            # else:  # 利用
            q_values = q_network(state)
            valid_actions = [k for k,v in new_game.ways.items() if v is None]
            action_idx = torch.argmax(q_values[[new_game.ways_sort.index(a) for a in valid_actions]]).item()
            action = valid_actions[action_idx]

            # 应用动作并获取奖励
            reward = new_game.apply_action(touzi,action,obj)
            total_reward += reward

            # 保存经验
            next_state = torch.tensor(
                list(touzi) +
                new_game.game_state +
                [new_game.remain_rounds],
                dtype=torch.float32
            )
            number_action = new_game.ways_sort.index(action)
            replay_buffer.append((state, number_action, reward, next_state, not new_game.running))

            # 从缓冲区采样训练
            if len(replay_buffer) >= batch_size:
                batch = random.sample(replay_buffer, batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)

                states = torch.stack(states)
                next_states = torch.stack(next_states)
                rewards = torch.tensor(rewards, dtype=torch.float32)
                dones = torch.tensor(dones, dtype=torch.float32)

                q_values = q_network(states)
                q_values = q_values[range(batch_size), actions]
                next_q_values = q_network(next_states).max(dim=1)[0]
                target_q_values = rewards + gamma * next_q_values * (1 - dones)

                optimizer.zero_grad()
                loss = loss_fn(q_values, target_q_values)
                loss.backward()
                optimizer.step()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}: Total Reward = {total_reward/100}")
            torch.save(q_network.state_dict(), "dqn_model.pth")
            total_reward = 0

    return q_network
if __name__ == '__main__':

    train_dqn()