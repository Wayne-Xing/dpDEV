import akshare as ak
import pandas as pd
import time
from datetime import datetime

class DataFetcher:
    def __init__(self):
        self.data = None

    def fetch_dometic_info(self, product):
        """获取国内期货信息"""
        symbol_map = ak.futures_symbol_mark() 
        return(symbol_map[symbol_map["symbol"].str.contains(product)]["symbol"].values[0])
        pass

    def fetch_foreign_info(self, product):
        """获取外盘期货信息"""
        symbol_map = ak.futures_hq_subscribe_exchange_symbol()
        return(symbol_map[symbol_map["symbol"]=="CBOT-黄豆"]["code"].values[0])
        pass

    def fetch_domestic_data_cur(self, symbol):
        """获取实时国内期货数据"""
        data = ak.futures_zh_realtime(symbol=symbol)
        return data
        pass

    def fetch_domestic_data_his(self, symbol, period='daily', start_date='', end_date=''):
        """获取历史国内期货数据
        Args:
            symbol: 期货代码
            period: 数据周期，默认为'daily'
            start_date: 开始日期，默认为空
            end_date: 结束日期，默认为空
        """
        if not period:
            period = 'daily'
        
        if start_date and end_date:
            data = ak.futures_hist_em(symbol=symbol+'主连', period=period, start_date=start_date, end_date=end_date)
        else:
            data = ak.futures_hist_em(symbol=symbol+'主连', period=period)
        return data
        pass

    def fetch_foreign_data_cur(self, symbol):
        """获取实时外盘期货数据"""
        data = ak.futures_foreign_commodity_realtime(symbol)
        return data
        pass

    def fetch_foreign_data_his(self, symbol):
        """获取历史外盘期货数据"""
        futures_foreign_hist_df = ak.futures_foreign_hist(symbol=symbol)
        return(futures_foreign_hist_df)

        pass

    def process_data(self, data, status):
        """数据预处理"""
        # 创建列名映射字典
        column_mapping = {
            '名称': 'name',
            '日期': 'date',
            '时间': 'date',
            'tradedate': 'date',
            '行情时间 ': 'time',
            'ticktime ': 'time',
            '开盘价': 'open',
            '最高价': 'high',
            '最低价': 'low',
            '收盘价': 'close',
            '最新价': 'close',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '昨日结算价': 'ys_close',
            '成交量': 'volume',
            '持仓量': 'openinterest',
            '涨跌幅': 'change_pct',
            'changepercent': 'change_pct',
            
        }
        
        # 重命名列
        df = data.rename(columns=column_mapping)
        
        # 设置日期索引
        df.index = pd.to_datetime(df.date)
        
        # 确保必要的列存在
        if 'openinterest' not in df.columns:
            df['openinterest'] = 0
        if 'time' not in df.columns:
            current_time = datetime.now().strftime('%H:%M:%S')
            df['time'] = current_time
            
        # 选择需要的列并排序
        if status == 'his':
            df = df[['open', 'high', 'low', 'close', 'volume']]
        elif status == 'cur':
            df = df[['name','time','open', 'high', 'low', 'close', 'change_pct']]
        else:
            pass
        
        return df

    def process_csv(self, file):
        """处理CSV文件
        Args:
            file: CSV文件路径
        Returns:
            处理后的DataFrame
        """
        try:
            # 读取CSV文件，尝试自动检测编码
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='gbk')
            
            # 处理列名，去除空格和特殊字符
            df.columns = df.columns.str.strip()
            
            # 设置第一列为索引
            df = df.set_index(df.columns[0])
            
            # 如果存在日期列，转换为datetime类型
            date_cols = df.filter(like='日期').columns
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')
            
            # 处理数值列，将百分比转换为小数
            for col in df.columns:
                if df[col].dtype == 'object':
                    # 检查是否为百分比列
                    if df[col].str.contains('%').any():
                        df[col] = df[col].str.rstrip('%').astype('float') / 100
            
            # 填充空值
            df = df.fillna(method='ffill')
            
            return df
            
        except Exception as e:
            print(f"处理CSV文件时出错: {str(e)}")
            return None
