import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get(self, endpoint, params=None, headers=None):
        return self._request("GET", endpoint, params=params, headers=headers)
    
    def post(self, endpoint, data=None, json=None, headers=None):
        return self._request("POST", endpoint, data=data, json=json, headers=headers)
    
    def put(self, endpoint, data=None, json=None, headers=None):
        return self._request("PUT", endpoint, data=data, json=json, headers=headers)
    
    def delete(self, endpoint, headers=None):
        return self._request("DELETE", endpoint, headers=headers)
    
    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response
