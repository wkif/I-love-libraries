# /*
#  * @Author: kif kif101001000@163.com 
#  * @Date: 2022-10-25 18:18:42 
#  * @Last Modified by:   kif kif101001000@163.com  
#  * @Last Modified time: 2022-10-25 18:18:42 
#  */
import requests

session = requests.Session()


def login(loginUrl):
    # Args:
    #   arg1 : self
    # Returns:
    #   Boolean value indicating whether

    loginCookies = {
        'Hm_lvt_7ecd21a13263a714793f376c18038a87': '1666664612,1666665692',
        'Hm_lpvt_7ecd21a13263a714793f376c18038a87': '1666665723',
        'SERVERID': 'd3936289adfff6c3874a2579058ac651|1666665723|1666665723',
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
    res = session.get(loginUrl, headers=headers, cookies=loginCookies)
    return True


def getHome():
    json_data = {
        'operationName':
        'list',
        'query':
        'query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n libGroups {\n id\n group_name\n }\n reserve {\n isRecordUser\n }\n }\n record {\n libs {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_color_name\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n }\n rule {\n signRule\n }\n }\n}',
    }

    response = session.post(
        'https://wechat.v2.traceint.com/index.php/graphql/', json=json_data)
    list = []
    responseList = response.json()['data']['userAuth']['reserve']['libs']
    for res in responseList:
        list.append({
            'id':
            res['lib_id'],
            'name':
            res['lib_name'],
            'hasSeat':
            res['lib_rt']['seats_total'] - res['lib_rt']['seats_used']
        })
    return (list)


def getSeat(libId):

    json_data = {
        'operationName': 'libLayout',
        'query':
        'query libLayout($libId: Int, $libType: Int) {\n userAuth {\n reserve {\n libs(libType: $libType, libId: $libId) {\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n lib_layout {\n seats_total\n seats_booking\n seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n type\n name\n seat_status\n status\n }\n }\n }\n }\n }\n}',
        'variables': {
            'libId': libId,
        },
    }

    response = session.post(
        'https://wechat.v2.traceint.com/index.php/graphql/', json=json_data)
    responseList = response.json(
    )['data']['userAuth']['reserve']['libs'][0]['lib_layout']['seats']
    list = []
    for res in responseList:
        if res['name']:
            status = ''
            if res['seat_status'] == 1:
                status = '可选'
            if res['seat_status'] == 3:
                status = '已被选'
            if res['seat_status'] == 2:
                status = '可被预约'
            list.append({
                '位置': res['name'],
                'key': res['key'],
                '状态 seat_status': status,
            })
    return list


if __name__ == '__main__':


    loginUrl = input('请输入首页地址:\n')
    login(loginUrl)
    homeList = getHome()
    print('房间：', homeList)
    libId = input('输入房间id：\n')
    SeatList = getSeat(libId)
    print('位置：', SeatList)
