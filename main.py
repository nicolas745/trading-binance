#!.venv/bin/python3
from apibinance.binance import Binance
from web.main import main,run
#main()
print(Binance().get_spot().getdata())
#run()
