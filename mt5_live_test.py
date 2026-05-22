#!/usr/bin/env python3
"""MT5 连接测试 — 检查能否连上 TMGM MT5 终端"""
import MetaTrader5 as mt5
import sys

def main():
    print("=" * 50)
    print("MT5 连接测试")
    print("=" * 50)

    # 1. 检查 MT5 包版本
    print(f"\nMetaTrader5 包版本: {mt5.__version__}")

    # 2. 初始化 MT5 连接（指定 TMGM MT5 路径）
    mt5_path = r"D:\知行合一量化\tmgm mt5\terminal64.exe"
    print(f"\n正在连接 MT5 终端 ({mt5_path})...")
    if not mt5.initialize(path=mt5_path):
        print(f"连接失败! 错误: {mt5.last_error()}")
        print("\n请确保:")
        print("  1. MT5 终端已启动并登录 TMGM 账户")
        print("  2. MT5 中已开启 '工具 → 选项 → 智能交易系统 → 允许自动化交易'")
        print("  3. 勾选 '允许 WebRequest'")
        sys.exit(1)

    print("连接成功!")

    # 3. 显示 MT5 版本和账户信息
    info = mt5.terminal_info()
    if info:
        print(f"\nMT5 终端信息:")
        print(f"  路径: {info.path}")
        print(f"  版本: {info.build}")
        print(f"  已连接服务器: {info.connected}")
        print(f"  社区账户: {info.community_account}")

    account = mt5.account_info()
    if account:
        print(f"\n账户信息:")
        print(f"  登录号: {account.login}")
        print(f"  服务器: {account.server}")
        print(f"  账户类型: {'模拟' if account.trade_mode == 0 else '真实'}")
        print(f"  杠杆: 1:{account.leverage}")
        print(f"  余额: {account.balance:.2f}")
        print(f"  净值: {account.equity:.2f}")
        print(f"  币种: {account.currency}")

    # 4. 列出可用品种 (前20个)
    symbols = mt5.symbols_get()
    if symbols:
        print(f"\n可用品种总数: {len(symbols)}")
        print("前20个品种:")
        for s in symbols[:20]:
            print(f"  {s.name}")

    # 5. 测试获取行情
    print("\n测试行情获取 (XAUUSD):")
    tick = mt5.symbol_info_tick("XAUUSD")
    if tick:
        print(f"  Bid: {tick.bid}, Ask: {tick.ask}, Time: {tick.time}")
    else:
        print(f"  获取失败: {mt5.last_error()}")

    # 6. 测试获取K线
    print("\n测试K线获取 (XAUUSD, M5, 最近10根):")
    rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_M5, 0, 10)
    if rates is not None:
        for r in rates:
            print(f"  {r[0]} | O:{r[1]:.2f} H:{r[2]:.2f} L:{r[3]:.2f} C:{r[4]:.2f} V:{r[5]}")
    else:
        print(f"  获取失败: {mt5.last_error()}")

    print("\n" + "=" * 50)
    print("测试完成 — MT5 连接正常!")
    print("=" * 50)

    mt5.shutdown()

if __name__ == "__main__":
    main()
