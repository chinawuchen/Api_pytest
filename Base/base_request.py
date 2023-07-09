import requests
import json
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Config.config import HandleInit
from Util.handle_cookie import write_cookie

"""封装发送请求的类"""


class BaseRequest(object):

    # 发送post请求
    # verify = False 忽略https认证
    def send_post(self, url, data=None, cookie=None, get_cookie=None, header=None):
        response = requests.post(
            url=url, data=data, cookies=cookie, headers=header)
        if get_cookie != None:
            cookie_value_jar = response.cookies
            cookie_value = requests.utils.dict_from_cookiejar(cookie_value_jar)
            write_cookie(cookie_value, get_cookie['is_cookie'])
        return response

    # 发送get请求
    def send_get(self, url, data=None, cookie=None, get_cookie=None, header=None):
        response = requests.get(url=url, params=data,
                                cookies=cookie, headers=header)
        if get_cookie != None:
            cookie_value_jar = response.cookies
            cookie_value = requests.utils.dict_from_cookiejar(cookie_value_jar)
            write_cookie(cookie_value, get_cookie['is_cookie'])
        return response

    # 执行方法，根据method判读是执行get还是post请求
    def run_main(self, method, url, data=None, cookie=None, get_cookie=None, header=None):
        conf = HandleInit()
        base_url = conf.get_value('hub_host_test')
        if 'http' not in url:
            url = base_url + url
        if method == 'get':
            res = self.send_get(url, data, cookie, get_cookie, header)
        else:
            res = self.send_post(url, data, cookie, get_cookie, header)
        try:
            res = json.loads(res.text)
            # res = res.json()
        except:
            print("这个结果是一个text")
        return res


if __name__ == "__main__":
    request = BaseRequest()

    # url1 = "front/member/login"
    # # header1 = {"lang": "1", "token": "a_040933e972911f54ed163a0a77a35aef"}
    # data1 = {"user_email": "13045899811", "user_pass": "wu123456"}
    # aa = request.run_main("post", url1, data1)
    # print(aa)
    # print(type(aa))

    url1 = "front/member/goods-backpack"
    header1 = {"lang": "1", "token": "a_f3a00af8c2f545933566ea4214e9d503"}
    data1 = {"gtype": "1","page": "1","pageSize": "21"}
    aa = request.run_main("post", url1, data1, header=header1)
    print(aa)
    print(type(aa))