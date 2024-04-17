import http.client

conn = http.client.HTTPSConnection("api.surveymonkey.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
    }

conn.request("GET", "/v3/collectors/430914330/responses/bulk", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))