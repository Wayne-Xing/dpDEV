from qh_cn import ChinaFutures



cf = ChinaFutures()

product_id = cf.get_product_id("豆粕")
print(f"豆粕主力合约ID: {product_id}")