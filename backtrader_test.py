import efinance as ef
stock_code = '600519'
df = ef.futures.get_futures_base_info()
print(df[df['期货名称'].str.contains('豆粕')])

# 主力合约
# 863  m2505  豆粕2505  114.m2505  大商所
# 862     mm  豆粕主连  114.mm     大商所
quote_id = '114.mm'
df_dp = ef.futures.get_quote_history(quote_id)
print(df_dp)