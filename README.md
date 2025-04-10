# Bilibili2Bangumi

一个将B站追番列表同步到Bangumi的工具

## 功能

* 获取B站追番列表
* 自动搜索匹配Bangumi条目
* 批量添加到Bangumi收藏

## 安装

1. 确保已安装Python 3.8+
2. 克隆本项目
3. 安装依赖：

```bash
pip install requests tqdm opencc
```

## 使用方法

1. 修改`main.py`​中的配置：

    * ​`vmid`​: 你的B站用户ID
    * ​`cookie`​: 你的B站登录cookie
    * ​`bgm_token`​: 你的Bangumi API token
2. 运行程序：

```bash
python main.py
```

3. 程序会分三步执行：

    * 获取B站追番列表
    * 搜索匹配Bangumi条目
    * 添加到Bangumi收藏

## 注意事项

* 请妥善保管你的cookie和token
* 程序会自动添加延迟避免请求过快
* 如果遇到问题，请检查网络连接和API权限

## 依赖

* requests
* tqdm
* opencc

## 从b站获取追番列表

### api

https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=2&pn=9&ps=15&vmid=id

#### 参数

* follow_status=[1:想看,2:在看,3:看过]
* pn=[查询的页数]
* ps=[每页查询的个数]
* vmid=[b站个人主页的id]
* cookie b站获取

#### 响应

```js
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "list": [
      {
        "season_id": 48852,
        "media_id": 23154901,
        "season_type": 1,
        "season_type_name": "番剧",
        "title": "关于我转生变成史莱姆这档事 第三季",
        "cover": "https://i0.hdslb.com/bfs/bangumi/image/9c716a761afd055e6b65c96aac7880d2a960dd0b.png",
        "total_count": 24,
        "is_finish": 1,
        "is_started": 1,
        "is_play": 1,
        "badge": "大会员",
        "badge_type": 0,
        "rights": {
          "allow_review": 1,
          "allow_preview": 1,
          "is_selection": 1,
          "selection_style": 1,
          "demand_end_time": {.......
```

## 数据清洗

​`[item["title"] for item in data["data"]["list"]]`​

获取title值,存在三个json中如下格式

```js
{
  "vmid": "88502018",
  "follow_status": 1,
  "titles": [
    "滿腦都是○○的我沒辦法談戀愛（僅限台灣地區）",
    "白箱（僅限港澳台地區）",
    "自稱賢者弟子的賢者（僅限港澳台地區）",
    "異世界迷宮裡的後宮生活（僅限港澳台地區）"
  ]
}
```

## 获取番剧对应bangumi番剧id

```bash
curl -X 'GET' \
  'https://api.bgm.tv/search/subject/番剧名?type=2&responseGroup=small&max_results=1' \
  -H 'accept: application/json'
```

## 添加番剧到bangumi

```js
curl -X 'POST' \
  'https://api.bgm.tv/v0/users/-/collections/[id]' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer [Access Token]' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": 3
}'
```

### 参数

* Access Token   bangumi的Access Token详情见https://bangumi.github.io/api/#/

* id   番剧的id
* "type"  `1:想看, 2:看过, 3:在看,`​

‍

‍

‍

‍

‍
