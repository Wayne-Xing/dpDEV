from qh_cn import ChinaFutures
from qh_usa import USAFutures
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

class DpLr:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, x, y):
        """
        使用线性回归拟合数据
        :param x: 自变量数据
        :param y: 因变量数据
        :return: 拟合后的模型
        """
        self.model.fit(x, y)
        return self.model

    def predict(self, x):
        """
        使用拟合后的模型进行预测
        :param x: 自变量数据
        :return: 预测结果
        """
        return self.model.predict(x)

class SoybeanAnalyzer:
    def __init__(self):
        self.cn_futures = ChinaFutures()
        self.us_futures = USAFutures()
        
    def prepare_data(self, start_date, end_date=None):
        """准备数据并对齐"""
        cn_data = self.cn_futures.get_history_data("豆粕", start_date, end_date)
        us_data = self.us_futures.get_history_data("大豆", start_date, end_date)
        
        # 对齐数据
        merged_data = pd.merge(
            cn_data['close'],
            us_data['Close'],
            left_index=True,
            right_index=True,
            how='inner'
        )
        merged_data.columns = ['CN_SoyMeal', 'US_Soybean']
        return merged_data
        
    def analyze_correlation(self, data):
        """分析相关性"""
        X = data['US_Soybean'].values.reshape(-1, 1)
        y = data['CN_SoyMeal'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        r2 = r2_score(y, model.predict(X))
        return {
            'coefficient': model.coef_[0],
            'intercept': model.intercept_,
            'r2': r2
        }
        
    def plot_correlation(self, data, results):
        """绘制相关性图表"""
        plt.figure(figsize=(10, 6))
        plt.scatter(data['US_Soybean'], data['CN_SoyMeal'], alpha=0.5)
        plt.plot(data['US_Soybean'], 
                results['coefficient'] * data['US_Soybean'] + results['intercept'], 
                'r')
        plt.xlabel('US Soybean Price')
        plt.ylabel('CN Soy Meal Price')
        plt.title(f'Correlation Analysis (R² = {results["r2"]:.3f})')
        plt.grid(True)
        plt.show()