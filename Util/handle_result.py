import jsonpath
import sys
import os
from deepdiff import DeepDiff

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Util.codition_data import LinkedData
from Util.handle_json import get_value


"""封装接口响应断言的类"""


class ResponseCheck(object):

    # 判断实际结果 字符串str_one 是否在返回结果 字符串str_two 里面
    def is_contain(self, str_one, str_two):
        flag = None
        if str_one in str_two:
            flag = True
        else:
            flag = False
        return flag

    # mec 断言方法
    def handle_result(self, url, code):
        data = get_value(url, "/Data/code_message.json")
        if data != None:
            for i in data:
                message = i.get(str(code))
                if message:
                    return message
        return None

    # 需要给校验格式方法提供的预期结果(字典)
    def get_result_json(self, url, status):
        data = get_value(url, "/Data/result.json")
        if data != None:
            for i in data:
                message = i.get(status)
                if message:
                    return message
        return None

    # 校验json格式
    def handle_result_json(self, dict1, dict2):
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            cmp_dict = DeepDiff(dict1, dict2, ignore_order=True).to_dict()
            # print(cmp_dict)
            if cmp_dict.get("dictionary_item_added"):
                return False
            else:
                return True
        return False

    #  利用jsonpath解析json，并对响应结果进行数据校验
    def handle_result_jsonpath(self, response, expect_data):
        linked_data = LinkedData()
        flag = None
        json_rule, expect_list = linked_data.split_data(expect_data)
        expect_list = eval(expect_list)  # 从excel里面拿到的expect_list是str，需要转成list
        author_list = jsonpath.jsonpath(response, json_rule)
        if author_list == expect_list:
            flag = True
        else:
            flag = False
        return flag


if __name__ == "__main__":
    run = ResponseCheck()
    data1 = {"id": 12313, 'name': 'dghsa', 'age': 0, 'adds': '嘎环境'}
    data2 = {"id": 31213, 'name': 'dghsa', 'age': 0, 'adds': '2321312'}
    # print(run.handle_result("front/member/register", 99999))
    # print(run.handle_result_json(data1, data2))
    

    print(run.get_result_json('front/member/login', 'error'))
    print(type(run.get_result_json('front/member/login', 'error')))
