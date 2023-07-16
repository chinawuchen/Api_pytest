import pytest
import sys
import os

base_path = os.path.abspath("")
sys.path.append(base_path)


log_file = base_path + "/Log/log.txt"
# 每次执行用例之前清空一次日志
@pytest.fixture(scope="class")
def truncate_log():
    with open(log_file, 'w') as f:
        f.seek(0, 0)  # 把文件定位到0;truncate也是从这里开始删除
        f.truncate()
