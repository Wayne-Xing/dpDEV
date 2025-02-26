import akshare as ak
import pandas as pd

class DataFetcher:
    def __init__(self):
        self.data = None

    def fetch_dometic_info(self, product):
        """获取国内期货信息"""
        symbol_map = ak.futures_symbol_mark() 
        return(symbol_map[symbol_map["symbol"].str.contains(product)]["symbol"].values[0])
        pass

    def fetch_foreign_info(self, product):
        """获取外盘期货信息"""
        symbol_map = ak.futures_hq_subscribe_exchange_symbol()
        return(symbol_map[symbol_map["symbol"]=="CBOT-黄豆"]["code"].values[0])
        pass

    def fetch_domestic_data_cur(self, symbol):
        """获取实时国内期货数据"""
        data = ak.futures_zh_realtime(symbol=symbol)
        return data
        pass

    def fetch_domestic_data_his(self, symbol, period='daily', start_date='', end_date=''):
        """获取历史国内期货数据
        Args:
            symbol: 期货代码
            period: 数据周期，默认为'daily'
            start_date: 开始日期，默认为空
            end_date: 结束日期，默认为空
        """
        if not period:
            period = 'daily'
        
        if start_date and end_date:
            data = ak.futures_hist_em(symbol=symbol+'主连', period=period, start_date=start_date, end_date=end_date)
        else:
            data = ak.futures_hist_em(symbol=symbol+'主连', period=period)
        return data
        pass

    def fetch_foreign_data_cur(self, symbol):
        """获取实时外盘期货数据"""
        data = ak.futures_foreign_commodity_realtime(symbol)
        return data
        pass

    def fetch_foreign_data_his(self, symbol):
        """获取历史外盘期货数据"""
        futures_foreign_hist_df = ak.futures_foreign_hist(symbol=symbol)
        return(futures_foreign_hist_df)

        pass

    def process_data(self, data):
        """数据预处理"""
        pass

