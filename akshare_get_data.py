import akshare as ak

#豆粕ETF数据获取

# 外盘期货合约数据
# 产品列表
# symbol_map = ak.futures_hq_subscribe_exchange_symbol()
# # 产品id
# cbot_symbol = symbol_map[symbol_map["symbol"]=="CBOT-黄豆"]["code"].values  # 如"ZS00"
# print(cbot_symbol)

# futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(symbol=cbot_symbol[0])
# print(futures_foreign_commodity_realtime_df)

# symbol_map = ak.futures_symbol_mark(symbol) ["symbol"]
# print(symbol_map)

df = ak.futures_hist_em(symbol="豆粕主连", period="daily") 
print(df)
# dp = ak.futures_zh_realtime(symbol="豆粕")

# print(dp)