import json
from src.util.Network import Network


class UserData:
    def __init__(self, id:int, create_dt:str, **kwargs):
        self.id = id
        self.create_dt = create_dt

    @staticmethod
    def get_data(use_ip_id:int, device_id:str):
        try:
            url = f"https://q7548ulvf4.execute-api.ap-northeast-2.amazonaws.com/total/v1/userdata"
            params = {'use_ip_id':use_ip_id, 'device_id':device_id}
            resp = Network.request(url, params, method="get")
            print(resp)
            resp_dict = json.loads(resp)
            if resp_dict is not None and 'result' in resp_dict:
                result_dict = resp_dict['result']
                userdata = UserData(**result_dict)
                return userdata
            else:
                return None
        except Exception as e:
            print(e)
        return None