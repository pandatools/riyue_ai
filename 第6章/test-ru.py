import torch
import torch.nn as nn

# 定义 LeakyReLU 激活函数
leaky_relu = nn.LeakyReLU()

# 示例输入
x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])

# 输出
output = leaky_relu(x)
print(output)
