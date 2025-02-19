from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData, TickData
from vnpy.trader.utility import get_trading_date
from datetime import datetime, timedelta
import pandas as pd
import time

class ChinaFutures:
    def __init__(self):
        """初始化期货数据接口"""
        self.symbol_map = {
            "豆粕": ("M", Exchange.DCE),    # 大连商品交易所
            "豆油": ("Y", Exchange.DCE),
            "大豆": ("A", Exchange.DCE),
            "玉米": ("C", Exchange.DCE),
            "沪铜": ("CU", Exchange.SHFE),  # 上海期货交易所
            "沪铝": ("AL", Exchange.SHFE),
            "黄金": ("AU", Exchange.SHFE)
        }
        
        self._cache = {}
        self._cache_timeout = 60
        self.database = get_database()  # 初始化数据库连接

    def get_product_id(self, symbol, date=None):
        """
        获取期货产品ID
        :param symbol: 期货品种名称
        :param date: 指定日期，默认为当前日期
        :return: 主力合约ID
        """
        try:
            if symbol not in self.symbol_map:
                raise ValueError(f"不支持的期货品种: {symbol}")
            
            code, exchange = self.symbol_map[symbol]
            if date is None:
                date = datetime.now()

            # 获取所有可用合约
            contracts = self.database.get_contracts(exchange)
            valid_contracts = []
            
            # 筛选指定品种的合约
            for contract in contracts:
                if contract.symbol.startswith(code):
                    valid_contracts.append(contract)
            
            if not valid_contracts:
                return None

            # 按成交量排序获取主力合约
            main_contract = sorted(
                valid_contracts,
                key=lambda x: x.volume,
                reverse=True
            )[0]
            
            return main_contract.vt_symbol
            
        except Exception as e:
            print(f"获取期货产品ID失败: {str(e)}")
            return None

    def get_realtime_price(self, symbol):
        """获取实时价格"""
        try:
            # 检查缓存
            cache_key = f"realtime_{symbol}"
            if cache_key in self._cache:
                cache_time, cache_data = self._cache[cache_key]
                if time.time() - cache_time < self._cache_timeout:
                    return cache_data

            # 获取主力合约ID
            contract_id = self.get_product_id(symbol)
            if not contract_id:
                return None

            # 获取最新tick数据
            tick: TickData = self.database.get_tick(
                contract_id,
                get_trading_date(),
                Exchange.DCE
            )
            
            if tick:
                price = tick.last_price
                self._cache[cache_key] = (time.time(), price)
                return price
            
            return None
            
        except Exception as e:
            print(f"获取实时价格失败: {str(e)}")
            return None

    def get_history_data(self, symbol, start_date, end_date=None):
        """获取历史数据"""
        try:
            # 获取主力合约ID
            contract_id = self.get_product_id(symbol)
            if not contract_id:
                return None

            # 处理日期
            start = pd.to_datetime(start_date)
            if end_date is None:
                end = datetime.now()
            else:
                end = pd.to_datetime(end_date)

            # 获取K线数据
            bars = self.database.load_bar_data(
                symbol=contract_id,
                exchange=Exchange.DCE,
                interval=Interval.DAILY,
                start=start,
                end=end
            )
            
            if not bars:
                return None

            # 转换为DataFrame
            data = {
                "open": [],
                "high": [],
                "low": [],
                "close": [],
                "volume": [],
                "datetime": []
            }
            
            for bar in bars:
                data["datetime"].append(bar.datetime)
                data["open"].append(bar.open_price)
                data["high"].append(bar.high_price)
                data["low"].append(bar.low_price)
                data["close"].append(bar.close_price)
                data["volume"].append(bar.volume)
            
            df = pd.DataFrame(data)
            df.set_index("datetime", inplace=True)
            return df
            
        except Exception as e:
            print(f"获取历史数据失败: {str(e)}")
            return None

    def get_available_symbols(self):
        """获取所有可用的期货品种"""
        return list(self.symbol_map.keys())

    def clear_cache(self):
        """清除缓存"""
        self._cache = {}
