import xalpha as xaimport
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

class MarketDataAnalyzer:
    def __init__(self):
        """初始化分析器"""
        self.data_cache = {}

    def get_index_data(self, code='000016', start='20230101', end=None):
        """获取指数数据"""
        try:
            if end is None:
                end = datetime.now().strftime('%Y%m%d')
            
            # 使用xalpha获取指数数据
            index_data = xa.get_index(code, start=start, end=end)
            return index_data
        except Exception as e:
            print(f"获取指数数据失败: {str(e)}")
            return None

    def get_stock_data(self, code='600519', start='20230101', end=None):
        """获取股票数据"""
        try:
            if end is None:
                end = datetime.now().strftime('%Y%m%d')
            
            # 使用xalpha获取股票数据
            stock = xa.get_stock(code, start=start, end=end)
            return stock
        except Exception as e:
            print(f"获取股票数据失败: {str(e)}")
            return None

    def analyze_correlation(self, data1, data2):
        """分析相关性"""
        try:
            # 确保两个数据集的日期对齐
            merged = pd.merge(
                data1['close'],
                data2['close'],
                left_index=True,
                right_index=True,
                how='inner'
            )
            
            # 计算相关系数
            corr = merged.corr()
            return corr.iloc[0,1]
        except Exception as e:
            print(f"计算相关性失败: {str(e)}")
            return None

    def plot_comparison(self, data1, data2, title="价格对比"):
        """绘制对比图"""
        try:
            plt.figure(figsize=(12, 6))
            
            # 归一化数据
            norm1 = data1['close'] / data1['close'].iloc[0]
            norm2 = data2['close'] / data2['close'].iloc[0]
            
            plt.plot(norm1.index, norm1.values, label='Series 1')
            plt.plot(norm2.index, norm2.values, label='Series 2')
            
            plt.title(title)
            plt.xlabel('Date')
            plt.ylabel('Normalized Price')
            plt.legend()
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"绘图失败: {str(e)}")

def main():
    analyzer = MarketDataAnalyzer()
    
    # 示例：获取上证50指数和贵州茅台的数据
    print("正在获取数据...")
    index_data = analyzer.get_index_data('000016')  # 上证50指数
    stock_data = analyzer.get_stock_data('600519')  # 贵州茅台
    