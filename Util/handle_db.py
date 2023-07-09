import pymysql.cursors
import json
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Config.config import HandleInit


"""用来连接和查询数据库的类，现在暂时没用上，后面可能会用上"""


class OperationMysql(object):

    def __init__(self):
        self.handle_ini = HandleInit()
        self.conn = pymysql.connect(
            host=self.handle_ini.get_value("host", "mysql"),
            user=self.handle_ini.get_value("user", "mysql"),
            passwd=self.handle_ini.get_value("passwd", "mysql"),
            db=self.handle_ini.get_value("db", "mysql"),
            port=int(self.handle_ini.get_value("port", "mysql")),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor  # 以字典的形式返回操作结果，key:value
        )
        self.cur = self.conn.cursor()  # 创建一个游标，根据游标去查询数据

    # 传入sql，获取查询结果key:value
    def search_one(self, sql):
        self.cur.execute(sql)  # 1.查询
        result = self.cur.fetchone()  # 2.保存查询的结果
        return json.dumps(result, default=str, ensure_ascii=False)


if __name__ == "__main__":
    sql = OperationMysql()
    aa = sql.search_one(
        "select * from hb_member where user_email='1102055693@qq.com'")
    print(aa)
