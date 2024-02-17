import time
import requests
import hmac
import hashlib

class flexible:
    def __init__(self, base_url, api_secret, api_key) -> None:
        self.base_url = base_url
        self.api_secret = api_secret
        self.api_key = api_key
        timestamp = int(time.time() * 1000)
        query_string = 'timestamp=' + str(timestamp)
        signature = hmac.new(bytes(self.api_secret , 'latin-1'), msg = bytes(query_string , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        url = self.base_url + "sapi/v1/simple-earn/flexible/list?" + query_string + "&signature=" + signature
        print(url)
        response = requests.get(url, headers=headers)
        self.data = response

    def getdata(self):
        return self.data