from qh_cn import ChinaFutures
from qh_usa import USAFutures
from datetime import datetime, timedelta
import argparse
import sys
import pandas as pd

def test_china_futures(symbol="豆粕", days=30):
    """测试国内期货数据获取"""
    print("\n=== 测试国内期货数据 ===")
    try:
        cf = ChinaFutures()
        
        # 测试获取期货产品ID
        product_id = cf.get_product_id(symbol)
        print(f"\n1. {symbol}主力合约ID: {product_id}")
        if not product_id:
            print("警告: 无法获取主力合约ID")
            
        # 测试实时价格获取
        price = cf.get_realtime_price(symbol)
        print(f"\n2. {symbol}实时价格: {price}")
        if not price:
            print("警告: 无法获取实时价格")
            
        # 测试历史数据获取
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        history = cf.get_history_data(symbol, start_date)
        print(f"\n3. {symbol}历史数据(最近{days}天):")
        if isinstance(history, pd.DataFrame) and not history.empty:
            print(history.head())
            print(f"\n数据统计:")
            print(history.describe())
        else:
            print("警告: 无法获取历史数据")
            
        # 测试可用品种获取
        symbols = cf.get_available_symbols()
        print(f"\n4. 可用期货品种: {', '.join(symbols)}")
        
        return True
        
    except Exception as e:
        print(f"测试国内期货数据时发生错误: {str(e)}")
        return False

def test_usa_futures(symbol="大豆", days=30):
    """测试美国期货数据获取"""
    print("\n=== 测试美国期货数据 ===")
    try:
        us = USAFutures()
        
        # 测试实时价格获取
        price = us.get_realtime_price(symbol)
        print(f"\n1. {symbol}实时价格: {price}")
        if not price:
            print("警告: 无法获取实时价格")
            
        # 测试历史数据获取
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        history = us.get_history_data(symbol, start_date)
        print(f"\n2. {symbol}历史数据(最近{days}天):")
        if isinstance(history, pd.DataFrame) and not history.empty:
            print(history.head())
            print(f"\n数据统计:")
            print(history.describe())
        else:
            print("警告: 无法获取历史数据")
            
        return True
        
    except Exception as e:
        print(f"测试美国期货数据时发生错误: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='期货数据获取测试工具')
    parser.add_argument('--cn-symbol', type=str, default="豆粕", help='国内期货品种(默认:豆粕)')
    parser.add_argument('--us-symbol', type=str, default="大豆", help='美国期货品种(默认:大豆)')
    parser.add_argument('--days', type=int, default=30, help='历史数据天数(默认:30)')
    parser.add_argument('--test-cn', action='store_true', help='测试国内期货数据')
    parser.add_argument('--test-us', action='store_true', help='测试美国期货数据')
    
    args = parser.parse_args()
    
    # 如果没有指定具体测试，则全部测试
    if not (args.test_cn or args.test_us):
        args.test_cn = args.test_us = True
    
    success = True
    
    if args.test_cn:
        if not test_china_futures(args.cn_symbol, args.days):
            success = False
            
    if args.test_us:
        if not test_usa_futures(args.us_symbol, args.days):
            success = False
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    print("期货数据获取测试工具")
    print("使用说明:")
    print("1. 测试所有功能:")
    print("   python dp_test.py")
    print("2. 仅测试国内期货:")
    print("   python dp_test.py --test-cn")
    print("3. 仅测试美国期货:")
    print("   python dp_test.py --test-us")
    print("4. 指定期货品种和时间范围:")
    print("   python dp_test.py --cn-symbol 豆粕 --us-symbol 大豆 --days 60")
    print("\n开始测试...\n")
    
    main()
