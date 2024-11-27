import torch
from aim_game.game import game
from aim_game.gan import DQN
from aim_game.rule import NumberObj


def play_with_trained_model(model_path):
    # 加载训练好的模型
    q_network = DQN()
    q_network.load_state_dict(torch.load(model_path))
    q_network.eval()  # 设置为评估模式

    # 初始化游戏和规则
    new_game = game()
    obj = NumberObj()
    new_game.game_init()

    total_reward = 0

    # 使用模型玩游戏
    while new_game.running:
        # 骰子状态
        touzi = new_game.roll(5)
        # 构造当前状态
        current_state = torch.tensor(
            list(touzi) + new_game.game_state + [new_game.remain_rounds],
            dtype=torch.float32
        ).unsqueeze(0)  # 添加 batch 维度

        # 模型预测动作
        with torch.no_grad():
            q_values = q_network(current_state)

            q_values = q_values.squeeze(0)
            valid_actions = [k for k, v in new_game.ways.items() if v is None]
            valid_q_values = q_values[[new_game.ways_sort.index(a) for a in valid_actions]]
            action_idx = torch.argmax(valid_q_values).item()
            action = valid_actions[action_idx]
        # 执行动作并获取奖励
        reward = new_game.apply_action(touzi, action, obj)
        total_reward += reward
        print(f"动作: {action}, 奖励: {reward}")

    print(f"游戏结束，总奖励: {total_reward}")


if __name__ == "__main__":
    # 模型文件路径
    model_path = "dqn_model.pth"
    play_with_trained_model(model_path)
