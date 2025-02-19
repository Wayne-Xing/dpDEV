import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class USAFutures:
    def __init__(self):
        self.symbol_map = {
            "大豆": "ZS=F",  # 芝加哥商品交易所大豆期货
            "玉米": "ZC=F",
            "小麦": "ZW=F"
        }
    
    def get_realtime_price(self, symbol):
        """获取实时价格"""
        try:
            if symbol not in self.symbol_map:
                raise ValueError(f"不支持的期货品种: {symbol}")
            
            ticker = yf.Ticker(self.symbol_map[symbol])
            data = ticker.history(period='1d')
            return float(data['Close'].iloc[-1])
        except Exception as e:
            print(f"获取实时价格失败: {str(e)}")
            return None

    def get_history_data(self, symbol, start_date, end_date=None):
        """获取历史数据"""
        try:
            if symbol not in self.symbol_map:
                raise ValueError(f"不支持的期货品种: {symbol}")
            
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")
                
            ticker = yf.Ticker(self.symbol_map[symbol])
            data = ticker.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"获取历史数据失败: {str(e)}")
            return None
