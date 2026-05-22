indicator('BRICK', 'Brick Chart', False, '砖型图: 通达信原版, 红柱=上升, 绿柱=下降, 黄点=CC买点')

h4 = high().hhv(4)
l4 = low().llv(4)
c = close()

var1a = (h4 - c) / (h4 - l4) * 100 - 90
var2a = var1a.smma(4, 1) + 100
var3a = (c - l4) / (h4 - l4) * 100
var4a = var3a.smma(6, 1)
var5a = var4a.smma(6, 1) + 100
var6a = var5a - var2a

brick = (var6a > 4) * (var6a - 4)
prev = brick.ref(1)

rising = prev < brick
falling = prev > brick

plot('Brick', brick, Color.red, Line.line, 1)
plot_stickline('UP', rising, prev, brick, 0.8, False, False, Color.red)
plot_stickline('DN', falling, brick, prev, 0.8, False, False, Color.green)

aa = rising
cc = (aa.ref(1) == 0) & (aa == 1)
xg = cc > 0

plot('CC', xg * brick * 1.2, Color.yellow, Line.line, 1)
