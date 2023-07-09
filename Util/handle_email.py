from email.mime.application import MIMEApplication
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys
import os

base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_path)

from Config.config import HandleInit


"""封装发送邮件的类,可以用jenkins来替代"""


class SendEmail(object):

    def __init__(self):
        self.handle_ini = HandleInit()
        self.email_host = self.handle_ini.get_value(
            "email_host", "email")  # SMTP服务器
        self.mail_user = self.handle_ini.get_value(
            "mail_user", "email")  # 发件人邮箱账号
        self.mail_pass = self.handle_ini.get_value(
            "mail_pass", "email")  # 发件人邮箱密码
        self.user_list = self.handle_ini.get_value(
            "user_list", "email")  # 收件人邮箱

    # 发送邮件
    def send_mail(self, sub, content):
        # 发件人
        mail_user = "wuchen" + "<" + self.mail_user + ">"
        # 附件
        htmlFile = base_path + "/Report/接口自动化测试报告.html"
        htmlApart = MIMEApplication(open(htmlFile, 'rb').read())
        htmlApart.add_header('content-disposition',
                             'attachment', filename=htmlFile)
        # 构建邮件
        msg_file = MIMEMultipart()
        msg_file['From'] = Header(mail_user)
        msg_file['To'] = Header(self.user_list)
        msg_file['Subject'] = sub
        msg = MIMEText(content, _subtype="plain", _charset="utf-8")
        msg_file.attach(msg)
        msg_file.attach(htmlApart)
        # 创建SMTP服务，连接163邮件服务器，并发送邮件
        server = smtplib.SMTP()
        server.connect(self.email_host)
        server.login(self.mail_user, self.mail_pass)
        server.sendmail(mail_user, self.user_list, msg_file.as_string())
        server.close()

    # 构建邮件
    def send_main(self, pass_list, fail_list):
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        count_num = pass_num + fail_num
        # 成功率
        pass_result = "%.2f%%" % (pass_num / count_num * 100)
        # 失败率
        fail_result = "%.2f%%" % (fail_num / count_num * 100)
        user_list = ["1102055693@qq.com"]
        sub = "接口自动化"
        content = "此次一共运行接口%s个,通过%s个,失败%s个,通过率为%s,失败率为%s" % (
            count_num, pass_num, fail_num, pass_result, fail_result)
        self.send_mail(sub, content)


if __name__ == "__main__":
    sen = SendEmail()
    sen.send_main([1, 2], [4, 5, 6])
