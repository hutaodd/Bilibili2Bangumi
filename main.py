import collection_bangumi
import search_bangumi
import get_bangumi_list
import time
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 用户配置区域
CONFIG = {
    'vmid': "",
    'cookie': "",
    'bgm_token': ""
}

# 主函数
def main(vmid: str, cookie: str, bgm_token: str):
    print("=== 开始同步B站追番到Bangumi ===")
    
    # 初始化总进度条
    with tqdm(total=100, desc="总体进度") as pbar_total:
        with ThreadPoolExecutor(max_workers=3) as executor:
            # 获取B站追番列表
            print("\n[1/3] 正在获取B站追番列表...")
            future_get = executor.submit(get_bangumi_list.run, vmid, cookie)
            future_get.result()
            pbar_total.update(33)
            print("✓ 获取B站追番列表完成")
            
            # 搜索Bangumi信息
            print("\n[2/3] 正在搜索Bangumi信息...")
            future_search = executor.submit(search_bangumi.main, bgm_token)
            future_search.result()
            pbar_total.update(33)
            print("✓ 搜索Bangumi信息完成")
            
            # 添加到Bangumi收藏
            print("\n[3/3] 正在添加到Bangumi收藏...")
            futures = [
                executor.submit(collection_bangumi.run, 'ids_1.json', 1, bgm_token),
                executor.submit(collection_bangumi.run, 'ids_2.json', 2, bgm_token),
                executor.submit(collection_bangumi.run, 'ids_3.json', 3, bgm_token)
            ]
            
            # 添加收藏进度条
            with tqdm(total=len(futures), desc="收藏进度") as pbar_collect:
                for future in as_completed(futures):
                    future.result()
                    pbar_collect.update(1)
                    pbar_total.update(34/len(futures))
            
            print("✓ 添加到Bangumi收藏完成")
    
    print("\n=== 同步完成 ===")

if __name__ == "__main__":
    # 使用配置文件中的参数
    main(CONFIG['vmid'], CONFIG['cookie'], CONFIG['bgm_token'])