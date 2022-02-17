import json
from src.util.Network import Network


class NNB:
    def __init__(self, id: int, value: str, creation_dt: str, **kwargs):
        self.id = id
        self.value = value
        self.creation_dt = creation_dt
        self.kwargs = kwargs

    @staticmethod
    def get_data(userdata_id: str, device_id: str):
        try:
            url = f"https://q7548ulvf4.execute-api.ap-northeast-2.amazonaws.com/total/v1/nnb"
            params = {'userdata_id': userdata_id, 'device_id': device_id}
            resp = Network.request(url, params, method="get")
            print(resp)
            resp_dict = json.loads(resp)
            if resp_dict is not None and 'result' in resp_dict:
                result_dict = resp_dict['result']
                nnb = NNB(**result_dict)
                return nnb
            else:
                return None
        except Exception as e:
            print(e)
        return None
