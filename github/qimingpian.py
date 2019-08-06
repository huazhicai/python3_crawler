# import requests

import json
import execjs
import base64

# res = requests.get('https://vipapi.qimingpian.com/DataList/productListVip')
with open('qimingpian.html', 'r') as f:
    res_json = f.read()
content = json.loads(res_json)
content_list = execjs.compile(open("qimingpian.js").read()).call('decrypt', content['encrypt_data'])
# content_list = base64.b64decode(content_list)
content = json.loads(content_list)
print(content)
