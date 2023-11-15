from classes import OKXex, Bot

s = {'code': '0', 'data': [{'clOrdId': '', 'ordId': '644955062510850057', 'sCode': '0', 'sMsg': 'Order placed', 'tag': ''}], 'inTime': '1700041269588309', 'msg': '', 'outTime': '1700041269590599'}


# 'ordId': '644952027235651597'
# 'ordId': '644955062510850057'
# print(OKXex().order_details(symbol="KSM-USDT", ord_id='644952027235651597'))

print(s['data'][0]['ordId'])

