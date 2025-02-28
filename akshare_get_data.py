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

cb_file = '总种植成本.csv'
dc_file = '美国大豆单产调整表.csv'

# 读取CSV文件
df_cb = data_fetcher.process_csv(cb_file)
df_dc = data_fetcher.process_csv(dc_file)

print("\n=== 原始成本数据 ===")
print(df_cb)
print("\n=== 原始单产数据 ===")
print(df_dc)

# 获取年份列表（假设在df_dc的'USDA报告年份'行中）
years = df_dc.columns

# 创建结果DataFrame
df_final = pd.DataFrame(index=df_dc.index)

# 对每一年进行计算
for year in years:
    try:
        # 使用第一列数据除以对应年份的数据
        df_final[year] = (df_cb[year].iloc[0] / df_dc[year]).round(2)  # 添加round(2)保留两位小数
    except Exception as e:
        print(f"处理{year}年数据时出错: {str(e)}")
        df_final[year] = None  # 如果计算出错，填充为空值

print("\n=== 计算结果（单产/成本比率）===")
print(df_final)

# 可选：如果需要保存结果到文件
# df_final.to_csv('计算结果.csv', float_format='%.2f')  # 保存时也保留两位小数
