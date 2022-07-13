import requests
import json
from selenium import webdriver
import time
from LogSystem import writeLog
import base64
from io import BytesIO
from PIL import Image
import re
from OCR import ddocr


class qndxx:
    def __init__(self, account, passwd):
        self.account = account
        self.password = passwd
        self.token = ""

    def getPic(self):
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"
        }
        yanzheng_url = "https://www.sxgqt.org.cn/bgsxapiv2/login/verify"

        text_data = requests.get(url=yanzheng_url, headers=head)
        with open('code.jpg', 'wb') as file:
            file.write(text_data.content)
        verify = input("请输入验证码：")
        return verify

    def getToken(self):
        # 失败  密码的加密算法无法破解
        head = {
            "referer": "https://www.sxgqt.org.cn/bgsxv2/login?redirect=%2Fbgsxv2%2Freunion%2Fmember%2FmemberList",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"
        }
        verify = self.getPic()
        url = "https://www.sxgqt.org.cn/bgsxapiv2/admin/login"
        data = {
            "account": self.account,
            "is_quick": 0,
            "pass": self.password,
            "verify": verify
        }

        text_data = requests.post(url=url, json=data, headers=head).text
        # data = json.loads(text_data)
        print(text_data)

    def base64_to_image(self, base64_str):
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        return img

    def login(self):
        # 成功   cookie里面存在token的值
        url = "https://www.sxgqt.org.cn/bgsxv2/login?redirect=%2Fbgsxv2%2Freunion%2Fmember%2FmemberList"
        try:

            driver = webdriver.Edge(executable_path='msedgedriver.exe')
        except Exception:
            print("请更新Edge浏览器到最新版本")
            return

        driver.implicitly_wait(3)  # 隐性等待3s
        # tkinter.messagebox.showerror('提示', '只需要输入验证码，请勿点击网页的登录按钮')
        while 1:

            driver.get(url)
            time.sleep(0.5)
            driver.find_element("xpath", "//*[@id='pane-first']/div/div/form/div[1]/div/div/input").send_keys(
                self.account)
            driver.find_element("xpath", "//*[@id='pane-first']/div/div/form/div[2]/div/div/input").send_keys(
                self.password)
            ce = driver.find_element("xpath", "//*[@id='pane-first']/div/div/form/div[3]/div/img").get_attribute("src")

            img = self.base64_to_image(ce)
            img.save('code.png')

            verfCode = ddocr('code.png')
            # tkinter.messagebox.showerror('提示', '输入验证码，然后关掉弹窗')

            driver.find_element("xpath", "//*[@id='pane-first']/div/div/form/div[3]/div/div/input").send_keys(
                verfCode)
            time.sleep(1)
            driver.find_element("xpath", "//*[@id='pane-first']/div/div/form/button").click()
            time.sleep(1)

            cur_cookies = driver.get_cookies()

            if cur_cookies[0]["name"] == "token":
                break

        # print(cur_cookies[0]["value"])
        self.token = cur_cookies[0]["value"]

        # with open("222222.txt", "w") as f:
        #     f.write(json.dumps(cur_cookies))
        driver.quit()

        return True

    def getRequest(self):
        list_meixue = []
        if self.login():
            head = {
                "token": self.token,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"
            }

            url = "https://www.sxgqt.org.cn/bgsxapiv2/regiment?page=1&rows=100&keyword=&oid=100612025&leagueStatus=&goHomeStatus=&memberCardStatus=&isPartyMember=&isAll="
            url_qing = "https://www.sxgqt.org.cn/bgsxapiv2/regiment/youngList?oid=100612025&keyword=&isAll=&page=1&rows=15"

            text_data = requests.get(url=url, headers=head).text
            data = json.loads(text_data)
            # print(data)
            for line in data['data']['data']:
                if line["isStudy"] == "否":
                    list_meixue.append(line['realname'])
            text_data = requests.get(url=url_qing, headers=head).text
            data = json.loads(text_data)
            # print(data)
            for line in data['data']['data']:
                if line["isStudy"] == "否":
                    list_meixue.append(line['realname'])

            if len(list_meixue) == 0:
                print("本期大学习全部完成")
            else:
                line1 = "共%d个人没学本期大学习" % len(list_meixue)
                line2 = " ".join(list_meixue)
                print(line1)
                print(line2)
                writeLog(line1)
                writeLog(line2)
        return list_meixue
