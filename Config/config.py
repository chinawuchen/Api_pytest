import configparser
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

"""该模块用来读取配置文件的数据"""


class HandleInit(object):

    # 加载配置文件
    def load_ini(self):
        file_path = base_path + "/Config/config.ini"
        cf = configparser.ConfigParser()
        cf.read(file_path, encoding="utf-8-sig")
        return cf

    # 获取配置文件里面的value
    def get_value(self, key, node=None):
        if node == None:
            node = "server"
        cf = self.load_ini()
        try:
            data = cf.get(node, key)
        except Exception:
            print("没有获取到值")
            data = None
        return data


if __name__ == "__main__":
    hi = HandleInit()
    # xml_report_path = base_path + hi.get_value("xml_report_path","path")
    # print(xml_report_path)
    # print(hi.load_ini())
    print(hi.get_value("hub_host_Online"))