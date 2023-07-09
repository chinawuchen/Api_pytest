import subprocess
import sys
import os


base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

"""封装执行shell语句方法"""


class Shell(object):

    def invoke(self, cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("latin-1")
        # o = output.decode("utf-8")
        return o


if __name__ == "__main__":
    shell = Shell()
    cmd = "ls"
    print(shell.invoke(cmd))
