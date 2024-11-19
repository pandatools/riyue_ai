import pandas as pd

# 创建一个包含类别列的数据框
data = pd.DataFrame({
    'color': ['红', '蓝', '绿', '红', '绿']
})

print("原始数据框：")
print(data)

# 使用 pd.get_dummies() 进行独热编码
encoded_data = pd.get_dummies(data['color'])

print("\n独热编码后的数据：")
print(encoded_data)
