import http.client
import json

class LivepanelAPI:
    def __init__(self, token,survey_api_url):
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"{token}",
            "Content-Type": "application/json"
        }
        self.conn = http.client.HTTPSConnection(f"{survey_api_url}")

    def _api_request(self, method, url, payload=None):
        if payload is not None:
            payload = json.dumps(payload)
            self.conn.request(method, url, headers=self.headers, body=payload)
        else:
            self.conn.request(method, url, headers=self.headers)
        response = self.conn.getresponse()
        data = json.loads(response.read())
        return data

    def create_project(self, payload): 
        url = f"/v2/projects/"
        return self._api_request("POST", url, payload)