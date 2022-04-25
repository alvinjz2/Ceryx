from datetime import datetime
import requests

class Ceryx:
    def __init__(self, token) -> None:
        self.token = token
        self.base = 'http://127.0.0.1:5000/'

    def execute_order(self, broker, order, order_type, equity, quantity, price):
        order_details = {'api_key' : self.token, 'broker' : broker, 'timestamp' : datetime.now().strftime('%H:%M:%S:%MS'), \
        'order' : order, 'order_type' : order_type, 'instrument': equity, 'quantity': quantity, 'spot' : price}
        r = requests.get(f'{self.base}{order}', params=order_details)
        return r.status_code
    

a = Ceryx('alvinjz2')
print(a.execute_order('IB', 'buy', 'Market', 'AAPL', '100', '100'))