import requests


def login(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response


if __name__ == '__main__':
    url = 'http://chinackd.medidata.cn/doLoginAction?Action=doLogin&LoginIdPwd=3428df578ef3a18447b0c987507190ab1a00e36c2b58f209a1dd4fe208e28ea9ed001e06e55b2925a7775cba8744c961c8eec9c569b4d95d4813ff79f9be357d90e847f4b4f797e73219258e9cc6bd31605f7e8c3245f92eab62f21df6190f233d4f89913e690386e894b3cecb07f7e6fab36ff353079f4723efa48c8ceffd4c&loginType=1&LangID=zh_CN&_=1569553020936'
    resp = login(url)
    print(resp.headers)
    print(resp.text)