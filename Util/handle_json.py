import json
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)


"""用来读取和保存json文件方法"""


# 加载获取json文件数据
def read_json(file_name=None):
    if file_name == None:
        file_path = base_path + "/Data/user_data.json"
    else:
        file_path = base_path + file_name
    with open(file_path, encoding='UTF-8') as f:
        data = json.load(f)
    return data


# 通过key获取value
def get_value(key, file_name=None):
    data = read_json(file_name)
    return data.get(key)


# 往json文件中写入数据，如果不传文件路径，默认是写入cookie的文件路径
def write_value(data, file_name=None):
    data_value = json.dumps(data)
    if file_name == None:
        path = base_path + "/Data/cookie.json"
    else:
        path = base_path + file_name
    with open(path, 'w') as f:
        f.write(data_value)


if __name__ == "__main__":
    # print(read_json())
    print(get_value("front/member/login"))
