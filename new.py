
import asyncio
import websockets
import json
import zlib
import datetime


import conf






passphrase = conf.passw
secret_key = conf.secret
api_key = conf.key


# URL для реальной торговли
url = "wss://ws.okx.com:8443/ws/v5/public"
channels = [{"channel": "trades", "instId": "ZIL-USDT-SWAP"}]

def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

def partial(res):
    data_obj = res['data'][0]
    bids = data_obj['bids']
    asks = data_obj['asks']
    instrument_id = res['arg']['instId']
    return bids, asks, instrument_id

def change(num_old):
    num = pow(2, 31) - 1
    if num_old > num:
        out = num_old - num * 2 - 2
    else:
        out = num_old
    return out

def sort_num(n):
    if n.isdigit():
        return int(n)
    else:
        return float(n)

def check(bids, asks):
    # 获取bid档str
    bids_l = []
    bid_l = []
    count_bid = 1
    while count_bid <= 25:
        if count_bid > len(bids):
            break
        bids_l.append(bids[count_bid-1])
        count_bid += 1
    for j in bids_l:
        str_bid = ':'.join(j[0 : 2])
        bid_l.append(str_bid)
    # 获取ask档str
    asks_l = []
    ask_l = []
    count_ask = 1
    while count_ask <= 25:
        if count_ask > len(asks):
            break
        asks_l.append(asks[count_ask-1])
        count_ask += 1
    for k in asks_l:
        str_ask = ':'.join(k[0 : 2])
        ask_l.append(str_ask)
    # 拼接str
    num = ''
    if len(bid_l) == len(ask_l):
        for m in range(len(bid_l)):
            num += bid_l[m] + ':' + ask_l[m] + ':'
    elif len(bid_l) > len(ask_l):
        # bid档比ask档多
        for n in range(len(ask_l)):
            num += bid_l[n] + ':' + ask_l[n] + ':'
        for l in range(len(ask_l), len(bid_l)):
            num += bid_l[l] + ':'
    elif len(bid_l) < len(ask_l):
        # ask档比bid档多
        for n in range(len(bid_l)):
            num += bid_l[n] + ':' + ask_l[n] + ':'
        for l in range(len(bid_l), len(ask_l)):
            num += ask_l[l] + ':'

    new_num = num[:-1]
    int_checksum = zlib.crc32(new_num.encode())
    fina = change(int_checksum)
    return fina

def update_bids(res, bids_p):
    # 获取增量bids数据
    bids_u = res['data'][0]['bids']
    # print('增量数据bids为：' + str(bids_u))
    # print('档数为：' + str(len(bids_u)))
    # bids合并
    for i in bids_u:
        bid_price = i[0]
        for j in bids_p:
            if bid_price == j[0]:
                if i[1] == '0':
                    bids_p.remove(j)
                    break
                else:
                    del j[1]
                    j.insert(1, i[1])
                    break
        else:
            if i[1] != "0":
                bids_p.append(i)
    else:
        bids_p.sort(key=lambda price: sort_num(price[0]), reverse=True)
        # print('合并后的bids为：' + str(bids_p) + '，档数为：' + str(len(bids_p)))
    return bids_p

def update_asks(res, asks_p):
    # 获取增量asks数据
    asks_u = res['data'][0]['asks']
    # print('增量数据asks为：' + str(asks_u))
    # print('档数为：' + str(len(asks_u)))
    # asks合并
    for i in asks_u:
        ask_price = i[0]
        for j in asks_p:
            if ask_price == j[0]:
                if i[1] == '0':
                    asks_p.remove(j)
                    break
                else:
                    del j[1]
                    j.insert(1, i[1])
                    break
        else:
            if i[1] != "0":
                asks_p.append(i)
    else:
        asks_p.sort(key=lambda price: sort_num(price[0]))
        # print('合并后的asks为：' + str(asks_p) + '，档数为：' + str(len(asks_p)))
    return asks_p

