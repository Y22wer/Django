import requests ,time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from typing import List
import concurrent.futures

class WebSpider:
    def __init__(self, base_url, pattern, headers=None):
        """初始化 session、headers、目標網址和正則表達式"""
        self.session = requests.Session()
        self.base_url = base_url
        self.pattern = re.compile(pattern)
        self.headers = headers or {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

    def get_single_page_ids(self, soup) -> List[str]:
        """解析HTML並提取所有房屋 ID"""
        ids = []
        for link in soup.find_all('a', href=True,class_='link v-middle'):
          href = link['href']
          if match := self.pattern.search(href):
            item_id = match.group(1)
            ids.append(item_id)
        print(f"分頁ID {ids}")
        return ids

    def get_all_pages_ids(self, url):
      """解析HTML並提取所有房屋 ID"""
      all_ids = []
      page_urls = self.get_page_links(url)
      
      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
          futures = [executor.submit(self.get_page_ids, page_url) for page_url in page_urls]
          for future in concurrent.futures.as_completed(futures):
            all_ids.extend(future.result())  # 保持 ID 順序
      
      return all_ids
    def get_page_ids(self, page_url):
      """獲取單一頁面的房屋 ID"""
      time.sleep(2)  # 維持禮貌性延遲
      soup = self.getBS4(page_url)
      ids = self.get_single_page_ids(soup)
      return ids
    
    def search(self, filter_params=None, sort_params=None):
        """根據篩選和排序條件生成搜尋網址並取得資料"""
        params = filter_params or {}
        if sort_params:
            params.update(sort_params)

        search_url = f"{self.base_url}?{urlencode(params)}"
        print(f"Requesting: {search_url}")
        return self.get_all_pages_ids(search_url)
    
    def getBS4(self, url):
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup 
    
    def get_page_links(self,  base_url)-> List[str]:
        """解析HTML並提取所有頁碼的href連結"""
        page_links = [base_url]
        soup=self.getBS4(base_url)
        paginator = soup.find('div', class_='paginator-container')  # 找到分頁容器

        if paginator:
            links = paginator.find_all('a', href=True)  # 找到所有href的a標籤
            pa = [link['href'] for link in links if 'page=' in link['href']]
            page_numbers = [re.search(r'page=(\d+)', url).group(1) for url in pa if re.search(r'page=(\d+)', url)]
            max_page = max([int(page) for page in page_numbers])
            if max_page > 1:
              for i in range(2, max_page+1):  # 修正，生成從第 1 頁到最大頁碼的所有 URL
                    page_links.append(f"{base_url}&page={i}")
            else:
              page_links.append(base_url)
        print(f"總共有{len(page_links)}頁")
        return page_links

    def send_telegram(self, ids, url_template, token, chat_id):
        """發送結果至 Telegram"""
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        text = "\n\n".join([url_template.format(i) for i in ids])
        payload = {
            "chat_id": chat_id, #頻道ID
            "text": text
        }
        requests.post(api_url, data=payload)

# ---------------------------------------
# 使用範例：591 房屋爬蟲
class House591Spider(WebSpider):
    def __init__(self):
        super().__init__(
            base_url='https://rent.591.com.tw/list',
            pattern=r'https://rent\.591\.com\.tw/(\d+)'
        )

# 使用範例：求職網站爬蟲 (chickpt)
class JobSpider(WebSpider):
    def __init__(self):
        super().__init__(
            base_url='https://www.chickpt.com.tw/',
            pattern=r'https://www\.chickpt\.com\.tw/job-([a-zA-Z0-9]+)'
        )