import requests
from bs4 import BeautifulSoup
import time
import logging
import random
import json
from concurrent.futures import ThreadPoolExecutor


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
            soup = self.get_page(self.base_url)
            data = self.parse_page(soup)
        except Exception as e:
            self.logger.error(f"爬虫运行失败: {str(e)}")
        return data


def crawl_chapter(url):
    try:
        # 构造完整URL
        full_url = f"https://liaoxuefeng.com{url}"
        print(f"正在爬取: {full_url}")
        
        # 获取页面内容
        response = requests.get(full_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取章节内容区域
        content_div = soup.find('div', id='gsi-chapter-content')
        title_div = soup.find('div', id='gsi-chapter-title')
        if content_div:
            # 提取标题
            title = title_div.find('h1').get_text().strip()
            # 提取所有段落文本
            paragraphs = content_div.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            # 使用锁同步写入
            chapter_contents.append({
                'url': full_url,
                'title': title,
                'content': content
            })
        else:
            print(f"在 {full_url} 中未找到内容区域")
            
    except Exception as e:
        print(f"爬取 {url} 时出错: {str(e)}")

if __name__ == '__main__':
    # 爬取廖雪峰的Python教程主界面
    url = "https://liaoxuefeng.com/books/python/introduction/index.html"
    scraper = Scraper(url)
    try:
        data = scraper.run()
    except Exception as e:
        print(f"爬虫运行出错: {e}")

    # 解析HTML内容
    soup = BeautifulSoup(data, 'html.parser')
    
    # 获取目录区域
    index_div = soup.find('div', id='gsi-index')
    if index_div:
        # 获取所有章节项
        items = index_div.find_all('div', class_='gsc-index-item gsc-index-item-closed')
        
        # 提取每个章节的链接
        urls = []
        for item in items:
            link = item.find('a')
            if link and 'href' in link.attrs:
                urls.append(link['href'])
    
    else:
        print("未找到目录区域")

    # 遍历所有章节链接并爬取内容
    chapter_contents = []


    # 只爬取5-44个章节
    urls = urls[5:44]
    
    # 使用线程池并发爬取
    with ThreadPoolExecutor() as executor:
        executor.map(crawl_chapter, urls)
    
    # 将内容保存到文件
    with open('data/python_tutorial_contents_liaoxuefeng_5-44_chapter.json', 'w', encoding='utf-8') as f:
        json.dump(chapter_contents, f, ensure_ascii=False, indent=2)
    
    print(f"成功爬取 {len(chapter_contents)} 个章节的内容")

