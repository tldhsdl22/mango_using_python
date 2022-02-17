import json
from src.util.Network import Network


class IP:
    def __init__(self, use_ip_id: str, ip: str, **kwargs):
        self.use_ip_id = use_ip_id
        self.ip = ip

    @staticmethod
    def post_ip(ip: str, device_id: str, ip_type: str):
        try:
            url = "https://q7548ulvf4.execute-api.ap-northeast-2.amazonaws.com/total/v1/ip"
            params = {'ip': ip, 'device_id': device_id, 'type': ip_type}
            print(params)
            resp = Network.request(url, params, method="post")
            print(resp)
            resp_dict = json.loads(resp)
            if resp_dict is not None and 'result' in resp_dict:
                result_dict = resp_dict['result']
                total_ip = IP(**result_dict)
                return total_ip
        except:
            {}
        return None
