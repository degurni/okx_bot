import json

import okx.MarketData as Market
from okx import Account, MarketData, PublicData, Trade
import pandas as pd
import pandas_ta as ta
import numpy as np
import math
import datetime
import os

import conf
if os.path.isfile('keys.py'):
    import keys
    key = keys.key
    secret = keys.secret
    passw = keys.passw
else:
    key = conf.key
    secret = conf.secret
    passw = conf.passw

flag = '0'  # 0 - живая торговля, 1 - тестовая торговля
public = PublicData.PublicAPI(flag=flag, debug=False)
market = Market.MarketAPI(flag=flag, debug=False)
accaunt = Account.AccountAPI(api_key=key, api_secret_key=secret, passphrase=passw,
                             flag=flag, debug=False)
trade = Trade.TradeAPI(api_key=key, api_secret_key=secret, passphrase=passw,
                             flag=flag, debug=False)

# PUBLIC
def get_instrument(symbol: str, inst_type: str='SWAP'):
    """

    :param symbol:
    :param inst_type: SPOT, MARGIN, SWAP, FUTURES, OPTION
    :return:{'alias': '',
             'baseCcy': '',
             'category': '1',
             'ctMult': '1',
             'ctType': 'linear',
             'ctVal': '0.1',
             'ctValCcy': 'TRB',
             'expTime': '',
             'instFamily': 'TRB-USDT',
             'instId': 'TRB-USDT-SWAP',
             'instType': 'SWAP',
             'lever': '50',
             'listTime': '1611916828000',
             'lotSz': '1',
             'maxIcebergSz': '100000000.0000000000000000',
             'maxLmtSz': '100000000',
             'maxMktSz': '28000',
             'maxStopSz': '28000',
             'maxTriggerSz': '100000000.0000000000000000',
             'maxTwapSz': '100000000.0000000000000000',
             'minSz': '1',
             'optType': '',
             'quoteCcy': '',
             'settleCcy': 'USDT',
             'state': 'live',
             'stk': '',
             'tickSz': '0.001',
             'uly': 'TRB-USDT'}
    """
    return public.get_instruments(instType=inst_type, instId=symbol)



# ACCAUNT

def order_details(symbol: str, ord_id: str):
    """

    :param symbol:
    :param ord_id:
    :return:{'accFillSz': '1',
             'algoClOrdId': '',
             'algoId': '',
             'attachAlgoClOrdId': '',
             'avgPx': '126.466',
             'cTime': '1699298365373',
             'cancelSource': '',
             'cancelSourceReason': '',
             'category': 'normal',
             'ccy': '',
             'clOrdId': '',
             'fee': '-0.0063233',
             'feeCcy': 'USDT',
             'fillPx': '126.466',
             'fillSz': '1',
             'fillTime': '1699298365373',
             'instId': 'TRB-USDT-SWAP',
             'instType': 'SWAP',
             'lever': '10',
             'ordId': '641839096390262784',
             'ordType': 'market',
             'pnl': '0',
             'posSide': 'net',
             'px': '',
             'pxType': '',
             'pxUsd': '',
             'pxVol': '',
             'quickMgnType': '',
             'rebate': '0',
             'rebateCcy': 'USDT',
             'reduceOnly': 'false',
             'side': 'buy',
             'slOrdPx': '',
             'slTriggerPx': '',
             'slTriggerPxType': '',
             'source': '',
             'state': 'filled',
             'stpId': '',
             'stpMode': '',
             'sz': '1',
             'tag': '',
             'tdMode': 'cross',
             'tgtCcy': '',
             'tpOrdPx': '',
             'tpTriggerPx': '',
             'tpTriggerPxType': '',
             'tradeId': '135788695',
             'uTime': '1699298365375'}

    """
    return trade.get_order(instId=symbol, ordId=ord_id)['data'][0]

# Получить открытые позиции
def get_positions(symbol: str = None):
    """
    Получить открытые позиции
    :return: {'adl': '1',                          уровень делевереджа
              'availPos': '',
              'avgPx': '102.1168888888888889',     цена входа
              'baseBal': '',
              'baseBorrowed': '',
              'baseInterest': '',
              'bePx': '102.96527791777321',
              'bizRefId': '',
              'bizRefType': '',
              'cTime': '1698925498071',
              'ccy': 'USDT',
              'closeOrderAlgo': [],
              'deltaBS': '',
              'deltaPA': '',
              'fee': '-0.05816884',                комиссия
              'fundingFee': '0.0080302563557077',
              'gammaBS': '',
              'gammaPA': '',
              'idxPx': '101.316',
              'imr': '3.0357000000000003',
              'instId': 'TRB-USDT-SWAP',
              'instType': 'SWAP',
              'interest': '',
              'last': '101.228',
              'lever': '10',                       плечо
              'liab': '',
              'liabCcy': '',
              'liqPenalty': '0',
              'liqPx': '2.041765621390252',
              'margin': '',
              'markPx': '101.19',
              'mgnMode': 'cross',
              'mgnRatio': '139.99481419389195',
              'mmr': '0.1973205',
              'notionalUsd': '30.361553550000007',
              'optVal': '',
              'pendingCloseOrdLiabVal': '',
              'pnl': '-0.1889333333333333',
              'pos': '3',                          размер позиции
              'posCcy': '',
              'posId': '637080880187998214',       ID
              'posSide': 'net',
              'quoteBal': '',
              'quoteBorrowed': '',
              'quoteInterest': '',
              'realizedPnl': '-0.2390719169776256',
              'sId': 0,
              'spotInUseAmt': '',
              'spotInUseCcy': '',
              'thetaBS': '',
              'thetaPA': '',
              'tradeId': '131783287',
              'uTime': '1698954196183',
              'upl': '-0.278066666666669',
              'uplLastPx': '-0.26666666666667',
              'uplRatio': '-0.0907674429738481',
              'uplRatioLastPx': '-0.0870462171890174',
              'usdPx': '',
              'userId': 44786666,
              'vegaBS': '',
              'vegaPA': ''}

    """
    if symbol:
        return accaunt.get_positions(instId=symbol)['data']
    else:
        # Если не пердовать название торговой пары то получим только открытые позиции
        return accaunt.get_positions(instType='SWAP')['data']


