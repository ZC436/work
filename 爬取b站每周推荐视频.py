from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json

# 配置选项
options = Options()
# options.add_argument("--headless")  # 启用无头模式

# 启动浏览器
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10) # 设置等待页面加载的最长超时时间

# 打开Bilibili主页来设置正确的域
browser.get('https://www.bilibili.com')

# 读取并添加Cookies
cookies_filename = './data/my_cookies.json'
with open(cookies_filename, 'r', encoding='utf-8') as cookies_file:
    cookies_list = json.load(cookies_file)

for cookie in cookies_list:
    if 'expiry' in cookie:
        cookie['expiry'] = int(cookie['expiry'])
    # 确保cookie的域与当前域匹配
    if 'domain' in cookie and not cookie['domain'].startswith('.bilibili.com'):
        cookie['domain'] = '.bilibili.com'
    browser.add_cookie(cookie)

# 打开目标URL
with open('bilibili_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['热点', '浏览人数', 'up主', '评论数'])

    # 循环访问页面
    for num in range(1, 273):
        url = f"https://www.bilibili.com/v/popular/weekly?num={num}"
        browser.get(url)
        time.sleep(5)  # 等待页面加载
        # 找到视频卡片元素
        items = browser.find_elements(By.CSS_SELECTOR, '.video-card')
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '.video-name').text
                viewers = item.find_element(By.CSS_SELECTOR, '.play-text').text
                author = item.find_element(By.CSS_SELECTOR, '.up-name').text
                comments = item.find_element(By.CSS_SELECTOR, '.like-text').text
                writer.writerow([title, viewers, author, comments])
                print(f"热点标题：{title}, 播放量：{viewers}，up主:{author}, 评论数：{comments}")
            except Exception as e:
                print(f"Error processing item: {e}")

# 关闭浏览器
browser.quit()

# 结束
print("Finished accessing all pages.")
