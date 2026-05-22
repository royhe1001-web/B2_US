#!/usr/bin/env python3
"""B2 Spring US — 美股版回测入口"""
import sys, os, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd, numpy as np
import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s [%(levelname)s] %(message)s')

BASE = os.path.dirname(os.path.abspath(__file__))
FEAT_DIR = os.path.join(BASE, 'ML_optimization', 'features_4h')

# ============================================================
# 美股版参数 (与A股B2策略对齐)
# ============================================================
BEST_B2 = {
    'j_prev_max': 20, 'gain_min': 0.04, 'j_today_max': 65,
    'shadow_max': 0.035, 'j_today_loose': 70, 'shadow_loose': 0.045,
    'prior_strong_ret': 0.20,
    'weight_gain_2x_thresh': 0.0842, 'weight_gain_2x': 1.479,
    'weight_gap_thresh': 0.02, 'weight_gap_up': 1.5,
    'weight_shrink': 1.171, 'weight_deep_shrink_ratio': 0.80,
    'weight_deep_shrink': 1.3, 'weight_pullback_thresh': -0.05,
    'weight_pullback': 1.2, 'weight_shadow_discount_thresh': 0.015,
    'weight_shadow_discount': 0.7, 'weight_strong_discount': 0.8,
    'weight_brick_resonance': 1.5,
    'sector_momentum_enabled': False,
    'dynamic_thresholds': False, 'trend_filter': False,
    'rotate_base': 0.5,
    'vol_check_days': 5, 'vol_spike_thresh': 1.954,
    'sig_expire_thresh': 0.973, 'max_signal_days': 14,
}

# 美股无OAMV - 用虚拟OAMV (始终normal)
BEST_OAMV = {
    'oamv_aggressive_threshold': 999, 'oamv_defensive_threshold': -999,
    'max_positions': 2,
}


def load_all(test_start, test_end):
    print('=' * 70)
    print(f'  B2 Spring US — {test_start.date()} ~ {test_end.date()}')
    print('=' * 70)

    # Load all parquet files
    stock_data = {}
    files = sorted([f for f in os.listdir(FEAT_DIR) if f.endswith('.parquet')])
    for f in files:
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
    print(f'  Loaded {len(stock_data)} stocks')

    # Create dummy OAMV dataframe
    dates = pd.date_range(test_start - pd.Timedelta(days=365), test_end, freq='B')
    oamv_df = pd.DataFrame({
        'date': dates,
        'oamv': 1.0, 'oamv_change_pct': 0.0,
        'oamv_cyc5': 1.0, 'oamv_cyc13': 1.0,
    })

    return stock_data, oamv_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=str, default=None)
    parser.add_argument('--end', type=str, default=None)
    args = parser.parse_args()

    today = pd.Timestamp.now()
    test_start = pd.Timestamp(args.start) if args.start else pd.Timestamp(f'{today.year}-01-01')
    test_end = pd.Timestamp(args.end) if args.end else today

    stock_data, oamv_df = load_all(test_start, test_end)

    # Import engine
    from ML_optimization.phase2c_oamv_grid_search import OAMVSimEngine
    import ML_optimization.phase2c_oamv_grid_search as p2c_mod
    p2c_mod.SIM_START = test_start
    p2c_mod.SIM_END = test_end

    print(f'\n{"="*70}')
    print(f'  B2 Spring US')
    print(f'{"="*70}')

    t0 = time.time()
    engine = OAMVSimEngine(stock_data, BEST_B2, oamv_df, BEST_OAMV)
    m = engine.run()
    elapsed = time.time() - t0

    print(f'\n  Return={m["total_return_pct"]:+.1f}%  '
          f'Sharpe={m["sharpe"]:.3f}  WR={m["win_rate"]:.1%}  '
          f'Trades={m["n_trades"]}  MaxDD={m["max_dd"]:.1%}  '
          f'({elapsed:.0f}s)')

    print()


if __name__ == '__main__':
    main()
