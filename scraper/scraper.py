import requests
from bs4 import BeautifulSoup
import time
import logging
import random

class Scraper:
    def __init__(self, base_url):
        """初始化爬虫
     
        Args:
            base_url: 目标网站的基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_page(self, url, retry_times=3):
        """获取页面内容
        
        Args:
            url: 目标页面URL
            retry_times: 重试次数
            
        Returns:
            BeautifulSoup对象
        """
        for i in range(retry_times):
            try:
                response = self.session.get(
                    url, 
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                self.logger.error(f"获取页面失败: {str(e)}")
                if i == retry_times - 1:
                    raise
                time.sleep(random.randint(1, 3))

    def parse_page(self, soup):
        """解析页面内容
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            str: 页面的原生HTML内容
        """
        return str(soup)

    def save_data(self, data):
        """保存数据
        
        Args:
            data: 要保存的数据
        """
        raise NotImplementedError("请在子类中实现此方法")

    def run(self):
        """运行爬虫"""
        try:
            print("starting get page")
            soup = self.get_page(self.base_url)
            print("starting parse page")
            data = self.parse_page(soup)
            print("starting save data")
            # self.save_data(data)
            self.logger.info("爬取完成")
        except Exception as e:
            self.logger.error(f"爬虫运行失败: {str(e)}")

if __name__ == '__main__':
    url = "https://liaoxuefeng.com/books/python/first-program/index.html"
    scraper = Scraper(url)
    try:
        scraper.run()
    except Exception as e:
        print(f"爬虫运行出错: {e}")

