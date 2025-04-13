import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_billboard_japan_hot100():
    url = "https://www.billboard-japan.com/charts/detail?a=hot100"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 發送HTTP請求
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 解析HTML內容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取發布日期
        date_published = soup.find('p', class_='date').text.strip()
        
        # 找到排行榜表格
        chart_table = soup.find('table')
        rows = chart_table.find_all('tr')[1:]  # 跳過標題行
        
        chart_data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:  # 確保有足夠的列
                try:
                    # 提取排名
                    rank = cols[0].text.strip()
                    
                    # 提取歌曲信息
                    title = cols[1].find('p', class_='musuc_title').text.strip()
                    artist = cols[1].find('p', class_='artist_name').text.strip()
                    
                    # 提取上周排名
                    last_week_elem = cols[1].find('span', class_='last')
                    last_week = last_week_elem.text.replace('前回：', '').strip() if last_week_elem else "-"
                    
                    # 提取上榜週數
                    charts_in_elem = cols[1].find('span', class_='charts_in')
                    charts_in = charts_in_elem.text.replace('チャートイン：', '').strip() if charts_in_elem else "0"
                    
                    # 提取分數（如果存在）
                    score_elem = row.find('p', class_='num')
                    score = score_elem.text.strip() if score_elem else "N/A"
                    
                    chart_data.append({
                        'rank': rank,
                        'title': title,
                        'artist': artist,
                        'last_week': last_week,
                        'weeks_on_chart': charts_in,
                        'score': score,
                        'date_published': date_published,
                        'scraped_date': datetime.now().strftime('%Y-%m-%d')
                    })
                except Exception as e:
                    print(f"處理行時發生錯誤: {str(e)}")
                    continue
        
        if not chart_data:
            raise Exception("沒有爬取到任何數據")
        
        # 輸出JSON
        with open('static.json', 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, ensure_ascii=False, indent=2)
        
        print(f"成功爬取 {len(chart_data)} 條數據並保存為 static.json")
        
    except Exception as e:
        print(f"爬取過程中發生錯誤: {str(e)}")

# 執行爬蟲
scrape_billboard_japan_hot100()
