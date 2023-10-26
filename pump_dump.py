

import conf
import classes





pairs = classes.pairs(type='SPOT')

pair = 'CSPR-USDT'

candles = classes.candles(pair=pair, tf='15m')

df = classes.frame(data=candles)

classes.detect_accumulation(df=df)






