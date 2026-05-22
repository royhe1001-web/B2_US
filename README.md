# B2 US — 美股上升趋势抄底策略

在标普500和纳斯达克中寻找"上升趋势中回调至超卖区"的抄底机会。

## 回测结果

| 窗口 | 收益 | Sharpe | 胜率 | 最大回撤 |
|------|------|--------|------|----------|
| 2026 YTD (01-01 ~ 05-22) | +82.9% | 3.263 | 66.1% | -3.0% |

## 策略逻辑

与A股B2策略的"爆发放量反弹"思路不同，美股版采用"提前抄底"逻辑：

### 入场 (4条件AND)
1. J < 20 — KDJ超卖
2. 白线 > 黄线 — 短期资金已进场
3. 收盘 > 黄线 — 股价站上中期支撑
4. 上影线 < 振幅1/4 — 阳线质量过滤

### 离场 (5条优先级)
1. **take_half**: +10% 卖一半锁利润
2. **white_line**: 跌破白线 (截损/牵牛)
3. **yellow_line**: 跌破黄线 (趋势破坏)
4. **candle**: 跌破买入日最低价
5. **time_stop**: 持仓4天不涨

### 与A股版的区别

| | A股 B2 | 美股 B2 US |
|------|--------|------------|
| 入场逻辑 | 超卖后放量反弹确认 (Spring) | 上升趋势中超卖抄底 |
| 涨幅要求 | >4% | 无 |
| 放量要求 | volume > 前日 | 无 |
| 趋势确认 | MA20 | 白黄线 |
| 市值过滤 | P50-P96 | 无 (全量标普500+纳指) |
| OAMV | 有 | 无 |
| 选股池 | ~2200只主板 | ~560只标普500+纳指+热门赛道 |

## 项目结构

```
├── run_backtest_us.py          # 回测入口
├── strategy_us.py              # 美股信号引擎
├── strategy_spring.py          # A股信号引擎(备用)
├── indicators.py               # 技术指标
├── close_sell_check.py         # 收盘卖出检测
├── oamv.py                     # 活筹指数(美股禁用)
└── ML_optimization/
    ├── phase2c_oamv_grid_search.py  # 仿真引擎
    ├── phase2c_bull_grid_search.py  # 数据加载
    └── mktcap_utils.py              # 市值过滤
```

## 使用方法

```bash
# 下载数据 (需要代理)
python download_sp500.py

# 计算指标
python -c "from indicators import calc_all_indicators; ..."

# 运行回测
python run_backtest_us.py
```

## 免责声明
仅供学术研究，不构成投资建议。历史回测不代表未来收益。
