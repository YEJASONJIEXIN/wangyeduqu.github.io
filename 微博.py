# 爬取今日头条的微博
import requests
from pyquery import PyQuery as pq
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

url = 'https://m.weibo.cn/api/container/getIndex?containerid=2304131618051664_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03'  #


def getJSON(page):
    hd = {'User-Agent': 'Mozilla'}  # 模拟浏览器进行访问
    params = {'page': page}
    try:
        r = requests.get(url, headers=hd, params=params)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.json())  # 返回json对象
        return r.json()
    except:
        print('------')


def parsePage(json):
    if json:
        items = json.get('data').get("cards")  # 由Network,XHR中检查到是一个列表类型，返回一个列表
        for item in items:  # 每一个item又是一个字典
            item = item.get('mblog')  # 字典类型
            if item == None:
                continue
            content = {}  # 创建一个字典
            content['时间'] = item.get('created_at')
            content['内容'] = pq(item.get('text')).text()  # 利用pyquery将正文中的HTML标签去掉
            content['发布设备'] = item.get('source')
            content['获赞数'] = item.get('attitudes_count')
            content['评论数'] = item.get('comments_count')
            yield content  # yield关键字，表明这个函数是一个generator，直接使用for循环来迭代


def main():
    print('请输入你想读取的页码:')
    i = input()  # 爬取第i页的内容
    r = getJSON(i)
    results = parsePage(r)
    for result in results:
        print(result)
        speaker.Speak(result)


main()
