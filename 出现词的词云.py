# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:24:27 2020
@author: Justin
"""
'''
从CSV文件中读出人物词频
用pyecharts画出词云，并做形状、轮廓图、字体等配置
'''
from pyecharts import options as opts
from pyecharts.charts import WordCloud

##-------从文件中读出人物词频------------------
src_filename = 'bilibili_words_count.csv'
# 格式：人物,出现次数

src_file = open(src_filename, 'r')
line_list = src_file.readlines()  #返回列表，文件中的一行是一个元素
src_file.close()

wordfreq_list = []  #用于保存元组(人物姓名,出现次数)
for line in line_list:
    line = line.strip()  #删除'\n'
    line_split = line.split(',')
    wordfreq_list.append((line_split[0],line_split[1]))

del wordfreq_list[0] #删除csv文件中的标题行
print('人物数量：' + str(len(wordfreq_list)))
##-------从文件中读出人物词频完成------------------

##===============================================
##-------生成词云---------------------------------
cloud = WordCloud()

# 设置词云图
cloud.add('', 
          wordfreq_list[0:90], #元组列表，词和词频
          shape='circle',# 轮廓形状：'circle','cardioid','diamond',                                选择词云的形状
                           # 'triangle-forward','triangle','pentagon','star'
          #mask_image='./data/词云背景图-蝴蝶.jpg', # 轮廓图，第一次显示可能有问题，刷新即可
          is_draw_out_of_bound=False, #允许词云超出画布边界
          word_size_range=[15, 50], #字体大小范围
          textstyle_opts=opts.TextStyleOpts(font_family="华文行楷"),
          #字体：例如，微软雅黑，宋体，华文行楷，Arial
          )

# 设置标题
cloud.set_global_opts(title_opts=opts.TitleOpts(title="热门视频词云"))

# render会生成HTML文件。默认是当前目录render.html，也可以指定文件名参数
out_filename = './output/wordcloud_opts.html'
cloud.render(out_filename)

print('生成结果文件：' + out_filename)

