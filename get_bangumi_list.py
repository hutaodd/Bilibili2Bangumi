import requests
import json
import time

def get_bangumi_list(vmid, follow_status, pn, ps, headers):
    """
    从B站获取追番列表
    :param vmid: B站用户ID
    :param follow_status: 追番状态(1:想看, 2:在看, 3:看过)
    :param pn: 页码
    :param ps: 每页数量
    :return: 番剧标题列表
    """
    url = "https://api.bilibili.com/x/space/bangumi/follow/list"
    params = {
        "type": 1,
        "follow_status": follow_status,
        "pn": pn,
        "ps": ps,
        "vmid": vmid
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "data" not in data or "list" not in data["data"]:
            return {"titles": []}
        result = {
            "titles": [item["title"] for item in data["data"]["list"]]
        }
        return result
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"获取番剧列表时出错: {e}")
        return {"titles": []}

def run(vmid, cookie):
    """
    获取B站追番列表并保存到文件
    :param vmid: B站用户ID
    :param cookie: B站Cookie
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": cookie
    }
    
    follow_status = 1  # 追番状态(1:想看, 2:在看, 3:看过)
    ps = 30
    pn = 1
    
    while follow_status <= 3:
        pn = 1
        all_titles = []
        while True:
            result = get_bangumi_list(vmid, follow_status, pn, ps, headers)
            if not result["titles"]:
                break
            all_titles.extend(result["titles"])
            pn += 1
            time.sleep(0.5)
        
        # 保存结果到文件
        with open(f'bangumi_s{follow_status}_list.json', 'w', encoding='utf-8') as f:
            json.dump({"titles": all_titles}, f, ensure_ascii=False, indent=2)
        
        follow_status += 1


if __name__ == "__main__":
    # 示例使用
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": "buvid3=DF592008-4669-EA21-2428-7290321450EA21532infoc; b_nut=1739350921; _uuid=5FB5E39C-869B-9C6E-B9CB-A1BB72FFE7DD22005infoc; enable_web_push=DISABLE; buvid4=309652B0-F968-65A5-7BED-C8466B07017222570-025021209-3ekHf0yzWI0Ve5zjd4h7OA%3D%3D; buvid_fp=d1af41f5e3a84fdaf4fdce29384d3c40; DedeUserID=88502018; DedeUserID__ckMd5=96cf3f87a375c77f; header_theme_version=CLOSE; rpdid=|(u)YJlkkm|~0J'u~JmJl|mYJ; SESSDATA=ff73b7e9%2C1756183327%2C08838%2A21CjBD2orndCgKHcCw8obDlXlCN9lbmDkEX9y_ZiH3-RravgTx4rFU_fg-wC5byKRLrIQSVm5USHpUREVkaFpZckIwYzlsS2FZS1R5b2tscVkyN1IwZFoxR3VJazZXNjJPNEZWeElaYVlydVRSU1p4Q0U4VkRsbXFidUtGRlV4UEtaN194XzNpcVpRIIEC; bili_jct=1c7bd3c997273ab28cfdcc3558e41d97; enable_feed_channel=ENABLE; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDQ0NjA0NjMsImlhdCI6MTc0NDIwMTIwMywicGx0IjotMX0.rus_CDHSRvtn3QRDrbHEnQZIy2boLpnGTkNRE_df5fg; bili_ticket_expires=1744460403; CURRENT_FNVAL=4048; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; fingerprint=199666188b652a06099630e7d5d8d5f1; bsource=search_google; home_feed_column=5; browser_resolution=1920-945; theme_style=light; b_lsid=9B372712_1962010B9E0"  # 用户需要在此处填入自己的B站Cookie
    }
    vmid = "88502018"  # 替换为你的B站用户ID
    follow_status = 1  # 追番状态(1:想看, 2:在看, 3:看过)
    ps = 30
    pn = 1
    all_titles = []
    while follow_status <= 3:
        pn = 1
        all_titles = []
        while True:
            result = get_bangumi_list(vmid, follow_status, pn, ps, headers)
            titles = result["titles"]
            if not titles:
                break
            all_titles.extend(titles)
            pn += 1
        # 保存结果到JSON文件
        output_data = {
            "vmid": vmid,
            "follow_status": follow_status,
            "titles": all_titles
        }
        with open(f"bangumi_s{follow_status}_list.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        follow_status += 1