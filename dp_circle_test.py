from dp_lr import SoybeanAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SoybeanTradeStrategy:
    def __init__(self):
        self.analyzer = SoybeanAnalyzer()
        self.positions = []
        self.trades = []
        
    def backtest(self, start_date, end_date=None):
        """回测策略"""
        # 获取5年数据
        data = self.analyzer.prepare_data(start_date, end_date)
        
        # 使用30天滚动窗口计算相关性
        window_size = 30
        results = []
        
        for i in range(window_size, len(data)):
            window_data = data.iloc[i-window_size:i]
            correlation = self.analyzer.analyze_correlation(window_data)
            
            current_price = data['CN_SoyMeal'].iloc[i]
            timestamp = data.index[i]
            
            # 策略逻辑
            if correlation['r2'] > 1.1:  # 相关性超过10%
                self.open_position('short', current_price, timestamp)
            elif correlation['r2'] < 0.9:  # 相关性低于10%
                self.open_position('long', current_price, timestamp)
            elif 0.95 <= correlation['r2'] <= 1.05:  # 相关性在5%范围内
                self.close_positions(current_price, timestamp)
                
            results.append({
                'timestamp': timestamp,
                'price': current_price,
                'correlation': correlation['r2']
            })
            
        # 计算策略收益
        return self.calculate_returns()
    
    def open_position(self, direction, price, timestamp):
        self.positions.append({
            'direction': direction,
            'entry_price': price,
            'entry_time': timestamp
        })
    
    def close_positions(self, price, timestamp):
        for position in self.positions:
            pnl = (price - position['entry_price']) * (-1 if position['direction'] == 'short' else 1)
            self.trades.append({
                'entry_time': position['entry_time'],
                'exit_time': timestamp,
                'direction': position['direction'],
                'entry_price': position['entry_price'],
                'exit_price': price,
                'pnl': pnl
            })
        self.positions = []
    
    def calculate_returns(self):
        df_trades = pd.DataFrame(self.trades)
        if len(df_trades) == 0:
            return {
                'total_trades': 0,
                'profitable_trades': 0,
                'total_pnl': 0,
                'win_rate': 0,
                'average_pnl': 0
            }
            
        return {
            'total_trades': len(df_trades),
            'profitable_trades': len(df_trades[df_trades['pnl'] > 0]),
            'total_pnl': df_trades['pnl'].sum(),
            'win_rate': len(df_trades[df_trades['pnl'] > 0]) / len(df_trades) * 100,
            'average_pnl': df_trades['pnl'].mean()
        }

def main():
    strategy = SoybeanTradeStrategy()
    start_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y%m%d")
    results = strategy.backtest(start_date)
    
    print("\n策略回测结果:")
    print(f"总交易次数: {results['total_trades']}")
    print(f"盈利交易次数: {results['profitable_trades']}")
    print(f"总盈亏: {results['total_pnl']:.2f}")
    print(f"胜率: {results['win_rate']:.2f}%")
    print(f"平均盈亏: {results['average_pnl']:.2f}")

if __name__ == "__main__":
    main()