# Подписка на публичные каналы
async def subscribe_without_login(url, channels):
    l = []
    while True:
        try:
            async with websockets.connect(url) as ws:
                sub_param = {"op": "subscribe", "args": channels}
                sub_str = json.dumps(sub_param)
                await ws.send(sub_str)
                print(f"Отправляем: {sub_str}")

                while True:
                    try:
                        res = await asyncio.wait_for(ws.recv(), timeout=25)
                    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                        try:
                            await ws.send('ping')
                            res = await ws.recv()
                            print(f'{res}')
                            continue
                        except Exception as e:
                            print('Соединение прервано, повторное подключение...')
                            break

                    # print(get_timestamp() + res)
                    res = eval(res)
                    # print(res.items())
                    # print(res)
                    if 'data' in res:
                        with open(file='torg_data.json', mode='a', newline='') as f:
                            f.write(json.dumps(res['data'][0]))

                    await asyncio.sleep(1)


        #             if 'event' in res:
        #                 continue
        #             for i in res['arg']:
        #                 if 'books' in res['arg'][i] and 'books5' not in res['arg'][i]:
        #                     if res['action'] == 'snapshot':
        #                         for m in l:
        #                             if res['arg']['instId'] == m['instrument_id']:
        #                                 l.remove(m)
        #                         bids_p, asks_p, instrument_id = partial(res)
        #                         d = {}
        #                         d['instrument_id'] = instrument_id
        #                         d['bids_p'] = bids_p
        #                         d['asks_p'] = asks_p
        #                         l.append(d)
        #
        #                         checksum = res['data'][0]['checksum']
        #                         check_num = check(bids_p, asks_p)
        #                         if check_num == checksum:
        #                             print("Результат проверки：True")
        #                         else:
        #                             print("Результат проверки：False，Повторная подписка...")
        #
        #                             await unsubscribe_without_login(url, channels)
        #                             async with websockets.connect(url) as ws:
        #                                 sub_param = {"op": "subscribe", "args": channels}
        #                                 sub_str = json.dumps(sub_param)
        #                                 await ws.send(sub_str)
        #                                 print(f"Отправляем: {sub_str}")
        #                     elif res['action'] == 'update':
        #                         for j in l:
        #                             if res['arg']['instId'] == j['instrument_id']:
        #                                 bids_p = j['bids_p']
        #                                 asks_p = j['asks_p']
        #                                 bids_p = update_bids(res, bids_p)
        #                                 asks_p = update_asks(res, asks_p)
        #                                 checksum = res['data'][0]['checksum']
        #                                 check_num = check(bids_p, asks_p)
        #                                 if check_num == checksum:
        #                                     print("Результат проверки：True")
        #                                 else:
        #                                     print("Результат проверки：False，Повторная подписка...")
        #                                     await unsubscribe_without_login(url, channels)
        #                                     async with websockets.connect(url) as ws:
        #                                         sub_param = {"op": "subscribe", "args": channels}
        #                                         sub_str = json.dumps(sub_param)
        #                                         await ws.send(sub_str)
        #                                         print(f"Отправляем: {sub_str}")
        except Exception as e:
            print(e)
            print('Соединение прервано, повторное подключение...')
            continue
        else:
            await asyncio.sleep(1)


# отписаться от каналов
async def unsubscribe_without_login(url, channels):
    async with websockets.connect(url) as ws:
        # unsubscribe
        sub_param = {"op": "unsubscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await ws.send(sub_str)
        print(f"send: {sub_str}")

        res = await ws.recv()
        print(f"recv: {res}")

async def buy_sell():

    with open('torg_data.json', 'r') as f:
        print(f)

async def main():
    errands = []
    errands.append(subscribe_without_login(url=url, channels=channels))
    errands.append(buy_sell())
    await asyncio.gather(*errands)




asyncio.run(main())
