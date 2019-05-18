#-*- coding: UTF-8 -*- 
import requests
import sys
from bs4 import BeautifulSoup
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

#获取网页body里的内容
def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }

    req = requests.get(url, headers=header)
    req.encoding = 'utf-8'
    bs = BeautifulSoup(req.text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    return body

#获取问题标题
def get_title(html_text):
    data = html_text.find('h1', {'class':'QuestionHeader-title'})  #匹配标签
    print (type(data))
    return data.string.encode('utf-8')

#获取问题内容
def get_question_content(html_text):
    data = html_text.find('span', {'class': 'RichText ztext'})
    print (data.string)
    if data.string is None:
        out = '';
        for datastring in data.strings:
            datastring = datastring.encode('utf-8')
            out = out + datastring.encode('utf-8')
        print ('内容：\n' + out)
    else:
        print ('内容：\n' + data.string.encode('utf-8'))

#获取点赞数
def get_answer_agree(body):
    agree = body.find('button',{'class': 'Button Button--plain'})
    print ('点赞数：' + agree.string.encode('utf-8') + '\n')

#获取答案
def get_response(html_text):
    out1 = ''
    response = html_text.find_all('div', {'class': 'ContentItem-time'})
    for index in range(len(response)):
        #获取标签
        answerhref = response[index].find('a', {'target': '_blank'})
        if not(answerhref['href'].startswith('javascript')):
            url = 'http://www.zhihu.com' + answerhref['href']
            body = get_content(url)
#            get_answer_agree(body)
            answer = body.find('span', {'class': 'RichText ztext CopyrightRichText-richText'})
            if answer.string is None:
                out = '';
                for datastring in answer.strings:
                    datastring = datastring.encode('utf-8')
                    out = out + '\n' + str(datastring,encoding = 'utf-8')
            else:
                print (answer.string.encode('utf-8'))
        out1 = out1 + '\n' + out
    return url + '\n' +out1

a = 1
while a == 1:
    print('输入所需网址：（成功示例：https://www.zhihu.com/question/324406970/answer/683454231）\n')
    url = input()
    html_text = get_content(url)
    title = get_title(html_text)
    print ("标题：\n" + str(title,encoding = 'utf-8') + '\n')
    speaker.Speak(str(title,encoding = 'utf-8'))
    #questiondata = get_question_content(html_text)
    print ('\n')
    data = get_response(html_text)
    print (data)
    speaker.Speak(data)
    print('=================================')


