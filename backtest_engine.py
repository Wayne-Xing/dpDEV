import pandas as pd
import numpy as np
from datetime import datetime

class Order:
    """订单类"""
    def __init__(self, size, price, type='MKT'):
        self.size = size  # 订单数量
        self.price = price  # 订单价格
        self.type = type  # 订单类型：MKT（市价）或LMT（限价）
        self.status = 'Created'  # 订单状态
        self.executed = None  # 执行细节
        
    def isbuy(self):
        return self.size > 0

class Trade:
    """交易类"""
    def __init__(self, size, price, commission):
        self.size = size
        self.price = price
        self.commission = commission
        self.pnl = 0  # 毛利润
        self.pnlcomm = 0  # 净利润
        self.isclosed = False
        
class BacktestEngine:
    def __init__(self):
        self.data = None  # 回测数据
        self.position = 0  # 当前持仓
        self.cash = 1000000  # 初始资金
        self.commission = 0.0003  # 手续费率
        self.slippage = 0.0001  # 滑点率
        self.trades = []  # 交易记录
        self.equity = []  # 权益曲线
        
    def set_commission(self, commission_rate):
        self.commission = commission_rate
        
    def set_slippage(self, slippage):
        self.slippage = slippage
        
    def match_orders(self, order):
        """订单撮合"""
        if order.type == 'MKT':
            execution_price = self.data['close'].iloc[-1] * (1 + self.slippage * (1 if order.isbuy() else -1))
        else:
            execution_price = order.price
            
        commission = abs(order.size * execution_price * self.commission)
        trade = Trade(order.size, execution_price, commission)
        
        # 更新持仓和现金
        self.position += order.size
        self.cash -= (order.size * execution_price + commission)
        
        # 更新订单状态
        order.status = 'Completed'
        order.executed = trade
        
        self.trades.append(trade)
        return order
        
    def update_equity(self):
        """更新账户权益"""
        current_price = self.data['close'].iloc[-1]
        market_value = self.position * current_price
        equity = self.cash + market_value
        self.equity.append(equity)
        
    def run(self, strategy, data):
        """运行回测"""
        self.data = data
        strategy.data = data
        
        for i in range(len(data)):
            strategy.datetime = data.index[i]
            strategy.price = data['close'].iloc[i]
            strategy.next()
            
            if strategy.order:
                executed_order = self.match_orders(strategy.order)
                strategy.notify_order(executed_order)
                
            self.update_equity()
            
        return pd.Series(self.equity, index=data.index)