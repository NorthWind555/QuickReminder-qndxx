import smtplib
from email.mime.text import MIMEText
from email.header import Header

from email.mime.multipart import MIMEMultipart


def send_mail(accountList, eAccount, eAuthorizationCode, eTitle, eContent):
    msg_from = eAccount  # 发送方邮箱
    passwd = eAuthorizationCode  # 就是上面的授权码
    to_addr = accountList  # 接受方邮箱,列表
    # print(to)

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    content = eContent
    # 把内容加进去
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = eTitle

    # 设置发送者信息
    msg['From'] = '青年大学习提醒Bot'
    # 设置接受者信息
    msg['To'] = '未进行青年大学习的同学'

    # 开始发送
    try:
        temp_flag_email = msg_from.split("@")[-1]
        if temp_flag_email == "qq.com":
            # 通过SSL方式发送，服务器地址和端口
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        elif temp_flag_email == "163.com":
            s = smtplib.SMTP_SSL("smtp.163.com", 465)
        elif temp_flag_email == "gmail.com":
            s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        elif temp_flag_email == "126.com":
            s = smtplib.SMTP_SSL("smtp.126.com", 465)
        else:
            # 如果没有匹配，默认用QQ邮箱
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        # 开始发送
        res = s.sendmail(msg_from, to_addr, msg.as_string())
        if len(res) != 0:
            print("发送失败，错误码：", res)
        s.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败！！", e)
