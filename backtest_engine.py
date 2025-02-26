class BacktestEngine:
    def __init__(self):
        self.data = None
        self.position = 0
        self.cash = 1000000
        self.trades = []
        self.equity = []
        
    def set_commission(self, commission_rate):
        """设置手续费"""
        pass

    def set_slippage(self, slippage):
        """设置滑点"""
        pass

    def match_orders(self, order):
        """订单撮合"""
        pass

    def update_equity(self):
        """更新账户权益"""
        pass