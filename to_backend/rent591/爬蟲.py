import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode



class WebSpider:
    def __init__(self, base_url, pattern, headers=None):
        """初始化 session、headers、目標網址和正則表達式"""
        self.session = requests.Session()
        self.base_url = base_url
        self.pattern = re.compile(pattern)
        self.headers = headers or {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

    def get_all_ids(self, url) -> set[str]:
        """根據給定的 URL 抓取並解析頁面資料"""
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return set()

        soup = BeautifulSoup(response.text, 'html.parser')
        ids = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if match := self.pattern.search(href):
                item_id = match.group(1)
                ids.add(item_id)
        return ids

    def search(self, filter_params=None, sort_params=None):
        """根據篩選和排序條件生成搜尋網址並取得資料"""
        params = filter_params or {}
        if sort_params:
            params.update(sort_params)

        search_url = f"{self.base_url}?{urlencode(params)}"
        print(f"Requesting: {search_url}")
        return self.get_all_ids(search_url)

    def send_telegram(self, ids, url_template, token, chat_id):
        """發送結果至 Telegram"""
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        text = "\n".join([url_template.format(i) for i in ids])
        payload = {
            "chat_id": chat_id,
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