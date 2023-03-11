# 账号密码登录地址：https://stu.ityxb.com/back/bxg_anon/login
# 对应参数列表：
# automaticLogon: false
# username: 15188753131
# password: fyy030306
import os

import requests
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

def getCookieStr():
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
    bookId_list=rsp3['resultObject']['items']
    for item in bookId_list:
        bookId=item['id']
        bookTitle=item['name']
        bookPhoto=f"![image]({item['photo']})"
        print("书籍：《"+bookTitle+"》添加成功")


if __name__ == '__main__':
    setp_1()
    getBookId()