import requests as requests

class Network:
    @staticmethod
    def request(url, params=None, headers = None, method = "get"):
        try:
            if headers is None:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                }
            print(url)
            if method.lower() == "get":
                resp = requests.get(url, params=params, headers=headers)
            elif method.lower() == "post":
                resp = requests.post(url, params=params, headers=headers)
            elif method.lower() == "put":
                resp = requests.put(url, params=params, headers=headers)
            return resp.text
        except:
            return "Request Error"