#!/usr/bin/env python3
"""Brick US 4h — 砖型图CC信号 + 白黄线趋势过滤"""
import numpy as np, pandas as pd

def generate_spring_signals(df, board_type='main', precomputed=False, params=None):
    p = params or {}
    if 'J' not in df.columns:
        from indicators import calc_all_indicators
        df = calc_all_indicators(df, board_type='main')

    # Entry: white > yellow (trend up) AND brick CC signal (green-to-red)
    trend_up = df['white_line'] > df['yellow_line']
    cc = df.get('brick_green_to_red', pd.Series(0, index=df.index))

    entry = trend_up & (cc == 1)
    df['b2_entry_signal'] = entry.astype(int)

    # Weight: brick value as signal strength
    brick_val = df.get('brick_val', pd.Series(0, index=df.index))
    df['b2_position_weight'] = (1.0 + brick_val / brick_val.max() * 2.0).fillna(1.0).clip(1.0, 5.0)

    df['b2_state'] = 'wait'
    return df

generate_spring_entry_only = generate_spring_signals
