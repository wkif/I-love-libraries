# /*
#  * @Author: kif kif101001000@163.com
#  * @Date: 2022-10-25 16:39:02
#  * @Last Modified by:   kif kif101001000@163.com
#  * @Last Modified time: 2022-10-25 16:39:02
#  */

from ast import Str
from re import T
from time import sleep
import requests

serverSendKey = ''
# server酱SendKey  link：https://sct.ftqq.com/sendkey

loginUrl = ''
# "我去图书馆"首页地址，获取方式见readme
libId = ''
# 期望图书馆房间，获取方式见readme
seatKeyList = []
#  期望位置列表，获取方式见readme


class getData():

    def __init__(self):
        self.session = requests.Session()
        #  session类
        self.serverCode = serverSendKey
        # server酱SendKey
        self.user = 'dlt'
        #  用户名，自定义，用于server酱提示信息展示
        self.loginUrl = loginUrl
        # "我去图书馆"首页地址
        self.seatKeyList = seatKeyList
        # 期望位置列表
        self.submitCount = 0
        # 占位请求计数器
        self.libId = libId
        # 期望图书馆房间
        self.message = ''
        #  server消息

    def login(self):
        # Args:
        #   arg1 : self
        # Returns:
        #   Boolean value indicating whether

        loginCookies = {
            'Hm_lvt_7ecd21a13263a714793f376c18038a87': '1666664612,1666665692',
            'Hm_lpvt_7ecd21a13263a714793f376c18038a87': '1666665723',
            'SERVERID':
            'd3936289adfff6c3874a2579058ac651|1666665723|1666665723',
        }

        headers = {
            'authority':
            'wechat.v2.traceint.com',
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language':
            'zh-CN,zh;q=0.9',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'Hm_lvt_7ecd21a13263a714793f376c18038a87=1666664612,1666665692; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1666665723; SERVERID=d3936289adfff6c3874a2579058ac651|1666665723|1666665723',
            'sec-ch-ua':
            '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile':
            '?0',
            'sec-ch-ua-platform':
            '"Windows"',
            'sec-fetch-dest':
            'document',
            'sec-fetch-mode':
            'navigate',
            'sec-fetch-site':
            'none',
            'sec-fetch-user':
            '?1',
            'upgrade-insecure-requests':
            '1',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        res = self.session.get(self.loginUrl,
                               headers=headers,
                               cookies=loginCookies)
        return True

    def submit(self):
        #  占位请求方法

        if self.submitCount >= len(self.seatKeyList):
            return True
        json_data = {
            'operationName': 'reserueSeat',
            'query':
            'mutation reserueSeat($libId: Int!, $seatKey: String!, $captchaCode: String, $captcha: String!) {\n userAuth {\n reserve {\n reserueSeat(\n libId: $libId\n seatKey: $seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n )\n }\n }\n}',
            'variables': {
                'seatKey': self.seatKeyList[self.submitCount],
                'libId': self.libId,
                'captchaCode': '',
                'captcha': '',
            },
        }
        response = self.session.post(
            'https://wechat.v2.traceint.com/index.php/graphql/',
            json=json_data)
        print(response.json())
        if response.json()['errors']:
            self.message = response.json()['errors'][0]['msg']
            return response.json(
            )['data']['userAuth']['reserve']['reserueSeat']
        else:
            return True

    def sendMessage(self, message):
        # server 请求函数
        requests.get("https://sc.ftqq.com/" + self.serverCode +
                     ".send?text={}&desp={}".format(
                         '图书馆抢座结果', message + ':\n' + self.user))

    def main(self):
        
        self.submitCount = 0
        self.login()
        while not self.submit() and self.submitCount < 5:
            if self.message == '该座位已经被人预定了!(3)':

                if self.submitCount + 1 < len(self.seatKeyList):
                    self.submitCount += 1
                    message = '第' + str(
                        self.submitCount
                    ) + '次抢座失败:' + self.message + ',换位置到' + self.seatKeyList[
                        self.submitCount]
                    self.sendMessage(message)
                    sleep(1)
                    # self.submit()
                else:
                    self.submitCount = len(self.seatKeyList) - 1
                    message = '第' + str(
                        self.submitCount) + '次抢座失败:' + self.message
                    self.sendMessage(message)
            elif self.message == 'access denied!':
                message = '可能退出登陆过，正在重试。。。'
                self.sendMessage(message)
                self.login()
                sleep(1)
                # self.submit()
                self.submitCount = len(self.seatKeyList) - 1
            elif self.message == '请重新尝试':
                self.login()
                sleep(2)
                # self.submit()
                self.submitCount += 1
            elif self.message == '操作失败, 您已经预定了座位!':
                message = '抢座成功'
                self.sendMessage(message)
                self.submitCount = len(self.seatKeyList) - 1
                break
            else:
                self.login()
                sleep(1)
                # self.submit()
                self.submitCount += 1
                message = '第' + str(self.submitCount) + '次抢座失败:' + self.message
                self.sendMessage(message)


kif = getData()
kif.main()