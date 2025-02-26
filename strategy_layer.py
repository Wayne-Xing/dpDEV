import pandas as pd
import numpy as np

class StrategyBase:
    def __init__(self):
        self.position = 0
        self.params = {}

    def generate_signals(self, data):
        """生成交易信号"""
        raise NotImplementedError

class StrategyContainer:
    def __init__(self):
        self.strategies = {}
        
    def add_strategy(self, name, strategy):
        """添加策略"""
        self.strategies[name] = strategy

    def run_all(self, data):
        """运行所有策略"""
        pass