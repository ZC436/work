import pandas as pd
from collections import Counter
import chardet
import jieba
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.font_manager import FontProperties

# 设置中文字体
font_path = 'C:\Windows\Fonts\STFANGSO.TTF'  # 替换为你系统中的中文字体路径
font_prop = FontProperties(fname=font_path)
# 检测文件编码

input_file = 'bilibili_data.csv'

with open(input_file, 'rb') as f:
    result = chardet.detect(f.read())
    file_encoding = result['encoding']
    print(f"检测到的文件编码：{file_encoding}")

# 使用检测到的编码读取CSV文件
try:
    df = pd.read_csv(input_file, encoding=file_encoding)
except UnicodeDecodeError:
    # 如果检测的编码不正确，尝试使用其他编码
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding='gbk')

# 检查数据结构
print(df.head())


#-----------处理第一列内容-
# 选取第一列数据
first_column_data = df.iloc[:, 0].astype(str)  # 转换为字符串类型

# 自定义忽略词列表
ignore_words = set(["什么","一个","我们","如何","这个","自己","这么","真的","10","竟然","可以","不要","无数"])  # 添加你想忽略的词

# 对第一列内容进行分词
words = []
for content in first_column_data:
    words.extend(jieba.lcut(content))

# 忽略标点符号，空格，只有一个字的数据，以及自定义忽略词
filtered_words = [word for word in words if len(word) > 1 and not re.match(r'^\W+$', word) and word not in ignore_words]

# 统计每个词出现的次数
counter = Counter(filtered_words)

# 将统计结果转换为DataFrame
result_df = pd.DataFrame(counter.items(), columns=['词语', '出现次数'])
# 根据出现次数降序排列
result_df = result_df.sort_values(by='出现次数', ascending=False)

# 将统计结果写入新的CSV文件
output_file = 'bilibili_words_count.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"统计结果已写入文件：{output_file}")
#------------------处理第三列内容
# 选取第三列数据（假设第三列是需要的列）
third_column_data = df.iloc[:, 2]  # .iloc[:, 2]选择第三列

# 统计第三列数据的出现次数
counter = Counter(third_column_data)

# 将统计结果转换为DataFrame
result_df = pd.DataFrame(counter.items(), columns=['up主', '出现次数'])
# 根据出现次数降序排列
result_df = result_df.sort_values(by='出现次数', ascending=False)

# 将统计结果写入新的CSV文件
output_file = 'bilibili_third_column_count.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"统计结果已写入文件：{output_file}")

first_column_data = df.iloc[:, 0].astype(str)  # 转换为字符串类型

#----------分析第观看人数与评论的函数关系-------
# 检查数据结构
print(df.head())

# 定义一个函数来转换包含“万”的字符串为数值
def convert_to_number(value):
    if isinstance(value, str):
        if '万' in value:
            return float(value.replace('万', '')) * 10000
        try:
            return float(value)
        except ValueError:
            return np.nan
    return value

# 应用转换函数到第二列和第四列数据
second_column_data = df.iloc[:, 1].astype(str).apply(convert_to_number)
fourth_column_data = df.iloc[:, 3].astype(str).apply(convert_to_number)

# 将处理后的数据重新赋值回DataFrame
df.iloc[:, 1] = second_column_data
df.iloc[:, 3] = fourth_column_data

# 过滤掉无法转换为浮点数的行
filtered_data = df.dropna(subset=[df.columns[1], df.columns[3]])

# 转换为浮点数
second_column_data = filtered_data.iloc[:, 1].astype(float)
fourth_column_data = filtered_data.iloc[:, 3].astype(float)

# 绘制散点图以观察数据分布
plt.scatter(second_column_data, fourth_column_data)
plt.xlabel('第二列数据', fontproperties=font_prop)
plt.ylabel('第四列数据', fontproperties=font_prop)
plt.title('第二列与第四列数据的散点图', fontproperties=font_prop)
plt.show()

# 计算线性回归
slope, intercept, r_value, p_value, std_err = linregress(second_column_data, fourth_column_data)

# 绘制回归线
plt.scatter(second_column_data, fourth_column_data, label='数据点')
plt.plot(second_column_data, intercept + slope * second_column_data, 'r', label='回归线')
plt.xlabel('浏览人数', fontproperties=font_prop)
plt.ylabel('评论数', fontproperties=font_prop)
plt.title('浏览人数与评论数的回归分析', fontproperties=font_prop)
plt.legend()
plt.show()
# 保持图像
plt.savefig('数据分析.png')
# 打印回归分析结果
print(f"斜率: {slope}")
print(f"截距: {intercept}")
print(f"相关系数 (R-squared): {r_value**2}")
print(f"p-value: {p_value}")
print(f"标准误差: {std_err}")
print("完成")