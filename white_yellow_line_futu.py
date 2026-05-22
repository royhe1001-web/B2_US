indicator('WHITE', 'White & Yellow Line', True, '白黄线: 白线=EMA(EMA(C,10),10), 黄线=(MA14+MA28+MA57+MA114)/4')

white = close().ema(10).ema(10)
yellow = (close().sma(14) + close().sma(28) + close().sma(57) + close().sma(114)) / 4

plot('White', white, Color.white, Line.line, 2)
plot('Yellow', yellow, Color.yellow, Line.line, 2)
