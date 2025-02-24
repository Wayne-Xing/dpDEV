from vnpy.trader.engine import MainEngine
from vnpy.trader.object import ContractData
from vnpy.app.data_manager import DataManagerApp  # 数据管理模块[^4]

def get_contract_codes():
    """获取可交易合约列表"""
    main_engine = MainEngine()
    main_engine.add_app(DataManagerApp)  # 添加数据管理应用[^4]
    
    # 从主引擎获取全部合约数据
    contracts = main_engine.get_all_contracts()  # [^4]
    
    # 筛选期货合约并格式化输出
    futures_list = [
        (contract.symbol, contract.exchange.value, contract.name)
        for contract in contracts
        if contract.product == "FUTURES"  # 过滤期货产品[^4]
    ]
    
    print("交易所代码示例：")
    for symbol, exchange, name in futures_list[:5]:
        print(f"{exchange}.{symbol} - {name}")
        
    return futures_list

get_contract_codes()