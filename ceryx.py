from datetime import datetime
import requests
"""
Design: Class Ceryx implements websocket connection to server
- close connection once done
- should minimize overhead this way, instead of sending HTTP requests for each function
"""

class Ceryx:
    def __init__(self, token) -> None:
        self.token = token
        self.base = 'http://127.0.0.1:5000/'

    # execute order should generalize to any broker, but maybe would need various execute functions for each asset class
    def execute_order(self, broker, order, order_type, equity, quantity, price):
        order_details = {'api_key' : self.token, 'broker' : broker, 'timestamp' : datetime.now().strftime('%H:%M:%S:%MS'), \
        'order' : order, 'order_type' : order_type, 'instrument': equity, 'quantity': quantity, 'spot' : price}
        r = requests.get(f'{self.base}{order}', params=order_details)
        return r.status_code


    # Return all open positions
    def open_positions(self) -> None:
        return None

        
    # Return all trades between the start and end date
    def get_trade_history(self, start, end) -> None:
        return None   

a = Ceryx('alvinjz2')
print(a.execute_order('IB', 'buy', 'Market', 'AAPL', '100', '100'))