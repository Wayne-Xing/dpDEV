from datetime import datetime, timedelta
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import HistoryRequest
from vnpy_ctp import CtpGateway  # 修改为正确的CTP网关
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
import pandas as pd
import os

class FuturesDataCollector:
    def __init__(self):
        """初始化数据收集器"""
        # 创建事件引擎
        self.event_engine = EventEngine()
        # 创建主引擎
        self.main_engine = MainEngine(self.event_engine)
        # 添加CTP接口
        self.main_engine.add_gateway(CtpGateway)  # 修改为CtpGateway
        
        # 创建保存目录
        self.data_path = "market_data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def connect_gateway(self):
        """连接到行情网关"""
        setting = {
            "用户名": "",          # SimNow账户
            "密码": "",           # SimNow密码
            "经纪商代码": "9999",
            "交易服务器": "180.168.146.187:10130",  # 电信1
            "行情服务器": "180.168.146.187:10131",   # 电信1
            "产品名称": "simnow_client_test",
            "授权编码": "0000000000000000"
        }
        
        try:
            self.main_engine.connect(setting, "CTP")
            print("CTP接口连接请求发送成功")
            return True
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def get_all_contracts(self):
        """获取所有可用合约"""
        contracts = self.main_engine.get_all_contracts()
        return [contract for contract in contracts if contract.product == "FUTURES"]

    def get_product_info(self, symbol, exchange):
        """获取期货产品信息"""
        contract = self.main_engine.get_contract(symbol, Exchange(exchange))
        if contract:
            return {
                "symbol": contract.symbol,
                "exchange": contract.exchange.value,
                "name": contract.name,
                "product": contract.product,
                "size": contract.size,
                "pricetick": contract.pricetick
            }
        return None

    def get_history_data(self, symbol, exchange, start_date, end_date=None, interval=Interval.DAILY):
        """获取历史数据"""
        if end_date is None:
            end_date = datetime.now()

        req = HistoryRequest(
            symbol=symbol,
            exchange=Exchange(exchange),
            start=datetime.strptime(start_date, "%Y%m%d"),
            end=end_date,
            interval=interval
        )

        data = self.main_engine.query_history(req, "CTP")
        return data

    def save_to_csv(self, data, symbol, interval):
        """保存数据到CSV文件"""
        if not data:
            print(f"没有可用数据: {symbol}")
            return False

        # 转换为DataFrame
        df = pd.DataFrame([
            {
                "datetime": bar.datetime,
                "open": bar.open_price,
                "high": bar.high_price,
                "low": bar.low_price,
                "close": bar.close_price,
                "volume": bar.volume,
                "open_interest": bar.open_interest
            }
            for bar in data
        ])

        # 保存文件
        filename = f"{self.data_path}/{symbol}_{interval.value}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"数据已保存到: {filename}")
        return True

def main():
    """主程序"""
    collector = FuturesDataCollector()
    
    # 连接行情网关
    print("正在连接CTP接口...")
    if not collector.connect_gateway():
        print("连接失败")
        return

    # 等待连接初始化（增加等待时间）
    print("等待连接初始化...")
    import time
    time.sleep(5)  # 增加等待时间到5秒

    try:
        # 获取所有期货合约
        contracts = collector.get_all_contracts()
        if not contracts:
            print("未能获取到合约信息，可能是连接未完全建立")
            return

        print("\n可用期货合约:")
        for contract in contracts[:5]:  # 显示前5个合约
            print(f"{contract.symbol} - {contract.name}")

        # 示例：获取指定合约的历史数据
        symbol = "rb2405"  # 螺纹钢2405合约
        exchange = "SHFE"  # 上海期货交易所
        start_date = "20230101"  # 起始日期

        # 获取产品信息
        product_info = collector.get_product_info(symbol, exchange)
        if product_info:
            print("\n产品信息:")
            for key, value in product_info.items():
                print(f"{key}: {value}")

        # 获取并保存历史数据
        print(f"\n获取 {symbol} 的历史数据...")
        data = collector.get_history_data(symbol, exchange, start_date)
        if data:
            collector.save_to_csv(data, symbol, Interval.DAILY)
        else:
            print("未获取到历史数据")

    except Exception as e:
        print(f"运行过程中出现错误: {str(e)}")
    
    finally:
        # 关闭连接
        print("\n正在关闭连接...")
        collector.main_engine.close()
        print("程序结束")

if __name__ == "__main__":
    main()
