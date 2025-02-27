from data_layer import DataFetcher
from strategy_layer import StrategyBase, StrategyContainer
from backtest_engine import BacktestEngine
from performance_analysis import PerformanceAnalyzer
import pandas as pd
#豆粕ETF数据获取

# 1. 初始化各个模块
data_fetcher = DataFetcher()
backtest_engine = BacktestEngine()
strategy_container = StrategyContainer()
performance_analyzer = PerformanceAnalyzer()

# 2. 获取数据
# 外盘settings
f_product = "CBOT-黄豆"  # 交易品种
f_start_date = "2023-01-01"
f_end_date = "2024-01-01"
# 内盘settings
d_product = "豆粕"  # 交易品种
d_period = ""  # 数据周期 period="daily"; choice of {"daily", "weekly", "monthly"}
d_start_date = ""
d_end_date = ""   


# 获取外盘期货信息  
f_symbol = data_fetcher.fetch_foreign_info(f_product)

# 获取外盘历史数据
foreign_data_his = data_fetcher.fetch_foreign_data_his(
    symbol=f_symbol
)
if not isinstance(foreign_data_his, pd.DataFrame):
    foreign_data_his = pd.DataFrame([foreign_data_his])

# 将date列转换为datetime类型
foreign_data_his['date'] = pd.to_datetime(foreign_data_his['date'])

# 筛选每月月初数据
monthly_data = foreign_data_his.set_index('date').resample('MS').first().reset_index()

print("\n=== %s 外盘期货历史行情（每月月初）==="%f_product)
print(monthly_data.head())  # 显示前5行月初数据