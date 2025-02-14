import akshare as ak
from datetime import datetime
import pandas as pd

class SoybeanMealData:
    """
    豆粕数据获取类
    """
    def __init__(self):
        # 大连商品交易所豆粕期货代码
        self.symbol = "m"
    
    def get_realtime_price(self):
        """
        获取豆粕期货实时价格
        返回: pandas.DataFrame 包含实时行情数据
        """
        try:
            # 获取豆粕期货实时行情数据
            df = ak.futures_zh_spot(symbol=self.symbol, market="DCE")
            return df
        except Exception as e:
            print(f"获取实时价格时发生错误: {str(e)}")
            return None

    def get_historical_data(self, symbol: str, start_date: str, end_date: str = None):
        """
        获取豆粕期货历史数据
        
        参数:
            symbol: str, 合约代码，例如 'm2405' 表示24年5月豆粕期货
            start_date: str, 开始日期，格式 YYYYMMDD
            end_date: str, 结束日期，格式 YYYYMMDD，默认为当前日期
            
        返回:
            pandas.DataFrame 包含历史价格数据
        """
        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
                
            # 获取大连商品交易所豆粕期货历史数据
            df = ak.futures_main_sina(symbol=symbol, start_date=start_date, end_date=end_date)
            return df
        except Exception as e:
            print(f"获取历史数据时发生错误: {str(e)}")
            return None

    def get_main_contract_price(self):
        """
        获取豆粕期货主力合约价格
        返回: pandas.DataFrame 包含主力合约价格数据
        """
        try:
            # 获取豆粕期货主力合约数据
            df = ak.futures_main_sina(symbol="M0")
            return df
        except Exception as e:
            print(f"获取主力合约价格时发生错误: {str(e)}")
            return None

def example_usage():
    """
    使用示例
    """
    sm = SoybeanMealData()
    
    # 获取实时价格
    print("实时价格:")
    print(sm.get_realtime_price())
    
    # 获取历史数据 (以m2405为例)
    print("\n历史数据:")
    historical_data = sm.get_historical_data('m2405', '20230101')
    print(historical_data)
    
    # 获取主力合约价格
    print("\n主力合约价格:")
    print(sm.get_main_contract_price())

if __name__ == "__main__":
    example_usage() 