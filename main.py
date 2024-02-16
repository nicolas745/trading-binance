#!/bin/python3
from apibinance.binance import Binance
print(Binance(True).get_spot().getbalances().getwallets().keys())