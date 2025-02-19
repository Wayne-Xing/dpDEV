from qh_cn import ChinaFutures
from qh_usa import USAFutures
from datetime import datetime, timedelta

def main():
    cf = ChinaFutures()
    us_futures = USAFutures()
    
    # 测试实时价格获取
    price = cf.get_realtime_price("豆粕")
    print(f"豆粕实时价格: {price}")
    print("美国大豆实时价格:", us_futures.get_realtime_price("大豆"))
    
    # 测试历史数据获取
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    cn_history = cf.get_history_data("豆粕", start_date)
    us_history = us_futures.get_history_data("大豆", start_date)
    
    print("\n国内豆粕历史数据:")
    print(cn_history.head())
    print("\n美国大豆历史数据:")
    print(us_history.head())

if __name__ == "__main__":
    main()
