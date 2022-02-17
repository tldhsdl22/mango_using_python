import json
from src.util.Network import Network


class UserAgentInfo:
    def __init__(self, id: int, user_agent: str, platform: str, width: float, height: float, ratio: float, **kwargs):
        self.id = id
        self.user_agent = user_agent
        self.platform = platform
        self.width = width
        self.height = height
        self.ratio = ratio

    @staticmethod
    def get_data(userdata_id: str, device_id: str):
        try:
            url = f"https://q7548ulvf4.execute-api.ap-northeast-2.amazonaws.com/total/v1/useragent"
            params = {'userdata_id': userdata_id, 'device_id': device_id}
            resp = Network.request(url, params, method="get")
            print(resp)
            resp_dict = json.loads(resp)
            if resp_dict is not None and 'result' in resp_dict:
                result_dict = resp_dict['result']
                ua = UserAgentInfo(**result_dict)
                return ua
            else:
                return None
        except Exception as e:
            print(e)
        return None
