#!/usr/bin/env python3
"""B2 US 4h Brick 回测 — 砖型CC + 白>黄"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd, numpy as np
import logging
logging.basicConfig(level=logging.WARNING)

BASE = os.path.dirname(os.path.abspath(__file__))
FEAT_DIR = os.path.join(BASE, 'ML_optimization', 'features_4h')

BEST_B2 = {
    'j_prev_max': 20, 'j_today_max': 65, 'shadow_max': 0.035,
    'j_today_loose': 70, 'shadow_loose': 0.045, 'prior_strong_ret': 0.20,
    'weight_gain_2x_thresh': 0.0842, 'weight_gain_2x': 1.479,
    'weight_gap_thresh': 0.02, 'weight_gap_up': 1.5,
    'sector_momentum_enabled': False, 'dynamic_thresholds': False,
    'trend_filter': False, 'rotate_base': 0.5,
}

BEST_OAMV = {
    'oamv_aggressive_threshold': 999, 'oamv_defensive_threshold': -999,
    'max_positions': 3,
}


def main():
    today = pd.Timestamp.now()
    test_start = pd.Timestamp('2026-01-01')
    test_end = today

    # Load 4h data
    stock_data = {}
    for f in sorted(os.listdir(FEAT_DIR)):
        if not f.endswith('.parquet'): continue
        sym = f.replace('.parquet', '')
        try:
            df = pd.read_parquet(os.path.join(FEAT_DIR, f))
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date').sort_index()
            if len(df) >= 120:
                stock_data[sym] = df
        except Exception:
            pass
    print(f'Loaded {len(stock_data)} stocks')

    # Dummy OAMV
    dates = pd.date_range(test_start - pd.Timedelta(days=365), test_end, freq='4h')
    oamv_df = pd.DataFrame({'date': dates, 'oamv': 1.0, 'oamv_change_pct': 0.0, 'oamv_cyc5': 1.0, 'oamv_cyc13': 1.0})

    # Switch engine to use brick strategy
    from strategy_brick_4h import generate_spring_signals as brick_gen
    import ML_optimization.phase2c_oamv_grid_search as eng
    eng.generate_spring_signals = brick_gen

    import ML_optimization.phase2c_oamv_grid_search as p2c_mod
    p2c_mod.SIM_START = test_start
    p2c_mod.SIM_END = test_end

    print(f'B2 US 4h Brick — {test_start.date()} ~ {test_end.date()}')
    t0 = time.time()
    engine = eng.OAMVSimEngine(stock_data, BEST_B2, oamv_df, BEST_OAMV)
    m = engine.run()
    elapsed = time.time() - t0

    print(f'Return={m["total_return_pct"]:+.1f}%  Sharpe={m["sharpe"]:.3f}  WR={m["win_rate"]:.1%}  Trades={m["n_trades"]}  MaxDD={m["max_dd"]:.1%}  ({elapsed:.0f}s)')


if __name__ == '__main__':
    main()
