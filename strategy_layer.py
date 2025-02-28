import pandas as pd
import numpy as np
from datetime import datetime

class StrategyBase:
    """策略基类"""
    def __init__(self):
        self.position = 0  # 当前持仓
        self.params = dict()  # 策略参数
        self.data = None  # 数据
        self.order = None  # 当前订单
        self.price = None  # 当前价格
        self.datetime = None  # 当前时间
        
    def log(self, txt, dt=None):
        """日志函数"""
        dt = dt or self.datetime
        print(f'{dt}: {txt}')
        
    def notify_order(self, order):
        """订单状态更新"""
        if order.status in ['Submitted', 'Accepted']:
            return
        
        if order.status in ['Completed']:
            if order.isbuy():
                self.log(f'买入执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 手续费: {order.executed.comm:.2f}')
            else:
                self.log(f'卖出执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 手续费: {order.executed.comm:.2f}')
        
        self.order = None
        
    def notify_trade(self, trade):
        """交易状态更新"""
        if trade.isclosed:
            self.log(f'交易利润, 毛利润: {trade.pnl:.2f}, 净利润: {trade.pnlcomm:.2f}')
            
    def next(self):
        """策略核心逻辑，需要子类实现"""
        raise NotImplementedError

class SimpleMAStrategy(StrategyBase):
    """简单双均线策略示例"""
    def __init__(self):
        super().__init__()
        self.params.update({
            'fast_period': 10,  # 快速均线周期
            'slow_period': 20   # 慢速均线周期
        })
        self.fast_ma = None
        self.slow_ma = None
        
    def next(self):
        # 计算均线
        close = self.data['close']
        self.fast_ma = close.rolling(window=self.params['fast_period']).mean()
        self.slow_ma = close.rolling(window=self.params['slow_period']).mean()
        
        # 交易逻辑
        if self.fast_ma[-1] > self.slow_ma[-1] and self.fast_ma[-2] <= self.slow_ma[-2]:
            if self.position <= 0:
                self.order = self.buy()
                
        elif self.fast_ma[-1] < self.slow_ma[-1] and self.fast_ma[-2] >= self.slow_ma[-2]:
            if self.position >= 0:
                self.order = self.sell()

class StrategyContainer:
    """策略容器"""
    def __init__(self):
        self.strategies = {}
        
    def add_strategy(self, name, strategy):
        self.strategies[name] = strategy
        
    def run_all(self, data):
        """运行所有策略"""
        results = {}
        for name, strategy in self.strategies.items():
            strategy.data = data
            strategy.next()
            results[name] = strategy.position
        return results