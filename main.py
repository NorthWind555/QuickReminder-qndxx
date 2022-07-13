import configparser
import os

from qndxx import qndxx
from send_emile import send_mail

# 配置初始化
cf = configparser.ConfigParser()
cf.read("config.ini", encoding="utf8")
account = cf.get("accountPart", "account")
password = cf.get("accountPart", "password")
eAccount = cf.get("sendEmail", "eAccount")
eAuthorizationCode = cf.get("sendEmail", "eAuthorizationCode")
eTitle = cf.get("emailContent", "eTitle")
eContent = cf.get("emailContent", "eContent")

print("配置初始化--完成")
print("使用前请检查config文件是否配置正确")

# print("邮件发送测试模式，收信人：1321313876@qq.com")

# print("点击弹窗的确定按钮，程序才会继续运行")
qn = qndxx(account, password)
list_meixue = qn.getRequest()
# list_meixue = ["111"]
list_email = []
if input("是否发送提醒邮件(1发送，0不发送)：") == "1":
    for line in list_meixue:
        try:
            email = cf.get("emailList", line)
            list_email.append(email)
        except Exception:
            print(line + "\t未初始化邮箱")

    if len(list_meixue) == len(list_email):
        send_mail(list_email, eAccount, eAuthorizationCode, eTitle, eContent)
    else:
        print("请在config文件初始化所有人的邮箱后再运行")

os.system("pause")
