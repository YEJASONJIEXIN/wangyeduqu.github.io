import urllib.request
import re
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

url='http://daily.zhihu.com/'#知乎日报的地址
 
 
def getHtml(url):#获取主页
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36'}#每台计算机到模拟登录不一样，具体知浏览器寻找
    myrequest = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(myrequest)#用地址创建一个对象
    text = response.read()#打开网址
    return text
 
 
def getUrls(html):#解析每条日报到链接
    html=html.decode('utf-8')
    pattern = re.compile('<a href="/story/(.*?)"', re.S)#使用正则编译
    items = re.findall(pattern, html)#获取每篇文章地址到末尾，末尾7位数字的地址编码是唯一的
    urls=[]
    for item in items:
        urls.append('http://daily.zhihu.com/story/'+item)
 
    return urls
 
 
def getContent(url):#获取日报文章内容
    html = getHtml(url)
    html = html.decode('utf-8')
    patten = re.compile('<h1 class="headline-title">(.*?)</h1>')
    items = re.findall(patten, html)#获取文章标题
    print('*********'+items[0]+'*******')#***号是为了区分文章标题和文章内容
    speaker.Speak(items[0])
    pattern2 = re.compile('<div class="content">\\n<p>(.*?)</div>',re.S)
    items_withtag = re.findall(pattern2, html)#获取文章内容
    for items2 in items_withtag:
        for content in characterProcessing(items2):#对文章内容进行清洗
            print(content)
            speaker.Speak(content)
 
def characterProcessing(html):#去除文章链接多余到文字和乱码，即对文章内容进行清洗
    pattern = re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?', re.S)
    items3 = re.findall(pattern,html)
    result = []
    for index in items3:
        if index != '':
            for content in index:
                tag = re.search('<.*?>', content)
                http = re.search('<.*?http.*?',content)
                html_tag = re.search('&',content)
                if html_tag:
                    content = html.unescape()
                if http:
                    continue
                elif tag:
                    pattern = re.compile('(.*?)<.*?>(.*?)</.*?>(.*?)')
                    items4 = re.findall(pattern, content)
                    content_tags = ''
                    if len(items4) > 0:
                        for item in items4:
                            if len(item) > 0:
                                for item_s in item:
                                    content_tags = content_tags + item_s
                            else:
                                content_tags = content_tags + items4
                        content_tags = re.sub('<.*?>','',content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result
 
 
#运行函数
html = getHtml(url)
urls = getUrls(html)
for url in urls:#遍历每篇文章到地址
    try:
        getContent(url)#获取打印文章到内容
    except Exception as e:
        print('异常')
 

