import json
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Util.handle_json import get_value, read_json, write_value


"""用来读取和保存cookie的方法,我们的接口暂时不需要,先写在这里"""


# 获取cookie
def get_cookie_value(cookie_key):
    data = read_json("/Data/cookie.json")
    return data[cookie_key]


# 写入cookie
def write_cookie(cookie_value, cookie_key):
    cookie = read_json("/Data/cookie.json")
    cookie[cookie_key] = cookie_value
    write_value(cookie)


if __name__ == "__main__":
    print(get_cookie_value("web"))
    data = {"bbb": "iiiii"}
    # rite_cookie(data, "app")
