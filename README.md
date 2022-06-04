# social_media_spy
刺探敵情小幫手：幫助你分析Facebook粉專！  

# 使用說明
1. 在終端機輸入以下指令以下載必要之模組及套件：
`pip install selenium BeautifulSoup requests lxml numpy scipy matplotlib jieba wordcloud`
2. 下載並解壓縮本程式包
3. 下載chrome，並確認chrome版本（可從右上角 `...` >> 設定 >> 關於chrome 查看  
4. 至以下網址下載對應版本之ChromeDriver  
https://sites.google.com/chromium.org/driver/  
安裝完畢後複製路徑，建議將chromedriver放在 `social_media_spy-main` 資料夾，則路徑僅需輸入 `./chromedriver` 即可  
5. 使用時，開啟終端機於 `social_media_spy-main` 資料夾下輸入指令：
 `python main.py` 或 `python3 main.py` ，並依指示依序輸入chromedriver路徑、粉專網址、頁面捲動次數、帳號、密碼，結果之折線圖與文字雲圖檔將會自動儲存至 `social_media_spy-main` 資料夾下  
※ 帳號、密碼僅為查看Facebook文章留言所需，本程式不會以任何形式記錄或傳送使用者之帳號密碼
