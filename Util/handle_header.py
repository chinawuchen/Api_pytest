import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Util.handle_json import read_json, get_value, write_value


"""用来读取和保存headaer(token)的方法"""


# 获取headaer
def get_header(headaer_key=None):
    if headaer_key == None:
        data = get_value("chinese", "/Data/header.json")
    else:
        data = get_value(headaer_key, "/Data/header.json")
    return data


# 写入headaer(token)
def write_header(header_value):
    hv = header_value["data"]["accessToken"]
    header = read_json("/Data/header.json")
    for i in header.items():
        i[1]['token'] = hv
    write_value(header, "/Data/header.json")


if __name__ == "__main__":
    data = {"data": {"accessToken": "a_1dbd0b61e4da658e62af373d68acdcee", "info": {"id": 27466,
                                                                                   "login_time": "1681372756", "balance": "1222.45", "user_email": ""}}, "code": 0, "result": 111}
    print(get_header())
    write_header(data)
