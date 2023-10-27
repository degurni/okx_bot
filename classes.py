
import okx.MarketData as Market
from okx import Account, MarketData, PublicData
import pandas as pd
import pandas_ta as ta
import numpy as np
import math

import conf

flag = '0'  # 0 - живая торговля, 1 - тестовая торговля
public = PublicData.PublicAPI(debug=False)
market = Market.MarketAPI(flag=flag, debug=False)
accaunt = Account.AccountAPI(api_key=conf.key, api_secret_key=conf.secret, passphrase=conf.passw,
                             flag=flag, debug=False)


def pairs(type: str='SPOT') -> list:
    """

    :param type:
    :return: {'alias': '',
              'baseCcy': 'FTM',
              'category': '1',
              'ctMult': '',
              'ctType': '',
              'ctVal': '',
              'ctValCcy': '',
              'expTime': '',
              'instFamily': '',
              'instId': 'FTM-OKB',
              'instType': 'SPOT',
              'lever': '',
              'listTime': '1635155926000',
              'lotSz': '0.000001',
              'maxIcebergSz': '999999999999.0000000000000000',
              'maxLmtSz': '999999999999',
              'maxMktSz': '1000000',
              'maxStopSz': '1000000',
              'maxTriggerSz': '999999999999.0000000000000000',
              'maxTwapSz': '999999999999.0000000000000000',
              'minSz': '1',
              'optType': '',
              'quoteCcy': 'OKB',
              'settleCcy': '',
              'state': 'live',
              'stk': '',
              'tickSz': '0.00001',
              'uly': ''}

    """
    res = public.get_instruments(instType=type)['data']
    pairs = []
    for i in res:
        pairs.append(i['instId'])
    return pairs

def candles(pair: str='BTC-USDT', tf: str='15m', limit: str='300') -> list:
    """
    Получить сведения о 300 последних рыночных свечах
    :param instId:
    :param bar:
    :param limit:
    :return:['1697125500000',           -Время
             '26668.4',                 -Открытие
             '26697.9',                 -Максимум
             '26605',                   -Минимум
             '26677.2',                 -Закрытие
             '6000603.65197306',
             '159971120351.05124191',
             '159971120351.05124191',
             '0']                       -1 - завершена. 0 - не завершена
    """
    res = market.get_candlesticks(instId=pair, bar=tf, limit=limit)
    if res['code'] == '0' and res['msg'] == '':
        # print(res['data'])
        return res['data']
    else:
        print(f'code - {res["code"]} : msg - {res["msg"]}')
        return []

# Преобразовываем данные о свечах в датафрейм
def frame(data):
    t = []
    o = []
    h = []
    l = []
    c = []
    v = []
    for i in data:
        t.append(int(i[0]) / 1000)
        o.append(float(i[1]))
        h.append(float(i[2]))
        l.append(float(i[3]))
        c.append(float(i[4]))
        v.append(float(i[5]))
    df = pd.DataFrame({'Time': t, 'Open': o, 'High': h, 'Low': l, 'Close': c, 'Volume': v})
    df.Time = pd.to_datetime(df.Time, unit='s')
    df.set_index('Time', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    # df.to_csv('df_data.csv')
    return df

# Получаем общий баланс
def balance():
    res = accaunt.get_account_balance()
    return res['data']

def detect_accumulation(df):
    means = df.Volume.mean()

    accum = [0] * len(df)
    detect = [0] * len(df)
    sum_detect = [0] * len(df)
    for i in range(len(df)):
        accum[i] = round(means / df.Volume.iloc[i], 2)
        detect[i] = round(df.Volume.diff().iloc[i] / df.Volume.iloc[i], 2)
    df['accum'] = accum
    df['detect'] = detect

    sum_detect[-1] = df.detect.iloc[-1]
    for i in reversed(range(len(df) - 1)):
        sum_detect[i] = sum_detect[i + 1] + df.detect.iloc[i]
    df['sum_detect'] = sum_detect
    print(df.sum_detect.max())
    df.to_csv('df_data.csv')

"""

Ax = 0
Ay = (-1)
Bx = 1
By = (0)
AB = корень (1*1 + )

A1-A2
"""




def _lenght_vektor(df):
    lenght_v = [0] * len(df)
    vector_sig = [0] * len(df)
    for i in range(len(df)):
        lenght_v[i] = math.sqrt(1 + (abs(df.MACD.iloc[i]) - abs(df.MACD.iloc[i-1])) ** 2)
        if lenght_v[i] > 1.000_012:
            vector_sig[i] = 2
        elif lenght_v[i] > 1.000_009:
            vector_sig[i] = 1
    df['lenght_v'] = lenght_v
    df['vector_sig'] = vector_sig
    return df

def _chek_signal(df):

    return df



def add_indicator(df: pd.DataFrame) -> pd.DataFrame:
    df[['MACD', 'MACDh', 'MACDs']] = ta.macd(close=df.Close, fast=12, slow=26, signal=9)
    # df['scal'] =
    df = _lenght_vektor(df=df)
    df = _chek_signal(df)
    df.to_csv('df_data.csv')
    return df

