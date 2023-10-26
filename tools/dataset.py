
import pandas as pd
from okx.MarketData import MarketAPI


class OkxDf:

    def __init__(self):
        self.flag = '1'
        self.debug = False
        self.inst_type = 'SPOT'  # 'SWAP', 'FUTURES', 'OPTION', 'SPOT'
        self.market = MarketAPI(flag=self.flag, debug=self.debug)

        # SWAP

        # ['ETC-USDT-SWAP', 'CETUS-USDT-SWAP', 'CRV-USDT-SWAP', 'SUSHI-USDT-SWAP', 'XLM-USDT-SWAP', 'DASH-USDT-SWAP',
        # 'THETA-USDT-SWAP', 'CRO-USDT-SWAP', 'LTC-USDT-SWAP', 'UNI-USDT-SWAP', 'XMR-USD-SWAP', 'IOST-USDT-SWAP',
        # 'BTC-USDT-SWAP', 'BNB-USDT-SWAP', 'APT-USDT-SWAP', 'NEO-USDT-SWAP', 'AVAX-USDT-SWAP', 'LPT-USDT-SWAP',
        # 'ZEC-USD-SWAP', 'KNC-USDT-SWAP', 'ORBS-USDT-SWAP', 'XLM-USD-SWAP', 'LINK-USDT-SWAP', 'DOGE-USDT-SWAP',
        # 'COMP-USDT-SWAP', 'VRA-USDT-SWAP', 'YFI-USD-SWAP', 'MKR-USDT-SWAP', 'UNI-USD-SWAP', 'SOL-USD-SWAP',
        # 'GRT-USDT-SWAP', 'AVAX-USD-SWAP', 'DOT-USD-SWAP', 'FIL-USDT-SWAP', 'FIL-USD-SWAP', 'ETH-USDT-SWAP',
        # 'SHIB-USDT-SWAP', 'MINA-USDT-SWAP', 'IMX-USDT-SWAP', 'SUI-USDT-SWAP', 'XTZ-USDT-SWAP', 'EOS-USDT-SWAP',
        # 'PEPE-USDT-SWAP', 'CRV-USD-SWAP', 'LRC-USDT-SWAP', 'OP-USDT-SWAP', 'GFT-USDT-SWAP', 'KISHU-USDT-SWAP',
        # 'SUSHI-USD-SWAP', 'BCH-USDT-SWAP', 'LTC-USD-SWAP', 'ETHW-USDT-SWAP', 'ATOM-USDT-SWAP', 'YGG-USDT-SWAP',
        # 'AAVE-USDT-SWAP', 'XMR-USDC-SWAP', 'TRX-USD-SWAP', 'ALGO-USDT-SWAP', 'BTC-USDC-SWAP', 'ADA-USDT-SWAP',
        # 'ADA-USD-SWAP', 'ETC-USD-SWAP', 'SAND-USDT-SWAP', 'TRX-USDT-SWAP', 'CELO-USDT-SWAP', 'BTC-USD-SWAP',
        # 'OMG-USDT-SWAP', 'EOS-USD-SWAP', '1INCH-USD-SWAP', 'DASH-USD-SWAP', 'GRT-USD-SWAP', 'ICP-USDT-SWAP',
        # 'BAND-USDT-SWAP', 'LDO-USDT-SWAP', 'ZEC-USDT-SWAP', 'QTUM-USDT-SWAP', 'YFI-USDT-SWAP', '1INCH-USDT-SWAP',
        # 'SOL-USDT-SWAP', 'ETH-USD-SWAP', 'ETH-USDC-SWAP', 'ATOM-USD-SWAP', 'DOT-USDT-SWAP', 'NEO-USD-SWAP',
        # 'AIDOGE-USDT-SWAP', 'DOGE-USD-SWAP', 'REN-USDT-SWAP', 'USDC-USDT-SWAP', 'LINK-USD-SWAP', 'XCH-USDT-SWAP',
        # 'GMT-USDT-SWAP', 'ALGO-USD-SWAP', 'KSM-USD-SWAP', 'ZIL-USDT-SWAP', 'KSM-USDT-SWAP', 'YFII-USDT-SWAP',
        # 'CFX-USDT-SWAP', 'MASK-USDT-SWAP', 'FRONT-USDT-SWAP', 'ZEN-USDT-SWAP', 'ATOM-USDC-SWAP', 'NEAR-USDT-SWAP',
        # 'FTM-USDT-SWAP', 'XRP-USDT-SWAP', 'HBAR-USDT-SWAP', 'BNT-USDT-SWAP', 'BAL-USDT-SWAP', 'BSV-USD-SWAP',
        # 'RDNT-USDT-SWAP', 'MAGIC-USDT-SWAP', 'AXS-USDT-SWAP', 'XMR-USDT-SWAP']

        # SPOT
        # ['CVC-OKB', 'MDT-USDT', 'OKB-USDT', 'OAS-USDT', 'LINK-BTC', 'LSK-OKB', 'KNC-USDT', 'MASK-ETH', 'NYM-USDT',
        # 'XTZ-USDT', 'LUNA-USDT', 'XEM-ETH', 'ETHW-USDC', 'SOL-ETH', 'ATOM-ETH', 'RVN-USDT', 'WLD-USDT', 'OP-USDT',
        # 'REN-USDT', 'LSK-USDT', 'QTUM-USDC', 'IOTA-USDT', 'ETHW-USDT', 'SUI-USDT', 'BCH-BTC', 'ICP-USDT', 'XRP-USDC',
        # 'OP-USDC', 'QTUM-OKB', 'AAVE-ETH', 'ADA-OKB', 'QTUM-USDT', 'BSV-USDT', 'LINK-OKB', 'XMR-USDT', 'ADA-BTC',
        # 'AXS-USDT', 'YFII-USDC', 'ZEN-USDT', 'XRP-ETH', 'KLAY-USDC', 'BCH-USDC', 'FTM-USDC', 'BTM-USDC', 'BSV-USDC',
        # 'BTM-OKB', 'OMN-USDT', 'ETC-USDT', 'DORA-USDT', 'SSWP-USDT', 'FTM-USDT', 'BCH-USDT', 'XMR-USDC', 'FIL-ETH',
        # 'ETC-USDC', 'MAGIC-USDT', 'AZY-ETH', 'LTC-BTC', 'SWRV-USDT', 'DEP-OKB', 'APT-USDT', 'GAS-USDT', 'FRONT-USDT',
        # 'TRX-USDT', 'CELR-USDT', 'LRC-USDT', 'CELO-USDT', 'KONO-USDT', 'ICP-OKB', 'SAND-USDT', 'LPT-OKB', 'LAT-USDT',
        # 'APT-USDC', 'KLAY-USDT', 'CRO-USDT', 'EOS-OKB', 'DASH-USDC', 'FIL-USDC', 'XMR-ETH', 'SOL-USDT', 'API3-USDT',
        # 'BAL-OKB', 'YFI-USDT', 'SC-USDT', 'ARB-USDC', 'LDO-USDT', 'AVAX-OKB', 'FIL-USDT', 'MATIC-BTC', 'GEAR-USDT',
        # 'YFI-USDC', 'RSR-USDT', 'AAVE-USDC', 'XLM-ETH', 'TON-USDT', 'DOGE-USDC', 'AAVE-USDT', 'CHAT-USDT',
        # 'TMTG-USDT', 'PAX-USDT', 'ETH-BTC', 'BZZ-USDT', 'MATIC-USDT', 'DOGE-USDT', 'ORBS-USDT', 'YFII-USDT',
        # 'ONT-USDT', 'SOL-USDC', 'FXS-USDT', 'UMA-USDT', 'FITFI-USDT', 'FTM-OKB', 'MATIC-USDC', 'XRP-USDT',
        # 'AIDOGE-USDT', 'LPT-USDT', 'ATOM-USDC', 'BNB-USDT', 'XLM-USDC', 'OMG-BTC', 'CRV-USDT', 'BAND-USDT',
        # 'ARB-USDT', 'XLM-USDT', 'DOGE-BTC', 'NEAR-OKB', 'YGG-USDT', 'LINK-ETH', 'HC-USDT', 'PAX-ETH', 'NEO-USDT',
        # 'XUC-USDT', 'ATOM-USDT', 'BNT-USDT', 'MRST-USDT', 'USDC-USDT', 'DOT-USDT', 'WXT-USDT', 'BNT-OKB', 'MINA-USDT',
        # 'EOS-USDT', 'DOT-USDC', 'GMX-USDT', 'CVC-USDT', 'TRX-BTC', 'GRT-USDT', 'SHIB-BTC', 'SKL-USDT', 'NYM-OKB',
        # 'DOT-BTC', 'GMX-USDC', 'IOST-USDT', 'KSM-USDT', 'LTC-USDC', 'BTC-USDC', 'SFG-USDT', 'JOE-USDT', 'RDNT-USDT',
        # 'ETH-USDT', 'BAND-OKB', 'BTC-USDT', 'GFT-USDT', 'BSV-BTC', 'OMG-USDC', 'CETUS-USDT', 'CONV-USDT', 'AVAX-BTC',
        # 'CVP-USDT', 'ALGO-USDC', 'OMG-USDT', 'IMX-USDC', 'ALV-USDT', 'BAL-USDT', 'TON-USDC', 'ZIL-USDT', 'OKT-BTC',
        # 'BIGTIME-USDT', 'BZZ-OKB', 'CELO-OKB', 'IMX-USDT', 'COMP-USDT', 'UNI-USDC', 'MYRIA-USDT', 'ALGO-USDT',
        # 'ATOM-BTC', 'ADA-USDC', 'KISHU-USDT', 'ALGO-OKB', 'ETC-BTC', 'OKB-BTC', 'AAVE-BTC', 'DASH-USDT',
        # 'BABYDOGE-USDT', 'ADA-USDT', 'HNT-USDT', 'ALPHA-USDT', 'SHIB-USDT', 'TUSD-USDT', 'ADA-ETH', 'SNT-USDT',
        # 'AZY-USDT', 'ENJ-USDT', 'USDT-USDC', 'FIL-BTC', 'VRA-USDT', 'CFX-USDT', 'OKT-USDT', 'UNI-USDT', 'PEPE-USDT',
        # 'XSR-USDT', 'OKT-ETH', 'XCH-USDT', 'TRX-USDC', 'BTM-USDT', 'TURBO-USDT', 'BETH-USDT', 'BTC-DAI', 'TORN-USDT',
        # 'ALGO-BTC', 'OKB-ETH', 'THETA-USDC', 'XPO-USDT', '1INCH-USDT', 'SHIB-USDC', 'ROAD-USDT', 'DOGE-ETH',
        # 'ATOM-OKB', 'ZKS-USDT', 'CFX-USDC', 'NEAR-USDT', 'THETA-USDT', 'HBAR-USDT', '1INCH-USDC', 'FIL-OKB',
        # 'ETH-USDC', 'BTT-USDT', 'ZEC-USDT', 'DEP-USDT', 'AKITA-USDT', 'SAND-ETH', 'USDT-TRY', 'SUSHI-USDT',
        # 'AVAX-USDC', 'LINK-USDC', 'MASK-USDC', 'ICP-ETH', 'MKR-USDT', 'LTC-USDT', 'FLOKI-USDT', 'ETM-USDT', 'CRV-OKB',
        # 'VELA-USDT', 'DMG-USDT', 'CAPO-USDT', 'AVAX-USDT', 'MKR-USDC', 'MASK-USDT', 'LINK-USDT', 'YOYO-USDT',
        # 'RNDR-USDT', 'GLMR-USDT', 'XRP-BTC', 'WIFI-USDT', 'LBR-USDT', 'ZEC-USDC']


    def get_df(self, symbol: str='BTC-USDT', tf: str='5m', limit: str='300') -> pd.DataFrame:
        data = self.market.get_candlesticks(instId=symbol, bar=tf, limit=limit)['data']
        df = self._create_df(data=data)

        return df



    def _create_df(self, data: list) -> pd.DataFrame:
        col = ['Date', 'Open', 'High', 'Low', 'Close', 'VolBase', 'VolQuote']
        df = pd.DataFrame(data=data)
        df.drop(columns=[7, 8], inplace=True)
        df.columns = col
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')
        return df










