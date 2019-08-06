import os

import requests
from lxml import etree
import execjs


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'http://www.114yygh.com/index.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.114yygh'
        }
        self.login_url = 'http://www.114yygh.com/account/loginStep1.htm'
        self.post_url = 'http://www.114yygh.com/account/loginStep2.htm'
        self.session = requests.Session()

    def token(self):
        post_data = {
            'mobileNo': 18701943997
        }
        response = self.session.post(self.login_url, headers=self.headers, data=post_data)
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="loginStep2_pwd_form"]/input')
        return token

    def password(self):
        """
        密码js加密
        :return:
        """
        with open('sha1.js', encoding='utf8') as f:
            strs = f.read()
        ctx = execjs.compile(strs).call('hex_sha1', os.getenv('PASSWORD'))
        return ctx

    def login(self):
        resp = self.token()
        post_data = {
            'token': resp[0],
            'mobileNo': resp[1],
            'smsType': resp[2],
            'loginType': resp[3],
            'password': self.password()
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print(response.text)


if __name__ == '__main__':
    login = Login()
    login.login()