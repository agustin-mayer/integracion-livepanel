import http.client
import json

conn = http.client.HTTPSConnection("api.surveymonkey.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
    }

def get_response(response_id):
    response_url = f"/v3/collectors/{response_id}/responses/bulk"
    conn.request("GET", response_url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    print(response)
    return data

get_response