# Изменяем плечо
def set_lever(symbol: str, lever: str):
    """
    Изменяем плечо
    :param symbol:       DYDX-USDT-SWAP
    :param lever:        желаемое плечо
    :return:
    """
    s = accaunt.set_leverage(instId=symbol, lever=lever, mgnMode='cross')
    return s



# TRADE

def amend_order(symbol: str):
    s = trade.amend_order(instId=symbol, newTpTriggerPx='129.065', newTpOrdPx='-1',
                          newSlTriggerPx='123.929', newSlOrdPx='-1')
    return s

def plas_order(symbol: str, side: str, size: str):
    data = {
        'instId': symbol,
        'tdMode': 'cross',
        'side': side,
        'ordType': 'market',
        'sz': size
    }
    poz_id = trade.place_order(**data)['data']['ordId']
    # Запрашиваем информацию об открытой позиции
    f = get_positions(symbol=symbol)
    open_price = f[0]['avgPx']
    fee = f[0]['fee']
    lever = f[0]['lever']
    size = f[0]['pos']
    pos_id = f[0]['posId']





def plas_order_and_tp_sl(symbol: str, side: str, size: str, tp: str, sl: str):
    """
    Выставляем рыночный ордер и тейкпрофит и стоплосс
    :param symbol:      ATOM-USDT-SWAP
    :param side:        buy или sell
    :param size:        кол-во контрактов
    :param tp:          цена тейкпрофита
    :param sl:          цена стоплосса
    :return:
    """
    answer = trade.place_order(instId=symbol, tdMode='cross', side=side, ordType='market',
                               sz=size, tpTriggerPx=tp, tpOrdPx='-1', slTriggerPx=sl, slOrdPx='-1')
    return answer['data']

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
    sig = [0] * len(df)
    for i in range(len(df)):
        if df.CCI_sig.iloc[i] == 'SHORT' and df.MACD_sig.iloc[i] == 'SHORT':
            sig[i] = 'SHORT'
            # print(df.index[i], sig[i])
        elif df.CCI_sig.iloc[i] == 'LONG' and df.MACD_sig.iloc[i] == 'LONG':
            sig[i] = 'LONG'
            # print(df.index[i], sig[i])
    df['SIG'] = sig
    # print(df.SIG.value_counts())
    return df

def _chek_CCI_signal(df: pd.DataFrame) ->pd.DataFrame:
    predel = 100
    cci_sig = [0] * len(df)
    for i in range(len(df)):
        if df.CCI.iloc[i - 2] > df.CCI.iloc[i - 1] < df.CCI.iloc[i] < -1 * predel:
            cci_sig[i] = 'LONG'
        elif df.CCI.iloc[i - 2] < df.CCI.iloc[i - 1] > df.CCI.iloc[i] > predel:
            cci_sig[i] = 'SHORT'
    df['CCI_sig'] = cci_sig
    # print(df.CCI_sig.value_counts())
    return df

def _chek_macd_signal(df: pd.DataFrame) -> pd.DataFrame:
    macd_sig = [0] * len(df)
    for i in range(len(df)):
        if df.MACD.iloc[i-2] < df.MACD.iloc[i-1] > df.MACD.iloc[i] and df.MACDh.iloc[i -1] > df.MACDh.iloc[i] > 0:
            macd_sig[i] = 'SHORT'
        elif df.MACD.iloc[i-2] > df.MACD.iloc[i-1] < df.MACD.iloc[i] and df.MACDh.iloc[i -1] < df.MACDh.iloc[i] < 0:
            macd_sig[i] = 'LONG'
    df['MACD_sig'] = macd_sig
    # print(df.MACD_sig.value_counts())
    return df

def add_indicator(df: pd.DataFrame) -> pd.DataFrame:
    df[['MACD', 'MACDh', 'MACDs']] = ta.macd(close=df.Close, fast=12, slow=26, signal=9)
    df['CCI'] = ta.cci(high=df.High, low=df.Low, close=df.Close,length=40)

    df = _chek_CCI_signal(df=df)
    df = _chek_macd_signal(df=df)

    df = _chek_signal(df)
    # df.to_csv('df_data.csv')
    return df



class Bot:

    def _time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    def debug(self, var: str, inf: str) -> None:
        time = Bot()._time() if var == 'debug' else None
        if conf.debug == 'inform':
            if var == 'inform':
                print(inf)
            elif var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'debug':
            if var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'error':
            if var == 'error':
                print('\033[31m {} \033[0;0m'.format(inf))

    def chek_files(self):
        Bot().debug('debug', 'Проверяем наличие вспомогательных файлов')
        if not os.path.isfile('trades.json'):
            with open('trades.json', 'w') as f:
                json.dump([], f)

    def checking_open_positions(self, symbol: str = None):
        with open('trades.json', 'r') as f:
            inf = json.loads(f.read())
        s = False
        if symbol and len(inf) != 0:
            for i in inf:
                if i['symbol'] == symbol:
                    s = True
        elif not symbol:
            if len(inf) == 0:
                Bot().debug('debug', 'Бот ещё не выставлял ордера, открытых позиций нет')
            else:
                Bot().debug('debug', f'Открыто {len(inf)} позиций')
        return s
