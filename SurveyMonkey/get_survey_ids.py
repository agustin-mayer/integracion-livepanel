import http.client
import json

# Función para realizar la conexión
def connect():
    return http.client.HTTPSConnection("api.surveymonkey.com")

def get_request(conn, endpoint, headers):
    conn.request("GET", endpoint, headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode())

def get_survey_ids(api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, "/v3/surveys", headers)
    print(response_data)

def main():
    # API Token (debes reemplazarlo con el tuyo)
    api_token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ"

    # Realizar la conexión
    conn = connect()

    # Obtener los IDs de todas las encuestas disponibles
    print(get_survey_ids(api_token, conn)) 

