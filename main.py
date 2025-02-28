from data_layer import DataFetcher
from strategy_layer import StrategyBase, StrategyContainer
from backtest_engine import BacktestEngine
from performance_analysis import PerformanceAnalyzer
import pandas as pd

class SimpleStrategy(StrategyBase):
    def generate_signals(self, data):
        """
        简单策略示例：当价格上涨时买入，下跌时卖出
        """
        signals = []
        close_prices = data['close']
        for i in range(1, len(close_prices)):
            if close_prices[i] > close_prices[i-1]:
                signals.append(1)  # 买入信号
            elif close_prices[i] < close_prices[i-1]:
                signals.append(-1)  # 卖出信号
            else:
                signals.append(0)  # 持仓不变
        return signals

def main():

    # 设置pandas显示选项
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', None)        # 显示宽度设置
    pd.set_option('display.max_rows', 20)       # 最多显示20行
    pd.set_option('display.float_format', lambda x: '%.2f' % x)  # 浮点数格式化为2位小数
    pd.set_option('display.max_colwidth', None)  # 设置列宽为无限制
    pd.set_option('display.expand_frame_repr', False)  # 禁止跨行显示
    pd.set_option('display.max_seq_items', None)  # 显示所有序列项
    
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
    # print(symbol)

    # 获取外盘期货数据
    foreign_data_cur = data_fetcher.fetch_foreign_data_cur(
        symbol=f_symbol
    )
    if not isinstance(foreign_data_cur, pd.DataFrame):
        foreign_data_cur = pd.DataFrame([foreign_data_cur])
    
    print("\n=== %s 外盘期货实时行情 ==="%f_product)
    print(data_fetcher.process_data(foreign_data_cur,'cur'))  # 不显示索引

    # 获取外盘历史数据
    foreign_data_his = data_fetcher.fetch_foreign_data_his(
        symbol=f_symbol
    )
    if not isinstance(foreign_data_his, pd.DataFrame):
        foreign_data_his = pd.DataFrame([foreign_data_his])
    
    # 将date列转换为datetime类型
    foreign_data_his['date'] = pd.to_datetime(foreign_data_his['date'])

    # 筛选每月月初数据
    foreign_data_his_monthly = foreign_data_his.set_index('date').resample('MS').first().reset_index()

    print("\n=== %s 外盘期货历史行情（每月月初）==="%f_product)
    # 将DataFrame转换为字符串并打印
    with pd.option_context('display.max_rows', None, 
                          'display.max_columns', None,
                          'display.width', None):
        print(data_fetcher.process_data(foreign_data_his_monthly,'his').tail(24).to_string())

    print("\n=== %s 外盘期货历史行情 ==="%f_product)
    print(foreign_data_his.tail(30))  # 不显示索引


    # 获取国内期货信息
    d_symbol = data_fetcher.fetch_dometic_info(d_product)
    # 获取实时国内期货数据
    domestic_data_cur = data_fetcher.fetch_domestic_data_cur(
        symbol=d_symbol
    )
    if not isinstance(domestic_data_cur, pd.DataFrame):
        domestic_data_cur = pd.DataFrame([domestic_data_cur])
    
    print("\n=== %s 国内期货实时行情 ==="%d_product)
    print(data_fetcher.process_data(domestic_data_cur,'cur'))  # 不显示索引

    # 获取历史国内期货数据
    domestic_data_his = data_fetcher.fetch_domestic_data_his(
        symbol=d_symbol,
        period=d_period,
        start_date=d_start_date,
        end_date=d_end_date
    )
    if not isinstance(domestic_data_his, pd.DataFrame):
        domestic_data_his = pd.DataFrame([domestic_data_his])
    
    print("\n=== %s主连 国内期货历史行情 ==="%d_product)
    print(data_fetcher.process_data(domestic_data_his,'his').tail(20))  # 不显示索引


    # 处理美豆种植成本数据
    cost_data = data_fetcher.process_csv("美豆种植成本数据.xlsx")
    if cost_data is not None:
        print("\n=== 美豆种植成本数据 ===")
        print(cost_data)

    # 处理美国大豆单产调整表数据
    yield_data = data_fetcher.process_csv("美国大豆单产调整表.csv")
    if yield_data is not None:
        print("\n=== 美国大豆单产调整数据 ===")
        print(yield_data.to_string())  # 使用to_string()方法显示完整数据

    # 3. 设置回测参数
    backtest_engine.set_commission(0.0003)  # 设置手续费率
    backtest_engine.set_slippage(0.0001)    # 设置滑点率
    backtest_engine.load_data(historical_data)

    # 4. 添加策略
    strategy = SimpleStrategy()

if __name__ == "__main__":
    main()