from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy_ctp import CtpGateway  # CTP交易接口[^5][^6]
from vnpy.trader.object import SubscribeRequest
from vnpy.trader.constant import Exchange

def main():
    """主程序入口"""
    # 创建Qt应用对象[^3][^6]
    qapp = create_qapp()
    
    # 创建事件引擎
    event_engine = EventEngine()
    
    # 创建主引擎
    main_engine = MainEngine(event_engine)
    
    # 添加CTP接口[^5]
    main_engine.add_gateway(CtpGateway)
    
    # 设置CTP连接参数（需替换为实际账号）
    setting = {
        "用户名": "your_username",
        "密码": "your_password",
        "经纪商代码": "your_broker_id",
        "交易服务器": "tcp://180.168.146.187:10201",
        "行情服务器": "tcp://180.168.146.187:10211",
        "产品名称": "simnow_client_test",
        "授权编码": "0000000000000000"
    }
    
    # 连接到CTP接口
    main_engine.connect(setting, "CTP")
    
    # 创建主窗口
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    
    # 订阅示例合约（沪银主力）
    req = SubscribeRequest(
        symbol="ag2408",
        exchange=Exchange.SHFE
    )
    main_engine.subscribe(req, "CTP")
    
    # 启动事件循环
    qapp.exec()

if __name__ == "__main__":
    main()
