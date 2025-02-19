from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData, TickData
from datetime import datetime, timedelta
import pandas as pd
import time
import sqlite3

class ChinaFutures:
    def __init__(self):
        """初始化期货数据接口"""
        self.symbol_map = {
            "豆粕": ("M", Exchange.DCE),    # 大连商品交易所
            "豆油": ("Y", Exchange.DCE),
            "大豆": ("A", Exchange.DCE),
            "玉米": ("C", Exchange.DCE),
            "沪铜": ("CU", Exchange.SHFE),  # 上海期货交易所
            "沪铝": ("AL", Exchange.SHFE),
            "黄金": ("AU", Exchange.SHFE)
        }
        
        self._cache = {}
        self._cache_timeout = 60
        
        # 尝试初始化vnpy数据库
        try:
            self.database = get_database()
            self.use_vnpy_db = True
        except Exception as e:
            print(f"VNPY数据库初始化失败，使用本地SQLite数据库: {e}")
            self.database = self._init_local_db()
            self.use_vnpy_db = False

    def _init_local_db(self):
        """初始化本地SQLite数据库"""
        db_path = "futures_data.db"
        conn = sqlite3.connect(db_path)
        
        # 创建实时数据表
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS realtime_data (
                symbol TEXT,
                datetime TEXT,
                price REAL,
                volume REAL,
                update_time TEXT,
                PRIMARY KEY (symbol)
            )
        ''')
        
        # 创建历史数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_data (
                symbol TEXT,
                datetime TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                PRIMARY KEY (symbol, datetime)
            )
        ''')
        
        conn.commit()
        return conn

    def _save_realtime_data(self, symbol, price, volume=0):
        """保存实时数据到本地数据库"""
        if not self.use_vnpy_db:
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor = self.database.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO realtime_data 
                    (symbol, datetime, price, volume, update_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (symbol, now, price, volume, now))
                self.database.commit()
            except Exception as e:
                print(f"保存实时数据失败: {str(e)}")

    def _get_trading_date(self):
        """获取当前交易日期"""
        current_time = datetime.now()
        # 如果是周末，返回上周五
        if current_time.weekday() >= 5:
            days_to_subtract = current_time.weekday() - 4
            current_time = current_time - timedelta(days=days_to_subtract)
        # 如果是早上9点前，返回上一个交易日
        elif current_time.hour < 9:
            current_time = current_time - timedelta(days=1)
            # 如果上一日是周末，继续往前推
            if current_time.weekday() >= 5:
                days_to_subtract = current_time.weekday() - 4
                current_time = current_time - timedelta(days=days_to_subtract)
        return current_time.strftime('%Y-%m-%d')

    def _get_current_main_contract(self, symbol):
        """获取当前主力合约代码"""
        now = datetime.now()
        code, exchange = self.symbol_map[symbol]
        # 计算当前月份的主力合约代码
        if now.day > 15:  # 15号后看下月合约
            if now.month == 12:
                year = now.year + 1
                month = 1
            else:
                year = now.year
                month = now.month + 1
        else:
            year = now.year
            month = now.month
        
        contract = f"{code}{str(year)[2:]}{month:02d}"
        return contract, exchange

    def get_product_id(self, symbol, date=None):
        """获取期货产品ID"""
        try:
            if symbol not in self.symbol_map:
                raise ValueError(f"不支持的期货品种: {symbol}")
            
            contract, exchange = self._get_current_main_contract(symbol)
            return f"{contract}.{exchange.value}"
            
        except Exception as e:
            print(f"获取期货产品ID失败: {str(e)}")
            return None

    def get_realtime_price(self, symbol):
        """获取实时价格"""
        try:
            # 检查缓存
            cache_key = f"realtime_{symbol}"
            if cache_key in self._cache:
                cache_time, cache_data = self._cache[cache_key]
                if time.time() - cache_time < self._cache_timeout:
                    return cache_data

            contract_id = self.get_product_id(symbol)
            if not contract_id:
                return None

            # 使用本地数据库获取最新价格
            if not self.use_vnpy_db:
                cursor = self.database.cursor()
                cursor.execute('''
                    SELECT price, update_time FROM realtime_data 
                    WHERE symbol = ?
                ''', (contract_id,))
                result = cursor.fetchone()
                
                if result:
                    price, update_time = result
                    # 检查数据是否过期（超过1小时）
                    update_time = datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')
                    if datetime.now() - update_time < timedelta(hours=1):
                        self._cache[cache_key] = (time.time(), price)
                        return price
                
                # 如果没有数据或数据过期，模拟一个价格（实际使用中应该从实时行情源获取）
                simulated_price = 3000.0  # 这里应该替换为实际的数据源
                self._save_realtime_data(contract_id, simulated_price)
                self._cache[cache_key] = (time.time(), simulated_price)
                return simulated_price
            
            return None
            
        except Exception as e:
            print(f"获取实时价格失败: {str(e)}")
            return None

    def get_history_data(self, symbol, start_date, end_date=None):
        """获取历史数据"""
        try:
            contract_id = self.get_product_id(symbol)
            if not contract_id:
                return None

            start = pd.to_datetime(start_date).strftime('%Y-%m-%d')
            end = pd.to_datetime(end_date).strftime('%Y-%m-%d') if end_date else datetime.now().strftime('%Y-%m-%d')

            if not self.use_vnpy_db:
                cursor = self.database.cursor()
                cursor.execute('''
                    SELECT datetime, open, high, low, close, volume 
                    FROM historical_data 
                    WHERE symbol = ? AND datetime BETWEEN ? AND ?
                    ORDER BY datetime
                ''', (contract_id, start, end))
                
                rows = cursor.fetchall()
                if not rows:
                    # 模拟一些历史数据（实际使用中应该从数据源获取）
                    data = self._generate_sample_data(start, end)
                    for record in data:
                        cursor.execute('''
                            INSERT OR IGNORE INTO historical_data 
                            (symbol, datetime, open, high, low, close, volume)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (contract_id, record['datetime'], record['open'], 
                              record['high'], record['low'], record['close'], 
                              record['volume']))
                    self.database.commit()
                    
                    # 重新获取数据
                    cursor.execute('''
                        SELECT datetime, open, high, low, close, volume 
                        FROM historical_data 
                        WHERE symbol = ? AND datetime BETWEEN ? AND ?
                        ORDER BY datetime
                    ''', (contract_id, start, end))
                    rows = cursor.fetchall()

                data = {
                    "datetime": [], "open": [], "high": [], 
                    "low": [], "close": [], "volume": []
                }
                
                for row in rows:
                    data["datetime"].append(pd.to_datetime(row[0]))
                    data["open"].append(row[1])
                    data["high"].append(row[2])
                    data["low"].append(row[3])
                    data["close"].append(row[4])
                    data["volume"].append(row[5])

                df = pd.DataFrame(data)
                df.set_index("datetime", inplace=True)
                return df
            
            return None
            
        except Exception as e:
            print(f"获取历史数据失败: {str(e)}")
            return None

    def _generate_sample_data(self, start, end):
        """生成示例数据（仅用于测试）"""
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        base_price = 3000
        data = []
        
        for date in dates:
            # 生成随机价格
            open_price = base_price + np.random.normal(0, 20)
            close_price = open_price + np.random.normal(0, 20)
            high_price = max(open_price, close_price) + abs(np.random.normal(0, 10))
            low_price = min(open_price, close_price) - abs(np.random.normal(0, 10))
            volume = np.random.randint(1000, 5000)
            
            data.append({
                'datetime': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })
            
            base_price = close_price
        
        return data

    def get_available_symbols(self):
        """获取所有可用的期货品种"""
        return list(self.symbol_map.keys())

    def clear_cache(self):
        """清除缓存"""
        self._cache = {}
