import os

import requests
import execjs
from lxml import etree
import pymysql
# https://stu.ityxb.com/back/bxg/preview/info?previewId=c01f217bf7744f42b406e6a77c426ef9&t=1677669954513
# 课程进入url：请求 URL: https://stu.ityxb.com/back/bxg/preview/list?name=&isEnd=&pageNumber=1&pageSize=10&type=1&courseId=f21b9584488441c58cfcfa2b986ad205&t=1677670760570
def sign_in(uname,password):
    sign_in_url = "https://stu.ityxb.com/back/bxg_anon/login"
    sign_in_data = {
        "automaticLogon": "false",
        "username": uname,
        "password": password
                    }
    sign_in_headers = {
        "content-length": "60",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://stu.ityxb.com",
        "referer": "https://stu.ityxb.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    sign_in_rsp = requests.post(url=sign_in_url, data=sign_in_data, headers=sign_in_headers)
    return sign_in_rsp

def step_1():
    sign_sus = False
    while sign_sus == False:
        # 如果密码错误，清屏重新开始输入账号密码
        os.system("cls")
        username = input("请输入你的手机号：")
        password = input("请输入你的密码：")
        sign_in_rsp = sign_in(username, password)
        sign_in_json = sign_in_rsp.json()
        # print(sign_in_json)
        if sign_in_json['success'] == False:
            print(sign_in_json.get('errorMessage'), ",请按回车重新输入账号密码！")
        else:
            sign_sus = True
            print("恭喜你登陆成功！")
    # 整合cookie 全局通用
    global cookieStr,global_headers
    cookieStr = ''
    for item in sign_in_rsp.cookies:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'
    global_headers = {
        'Cookie': cookieStr,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    print(cookieStr)

def getBookId():
    url="https://stu.ityxb.com/back/bxg/course/getHaveList"
    data={
        "type": 1,
        "pageNumber": 1,
        "pageSize": 100
    }
    rsp3=requests.post(url=url,headers=global_headers,data=data).json()
    # print(rsp3)
    # print("https://stu.ityxb.com/learning/"+rsp3['resultObject']['items'][0]['id'])
    # 如果链接存在
    # if rsp3.status_code==200:
        # rsp_json=rsp3.json()
    os.system("cls")
    print("处理成功！你当前已经开启的课程如下:\n")
        # i=0
        #存课程的字典
        # global course_dict
        # course_dict={}
    bookId_list=rsp3['resultObject']['items']
    for item in bookId_list:
            bookId=item['id']
            bookTitle=item['name']
            bookPhoto=f"![image]({item['photo']})"
            #这里是导入数据库信息
            # sql = f"insert into itheima(video_url,title) values('{bookTitle}','{bookPhoto}')"
            # ret = add(sql)
            # i+=1
            print("书籍：《"+bookTitle+"》添加成功")
            # course_dict[i]=[bookTitle,bookId]
            getUrl(bookId)
        # print("添加所有课程信息数据成功！")
    # else:
    #     print("请与作者Q3300519161，联系!")
#
# def step_2():
#     print("您所加入课程如下:")
#     for i in range(len(course_dict)):
#         print("%")
#         pass
def getUrl(id):
    url=f"https://stu.ityxb.com/back/bxg/preview/list?name=&isEnd=&pageNumber=1&pageSize=1000&type=1&courseId={id}"
    rsp2=requests.get(url=url,headers=global_headers).json()
    classId_list=rsp2['resultObject']['items']
    for item in classId_list:
        url="https://stu.ityxb.com/back/bxg/preview/info?previewId="+item['id']
        video(url)

def video(url):
    rsp=requests.get(url,headers=global_headers).json()
    # print(rsp['resultObject']['chapters'][0]['points'][0]['video_url'])
    chapters1_list=rsp['resultObject']['chapters']
    for item2 in chapters1_list:
        chapter_list=item2['points']
        chapter_name=item2['chapter']['point_name']
        chapter_is=item2['chapter']['is_chapter']
        sql = f"insert into itheima(video_url,title) values('{chapter_name}','{chapter_is}')"
        ret = add(sql)
        print(chapter_name)
        for item in chapter_list:
            video_url=item['video_url']
            title=item['point_name']
            print(item['video_url'],item['point_name'])
            # sql = f"insert into itheima(video_url,title) values('{video_url}','{title}')"
            # ret = add(sql
            print("第" + str(ret) + "条数据添加成功！")
            # skip_video()

def skip_video():
    ctx = execjs.compile("""
        function skip() {
        const video = document.getElementsByTagName('video')[0]
        if (video != null) {
            video.play()
            video.currentTime = video.duration-1
        } 
    }
    """)
    ctx.call("skip")

def change(sql,isInsert=False):
    try:
        conn = pymysql.connect(
            user="root",  # The first four arguments is based on DB-API 2.0 recommendation.
            password="root",
            host="localhost",
            database="spider",
            port=3306,
        )
        cursor = conn.cursor()
        count=cursor.execute(sql)
        conn.commit()
        # 新增的数据的id值
        if isInsert:
            new_id = cursor.lastrowid
            return new_id
        else:
            return count
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def add(sql):
    return change(sql,isInsert=True)

def upd(sql):
    return change(sql)

def delete(sql):
   return change(sql)

if __name__ == '__main__':
    # video()
    # getUrl()
    step_1()
    getBookId()