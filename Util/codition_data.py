import json
import sys
import os
from jsonpath_rw import parse

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Util.handle_excel import HandExcel
from Config.config import HandleInit


"""用来处理数据依赖，关联的数据"""


class LinkedData(object):

    # 拆分单元格数据
    def split_data(self, data):
        case_id = data.split(">")[0]
        rule_data = data.split(">")[1]
        return case_id, rule_data

    # 获取依赖结果集
    def depend_data(self, data):
        excel_data = HandExcel()
        hi = HandleInit()
        case_id = self.split_data(data)[0]
        row_number = excel_data.get_rows_number(case_id)
        data = excel_data.get_cell_value(row_number, int(hi.get_value('response_data', 'constant')))
        # data = excel_data.get_cell_value(row_number, 14)
        return data

    # 获取依赖字段
    def get_depend_data(self, res_data, key):
        res_data = json.loads(res_data)
        json_exe = parse(key)
        madle = json_exe.find(res_data)
        # print(madle)
        return [math.value for math in madle][0]

    # 获取依赖数据
    def get_data(self, data):
        res_data = self.depend_data(data)
        rule_data = self.split_data(data)[1]
        return self.get_depend_data(res_data, rule_data)


if __name__ == "__main__":
    run = LinkedData()
    data = 'Hub_0001>data.info.login_time'
    print(run.get_data(data))
