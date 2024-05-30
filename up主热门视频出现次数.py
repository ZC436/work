from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar
import chardet
import pandas as pd

# 检测文件编码

input_file = 'bilibili_third_column_count.csv'

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

    # 提取x轴和y轴数据
x_values = df['up主'].tolist()[:25]#出现次数
y_values = df['出现次数'].tolist()[:25]#与x轴11对应

# 创建Bar图表
c = (
    Bar()
    .add_xaxis(x_values)  # 使用CSV文件中的x轴数据
    .add_yaxis(
        "up主名字", 
        y_values,  # 使用CSV文件中的y轴数据
        itemstyle_opts=opts.ItemStyleOpts(color='green'),  # 设置颜色
        label_opts=opts.LabelOpts(position='insideBottom'),  # 设置标签位置
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="up主制作热门视频次数"),
         xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=45)  # 旋转x轴标签
        )
)
    .render("./output/up主制作热门视频次数.html")
)
print("完成")