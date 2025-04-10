import requests
import json
import time
from urllib.parse import quote
from opencc import OpenCC
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BangumiSearcher:
    def __init__(self):
        self.cc = OpenCC('t2s')
        self.session = self._create_session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'
        }

    def _create_session(self) -> requests.Session:
        """创建带有重试策略的Session"""
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def clean_title(self, title: str) -> str:
        """清理和转换标题"""
        return self.cc.convert(title.split('（')[0].split(')')[0].strip())

    def search_bangumi(self, title: str, bgm_token: str) -> Dict[str, Any]:
        """搜索番剧信息"""
        try:
            clean_title = self.clean_title(title)
            encoded_title = quote(clean_title)
            
            response = self.session.get(
                f'https://api.bgm.tv/search/subject/{encoded_title}?type=2&responseGroup=small&max_results=1',
                headers={
            'User-Agent': 'Bilibili2Bangumi/1.0 (https://github.com/hutaodd/Bilibili2Bangumi)',
            'Authorization': f'Bearer {bgm_token}'
        },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败 [{title}]: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"处理出错 [{title}]: {str(e)}")
            return {}

    def process_file(self, input_file: str, output_file: str, bgm_token: str) -> None:
        """处理单个文件"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            successful_ids = []
            
            for title in data['titles']:
                result = self.search_bangumi(title, bgm_token)
                if result.get('list'):
                    item = result['list'][0]
                    if item.get('id'):
                        successful_ids.append(item['id'])
                    logger.info(f"成功获取: {item.get('name_cn', 'N/A')} (ID: {item.get('id', 'N/A')})")
                
                time.sleep(0.5)
            
            self.save_results(output_file, successful_ids)
            
        except Exception as e:
            logger.error(f"处理文件 {input_file} 出错: {str(e)}")

    def save_results(self, output_file: str, ids: List[int]) -> None:
        """保存结果到文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'count': len(ids),
                'ids': ids
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"结果已保存到 {output_file}, 共 {len(ids)} 个ID")


def main(bgm_token: str):
    searcher = BangumiSearcher()
    file_mappings = [
        ('bangumi_s1_list.json', 'ids_1.json'),
        ('bangumi_s2_list.json', 'ids_3.json'), 
        ('bangumi_s3_list.json', 'ids_2.json')
    ]
    
    for input_file, output_file in file_mappings:
        searcher.process_file(input_file, output_file, bgm_token)

if __name__ == "__main__":
    main()