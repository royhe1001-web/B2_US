#!/usr/bin/env python3
"""B2 US — 上升趋势中抄底策略 (EMA19>EMA53 + J超卖 + 未破EMA53支撑)"""
import numpy as np, pandas as pd

def generate_us_signals(df: pd.DataFrame, params: dict = None) -> pd.DataFrame:
    """
    入场条件 (4条件AND):
      1. J < j_max (默认20) — 超卖
      2. EMA19 > EMA53 — 上升趋势中
      3. close > EMA53 — 未破长期支撑
      4. 上影线 < 振幅1/4 — 阳线质量
    """
    from indicators import calc_all_indicators
    if 'J' not in df.columns:
        df = calc_all_indicators(df, board_type='main')

    p = params or {}
    j_max = p.get('j_max', 20)

    c1 = df['J'] < j_max
    c2 = df['white_line'] > df['yellow_line']        # 白>黄 (短期资金进场)
    c3 = df['close'] > df['yellow_line']             # 收>黄 (股价站上支撑)
    upper_shadow = (df['high'] - df['close']) / (df['high'] - df['low']).replace(0, np.nan)
    c4 = upper_shadow < 0.25

    entry = c1 & c2 & c3 & c4
    df['b2_entry_signal'] = entry.astype(int)
    df['b2_position_weight'] = 1.0

    gain = df['close'] / df['close'].shift(1) - 1
    if p.get('weight_gain_2x_thresh'):
        df.loc[gain > p['weight_gain_2x_thresh'], 'b2_position_weight'] *= p.get('weight_gain_2x', 1.5)

    # 跳空高开加成 (gap > 2% -> x1.5)
    gap = df['open'] / df['close'].shift(1) - 1
    gap_up = gap > p.get('weight_gap_thresh', 0.02)
    df.loc[gap_up, 'b2_position_weight'] *= p.get('weight_gap_up', 1.5)

    df['b2_position_weight'] = df['b2_position_weight'].clip(upper=5.0)
    df['b2_state'] = 'wait'
    return df


def generate_spring_signals(df: pd.DataFrame, board_type: str = 'main',
                             precomputed: bool = False, params: dict = None) -> pd.DataFrame:
    return generate_us_signals(df, params)

generate_spring_entry_only = generate_spring_signals
