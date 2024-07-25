import http.client
import json

class SurveyMonkeyAPI:
    def __init__(self, token,survey_api_url):
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"bearer {token}",
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
    
    def complete_response(self, survey_collector_id, response_id, payload): 
        url = f"/v3/collectors/{survey_collector_id}/responses/{response_id}"
        return self._api_request("PATCH", url, payload)
    
    def get_responses(self, collector_id):
        url = f"/v3/collectors/{collector_id}/responses/bulk"
        return self._api_request("GET", url)