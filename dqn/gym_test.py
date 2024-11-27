import gymnasium as gym

# 创建 CartPole-v1 环境
env = gym.make("CartPole-v1")

# 重置环境，获取初始状态
obs, info = env.reset()

done = False
total_reward = 0

while not done:
    env.render()  # 可视化环境（需要支持 GUI）

    # 随机选择一个动作（0 或 1）
    action = env.action_space.sample()

    # 执行动作并获取返回值
    obs, reward, done, truncated, info = env.step(action)

    # 累计奖励
    total_reward += reward

    # 打印当前状态信息
    print(f"Observation: {obs}, Reward: {reward}, Done: {done}")

print(f"Total Reward: {total_reward}")
env.close()
