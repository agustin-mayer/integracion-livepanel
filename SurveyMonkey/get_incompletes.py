import http.client
import json

# Función para realizar la conexión
def connect():
    return http.client.HTTPSConnection("api.surveymonkey.com")

# Función para realizar una solicitud GET
def get_request(conn, endpoint, headers):
    conn.request("GET", endpoint, headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode())

# Función para obtener los IDs de todas las encuestas disponibles
def get_survey_ids(api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, "/v3/surveys", headers)
    return [survey["id"] for survey in response_data["data"]]

# Función para obtener los IDs de todos los colectores de una encuesta
def get_survey_collectors(survey_id, api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, f"/v3/surveys/{survey_id}/collectors", headers)
    return [collector["id"] for collector in response_data["data"]]

# Función para obtener todas las páginas de una encuesta
def get_survey_pages(survey_id, api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, f"/v3/surveys/{survey_id}/pages", headers)
    return response_data["data"]

# Función para obtener todas las preguntas de una página
def get_page_questions(survey_id, page_id, api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, f"/v3/surveys/{survey_id}/pages/{page_id}/questions", headers)
    return response_data["data"]

# Función para obtener todas las respuestas a encuestas
def get_survey_responses(collector_id, api_token, conn):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response_data = get_request(conn, f"/v3/collectors/{collector_id}/responses/bulk", headers)
    return response_data["data"]

# Función para comparar las preguntas respondidas con todas las preguntas
def identify_unanswered_questions(survey_id, collector_id, survey_responses, api_token, conn):
    all_questions = []
    # Obtener todas las preguntas de la encuesta
    survey_pages = get_survey_pages(survey_id, api_token, conn)
    for page in survey_pages:
        page_id = page["id"]
        questions = get_page_questions(survey_id, page_id, api_token, conn)
        all_questions.extend(questions)

    # Comparar preguntas respondidas con todas las preguntas
    unanswered_questions = []
    for question in all_questions:
        question_id = question["id"]
        question_heading = question["heading"]
        question_responded = False
        for response in survey_responses:
            if "pages" in response:
                for page_response in response["pages"]:
                    if page_response.get("id") == page_id and question_id in [q.get("id") for q in page_response.get("questions", [])]:
                        question_responded = True
                        break
            if question_responded:
                break
        if not question_responded:
            unanswered_questions.append((collector_id, question_id, question_heading))
    return unanswered_questions

# Main function
def main():
    # API Token (debes reemplazarlo con el tuyo)
    api_token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

    # Realizar la conexión
    conn = connect()

    # Obtener los IDs de todas las encuestas disponibles
    survey_ids = get_survey_ids(api_token, conn)

    # Iterar sobre cada encuesta
    for survey_id in survey_ids:
        print(f"Encuesta ID: {survey_id}")

        # Obtener los IDs de todos los colectores de la encuesta
        collectors = get_survey_collectors(survey_id, api_token, conn)

        # Iterar sobre cada colector
        for collector_id in collectors:
            print(f"  Colector ID: {collector_id}")

            # Obtener todas las respuestas a la encuesta
            survey_responses = get_survey_responses(collector_id, api_token, conn)

            # Identificar preguntas no respondidas
            unanswered_questions = identify_unanswered_questions(survey_id, collector_id, survey_responses, api_token, conn)

            # Mostrar preguntas no respondidas
            if unanswered_questions:
                print("    Preguntas no respondidas:")
                for collector_id, question_id, question_heading in unanswered_questions:
                    print(f"      Colector ID: {collector_id}, ID de la pregunta: {question_id}, Pregunta: {question_heading}")
            else:
                print("    Todas las preguntas fueron respondidas.")
        print()

if __name__ == "__main__":
    main()
