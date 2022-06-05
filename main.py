# 刺探敵情小幫手
## Step 1. 預先準備
'''
1. 在終端機輸入以下指令以下載必要模組：
pip install selenium BeautifulSoup requests lxml jieba numpy scipy wordcloud
2. 至以下網址下載ChromeDriver，安裝完畢後複製路徑
https://sites.google.com/chromium.org/driver/
詳細使用說明請查看 readme
'''

## Step 2. 安裝並匯入相關套件或模組
# 爬蟲相關套件
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import math
import os
import requests
import heapq
from getpass import getpass

# 折線圖相關套件
import numpy as np
import matplotlib.pyplot as plt

# 文字雲相關套件
import jieba
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude as ggm
import wordcloud

# 時間相關套件
from datetime import datetime
import time

## Step 3. 爬蟲
driver_path = input('請輸入webdriver路徑：')
while True:
    # 阻擋彈出式頁面
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values' :
            {
            'notifications' : 2
             }
    }
    options.add_experimental_option('prefs', prefs)
    
    # 開啟Facebook頁面
    input('Enter以重新啟動：')
    driver = webdriver.Chrome(driver_path, options = options)
    url = 'https://www.facebook.com'
    driver.get(url)
    url = input('請貼上粉專網址：') 
    driver.get(url)
    
    # 將該社團或粉絲專頁的貼文載入
    # 捲動頁面
    scrolls = int(input('請輸入希望捲動的頁面次數：'))
    time.sleep(3)
    for x in range(scrolls):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        
    root = Soup(driver.page_source, "html.parser")
    # 粉專名稱爬蟲
    Name_frame = root.find("div", class_= 'bi6gxh9e aov4n071')
    try:
        the_name = Name_frame.find("span", class_ = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 ns63r2gh rwim8176 m6dqt4wy h7mekvxk hnhda86s oo9gr5id hzawbc8m').text
    except:
        the_name = Name_frame.find("h1", class_ = 'gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl').text

    # 標題爬蟲
    titles_list = []
    temporary_post = []
    titles = root.find_all("div", class_= 'ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a')
    for title in titles:
        temporary_post= []
        posts = title.find_all("div", dir = "auto")
        # 如果有文章標題才印出
        if len(posts) != 0:
            for post in posts:
                temporary_post.append(post.text)
            titles_list.append(temporary_post)

    # 貼文的link爬蟲
    frames = root.find_all(class_ = 'll8tlv6m j83agx80 btwxx1t3 n851cfcs hv4rvrfc dati1w0a pybr56ya')
    links = []
    for ii in frames: 
        link_coulum = ii.find('span', class_ = 'tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41')
        if(link_coulum == None): 
            links.append('0')
        else:
            links.append(link_coulum.a["href"])    

    # 時間爬蟲
    frames = root.find_all(class_ = 'll8tlv6m j83agx80 btwxx1t3 n851cfcs hv4rvrfc dati1w0a pybr56ya')
    times = []
    for ii in frames: 
        time_coulum = ii.find('span',class_ = 'tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41')
        if(time_coulum == None): 
            times.append('0')
        else:
            times.append(time_coulum.text)

    soup = Soup(driver.page_source, 'lxml')
    frames = soup.find_all(class_ = 'stjgntxs ni8dbmo4 l82x9zwi uo3d90p7 h905i5nu monazrh9')

    comments = []
    likes = []
    shares = []

    for ii in frames: 
        finding =ii.text
        
        # 留言數爬蟲
        comment_coulum = ii.find('span',class_ = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain')
        if(comment_coulum == None) or finding.find('次分享') < finding.find('留言'): 
            comments.append('0則留言')
        else:
            comments.append(comment_coulum.text)

        # 分享數爬蟲，因span跟留言一樣，稍做修正
        finding = ii.text
        try:
            share_begin_num = finding.index('言') + 1
            share_end_num = finding.index('次')
            share = finding[share_begin_num:share_end_num]
            if len(share) == 0:
                shares.append(0)
            else:
                shares.append(int(share))
        except:
            shares.append(0)

        # 讚數爬蟲
        like_coulum = ii.find('span', class_= 'pcp91wgn')
        if(like_coulum == None): 
            likes.append('0')
        else:
            likes.append(like_coulum.text)
    
    # 按讚數/留言數/分享數資料整理
    for i in range(len(likes)):  
        if(likes[i].find('\xa0萬') != -1):
            likes[i] = int(float(likes[i][:likes[i].find('\xa0萬')])*10000)
        else:
            likes[i] = int(likes[i].replace(',', ''))

    for j in range(len(comments)):
        try:
            index = comments[j].find('則')
            comments[j] = int(comments[j][:index].replace(',', ''))
        except:
            pass
        
    for k in range(len(shares)):
        k = int(k)
        
    # 確定爬蟲資料無誤，若有誤則重新再爬一次
    if len(times) == len(likes) == len(comments) == len(shares) and len(likes) > 3 :
        break
    else:
        print('很抱歉！受網路速度影響，導致爬蟲結果不完整，請重新輸入。')
        continue
           
# 找出讚數前三高的貼文連結進行留言爬蟲
best_3 = map(likes.index, heapq.nlargest(3,likes))
best_links = []
for z in best_3:
    z = int(z)
    best_links.append(links[z])
        
# 留言爬蟲
account = input('請輸入帳號：')
psw = getpass('請輸入密碼：')
while True:
    comments_list = []
    for i in range(3):  
        driver.get(best_links[i])
        wait = WebDriverWait(driver, 30)
        try:
            email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
            email_field.send_keys(account)
            pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
            pass_field.send_keys(psw)
            pass_field.send_keys(Keys.RETURN)
            time.sleep(5)
        except:
            pass
        time.sleep(5)
        roots = Soup(driver.page_source, "html.parser")
        comments_ = roots.find_all(class_ = "tw6a2znq sj5x9vvc d1544ag0 cxgpxx05")
        for comment in comments_:
            content = comment.find_all(class_ = "ecm0bbzt e5nlhep0 a8c37x1j")
            if len(content) != 0:
                for cont in content:
                    comments_list.append(cont.text)
            # else:
            #     comments_list.append('')
    if len(comments_list) > 0:
        break
    else:
        print('很抱歉！受網路速度影響，導致爬蟲結果不完整，將再次嘗試。')
        continue

## Step 4. 視覺化｜繪製折線圖
# 設定圖片的中文字型、解析度、長寬與背景色
plt.rcParams['font.sans-serif'] = ['PingFang HK'] # 處理matplotlib無法顯示中文的問題
fig = plt.figure(figsize = (20,10), dpi = 500, linewidth = 2) 
font1 = {'weight': 'normal', 'size': 18} 
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['savefig.facecolor'] = 'none'

# 將數據從list改為ndarray格式，以避免ValueError
times = np.array(times)
likes = np.array(likes)
comments = np.array(comments)
shares = np.array(shares)

# 畫線
plt.plot(times, likes, color = '#1F7A8C', linestyle = "-", linewidth = "2",
         markersize = "15", marker = ".", label = '心情數')
plt.plot(times, comments, color = '#EB9486', linestyle = "-", linewidth = "2",
         markersize = "15", marker = ".", label = '留言數')
plt.plot(times, shares, color = '#419D78', linestyle = "-", linewidth = "2",
         markersize = "15", marker = ".", label = '分享數')

# 設定x軸、y軸參數
plt.xticks(np.arange(0, len(times), 1.0 ), fontsize = 15, rotation = 270) 
plt.yticks(np.arange(0, max(likes), 1000 ), fontsize = 15) 
plt.xlabel('發文時間', fontsize = '18') # 設定x軸標題內容及大小
plt.ylabel('數據成效', fontsize = '18') # 設定y軸標題內容及大小
plt.title(the_name, fontweight = 'bold', fontsize = '25') # 設定圖表標題內容及大小
plt.legend(prop = font1) # 圖例

# 繪製資料標籤
for x, y in zip(times, likes):
    plt.text(x, y, y, ha = 'center', va = 'bottom', fontsize = 15)
for x, y in zip(times, comments):
    plt.text(x, y, y, ha = 'center', va = 'bottom', fontsize = 15)
for x, y in zip(times, shares):
    plt.text(x, y, y, ha = 'center', va = 'top', fontsize = 15)

## Step 5. 視覺化｜繪製文字雲
# reading the article
article = ""
for c in comments_list:
        article += c + '\n'

# using jeiba mod to split the article
words = jieba.lcut(article)

# generate color function
# generate from image
image = np.array(Image.open('2021_Facebook_icon.svg.png'))
my_colors_func = wordcloud.ImageColorGenerator(image)
# mask
my_mask = image.copy()
my_mask[my_mask.sum(axis=2) == 0] = 255
edges = np.mean([ggm(my_mask[:, :, i] / 255., 2) for i in range(3)], axis=0)
my_mask[edges > .08] = 255

# using wordcloud mod
j = ' '.join(words)
# setting
sw = {"你","妳","我","他","的","之","是","有","在","再","就","卻","都","也",
      "好","很","了","啦","吧","啊","呢","顯示更多","顯示","更多","更","多"}
c = wordcloud.WordCloud(font_path = '/System/Library/Fonts/PingFang.ttc', \
                        width = 1000, height = 1000, scale = 1, \
                        prefer_horizontal = 0.95, \
                        min_font_size = 20, max_font_size = None, \
                        background_color = "rgba(255,255,255,0)", \
                        mode = "RGBA", \
                        mask = my_mask, \
                        color_func = my_colors_func, \
                        stopwords = sw, \
                        min_word_length = 1)
c.generate(j)

## Step 6. 處理輸出
# output with time stamp
local_time = time.localtime()
output_time = time.strftime('%m%d%H%M', local_time)
fig.savefig(f'折線圖_{output_time}.png')
c.to_file(f'文字雲_{output_time}.png')