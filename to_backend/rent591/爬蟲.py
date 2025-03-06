import time
import random
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class House591Spider:
    def __init__(self):
        """初始化 session 和 headers"""
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

    def get_house_all_ids(self, house_url) -> set[int]:
        """根據給定的 URL 取得網頁內容並解析出房屋 ID  """
        try:
            response = self.session.get(house_url, headers=self.headers)
            response.raise_for_status()  # 如果狀態碼不是 200，則引發異常
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return set()  # 返回空的 set

        soup = BeautifulSoup(response.text, 'html.parser')
        house_ids = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if match := (re.search(r'https://rent\.591\.com\.tw/(\d+)', href) ) :
                house_id = match.group(1)  # 提取數字部分
                house_ids.add(house_id)    # 使用 set 的 add 方法來添加元素
        return house_ids
        
    
    def search(self, filter_params=None, sort_params=None):
        """搜尋房屋，根據篩選條件和排序條件"""
        base_url = 'https://rent.591.com.tw/list?'
        params = filter_params or {'region': '1', 'kind': '0'}  # 預設篩選條件
        if sort_params:
            params.update(sort_params)  # 添加排序條件

        # 使用 urllib.parse 組合查詢參數
        search_url = base_url + urlencode(params)
        print(f"Requesting: {search_url}")

        # 獲取房屋資訊並添加隨機延遲
        house_ids = self.get_house_all_ids(search_url)

        return  house_ids
    
    def sendTele(self,message):
    
        TOKEN = "7860456857:AAEeGAEsSQ1tQuaCjxC4TqkhXs62GCKjsUI"# Telegram Bot Token
        chat_id = "5298494709" # 目標 chat_id 


        # Telegram API URL
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        text= ""
    
        for i in message :
            text+= f"https://rent.591.com.tw/rent-detail-{i}.html\n"
            
        # API 請求參數
        payload = {
            "chat_id": chat_id,
            "text": text
        }

        # 發送請求
        requests.post(url, data=payload)

