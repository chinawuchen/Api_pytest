import pytest
import json
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Util.codition_data import LinkedData
from Util.handle_result import ResponseCheck
from Util.handle_cookie import get_cookie_value
from Util.handle_header import get_header, write_header
from Util.handle_excel import HandExcel
from Base.base_request import BaseRequest
from Log.log import initLogging
from Config.config import HandleInit


"""主程序，用来加载和运行测试用例，执行断言，打印日志等操作"""

# 实例化，全局使用
excel_data = HandExcel()
request = BaseRequest()
assertion = ResponseCheck()
linked_data = LinkedData()
hi = HandleInit()
# 获取excel表格的全部测试数据,list
data = excel_data.get_excel_data()[0:-1]
# data = data[0:-1]
# log地址
log_file = base_path + "/Log/log.txt"


class TestRunCaseDdt(object):

    @classmethod
    def setup_class(cls):
        # 每次执行用例之前清空一次日志
        with open(log_file, 'w') as f:
            f.seek(0, 0)  # 把文件定位到0;truncate也是从这里开始删除
            f.truncate()

    @pytest.mark.parametrize("data", data)
    def test_main_case(self, data):
        res = None
        cookie = None
        get_cookie = None
        header = None
        depend_data = None
        try:
            is_run = data[int(hi.get_value("run","constant"))]  # 获取是否执行
            # 根据is_run判断该条用例是否执行
            if is_run == 'yes':
                is_depend = data[int(hi.get_value("preconditions","constant"))]  # 获取依赖的前置条件
                request_data = json.loads(
                    data[int(hi.get_value("data","constant"))])  # 获取请求参数,放在获取依赖数据之前
                # 获取依赖数据，关联
                if is_depend:
                    depend_key = data[int(hi.get_value("rely_id","constant"))]  # 获取依赖key
                    depend_data = linked_data.get_data(is_depend)
                    request_data[depend_key] = depend_data
                case_id = data[int(hi.get_value("case_id","constant"))]
                i = excel_data.get_rows_number(case_id)  # 根据case_id获取行号，从1开始
                url = data[int(hi.get_value("url","constant"))]  # 获取请求地址
                method = data[int(hi.get_value("method","constant"))]  # 获取请求类型get or post
                cookie_method = data[int(hi.get_value("cookie","constant"))]  # 获取cookie操作
                is_header = data[int(hi.get_value("header","constant"))]  # 获取header操作
                # 获取预期结果方式
                excepect_method = data[int(hi.get_value("excepect_method","constant"))]
                # 获取预期结果数据
                excepect_result = data[int(hi.get_value("excepect_result","constant"))]

                # 保存和读取cookie(先放这，暂时不用)
                if cookie_method == 'yes':
                    cookie = get_cookie_value('web')
                if cookie_method == 'write':
                    get_cookie = {"is_cookie": "web"}

                # 保存和读取header(主要是操作token), 并执行接口
                if is_header == "write_header":  # 替换成最新的token
                    res = request.run_main(
                        method, url, request_data, cookie, get_cookie)
                    write_header(res)
                elif is_header == "chinese":  # 获取中文的header
                    header = get_header(is_header)
                    res = request.run_main(
                        method, url, request_data, cookie, get_cookie, header)
                elif is_header == "english":  # 获取英文的header
                    header = get_header(is_header)
                    res = request.run_main(
                        method, url, request_data, cookie, get_cookie, header)
                else:  # 不传header
                    res = request.run_main(
                        method, url, request_data, cookie, get_cookie)

                # 获取响应中的code和msg 的值
                code = str(res["code"])  # 如果响应没有msg，把code放try里，导致我没拿到code，艹
                try:
                    msg = res["msg"]
                except Exception:  # 保证msg没拿到值时程序不报错并继续执行
                    # code = None
                    msg = None

                ''' 对响应结果进行数据校验，暂时写了5种断言方式 '''
                # 1.判断字符串excepect_result是否在响应里面
                if excepect_method == "in_res":
                    result = assertion.is_contain(
                        excepect_result, json.dumps(res, ensure_ascii=False))
                    try:
                        assert result
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "通过")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                    except Exception as e:
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "失败")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            li = i - 1
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % li)
                            f.write("预期结果:%s\n  实际结果:%s\n" %
                                    (excepect_result, res))
                        raise e
                    
                # 2.通过"mec"断言，同时匹配code和msg
                if excepect_method == "mec":
                    config_msg = assertion.handle_result(url, code)
                    try:
                        assert msg == config_msg
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "通过")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                    except Exception as e:
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "失败")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            li = i - 1
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % li)
                            f.write("预期结果:%s\n  实际结果:%s\n" % (config_msg, msg))
                        raise e
                    
                # 3.通过"errorcode"断言，匹配code
                if excepect_method == "errorcode":
                    # 这里拿到的excepect_result, code都是字符串
                    try:
                        assert excepect_result == code
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "通过")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                    except Exception as e:
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "失败")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            li = i - 1
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % li)
                            f.write("预期结果:%s\n  实际结果:%s\n" %
                                    (excepect_result, code))
                        raise e

                # 4.通过json数据格式断言
                if excepect_method == "json":
                    # code = int(code) # 这里拿到的code是字符串，我把状态码写成字符串
                    if code == "0":
                        status_str = 'sucess'
                    elif code == "99999":
                        status_str = 'error'
                    else:
                        status_str = 'shaocan'
                    excepect_result = assertion.get_result_json(
                        url, status_str)
                    result = assertion.handle_result_json(res, excepect_result)
                    try:
                        assert result
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "通过")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                    except Exception as e:
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "失败")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            li = i - 1
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % li)
                            f.write("预期结果:%s\n  实际结果:%s\n" %
                                    (excepect_result, res))
                        raise e
                    
                # 5.通过jsonpath解析断言
                if excepect_method == "jsonpath":
                    result = assertion.handle_result_jsonpath(
                        res, excepect_result)
                    try:
                        assert result
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "通过")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                    except Exception as e:
                        excel_data.excel_write_data(
                            i, int(hi.get_value("result","constant")), "失败")
                        excel_data.excel_write_data(i, int(hi.get_value("response_data","constant")),
                                                    json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            li = i - 1
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % li)
                            f.write("预期结果:%s\n  实际结果:%s\n" %
                                    (excepect_result, res))
                        raise e
                    
        except Exception as e:
            excel_data.excel_write_data(i, int(hi.get_value("result","constant")), "失败")
            with open(log_file, 'a', encoding='utf-8') as f:
                li = i - 1
                f.write("\n第%s条用例报错:\n" % li)
            initLogging(log_file, e)
            raise e


if __name__ == "__main__":
    pytest.main(['-s'])
