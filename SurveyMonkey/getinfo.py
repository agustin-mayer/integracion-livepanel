import http.client
import json

# Definir las URL de los endpoints
survey_id = "412807489"
survey_pages_url = f"/v3/surveys/{survey_id}/pages"
questions_url = "/v3/surveys/412807489/pages/{}/questions"
response_bulk_url = "/v3/collectors/430914330/responses/bulk"
response_details_url = "/v3/collectors/430914330/responses/{}/details?simple=true"

# Token de autorización
token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

# Configuración de la conexión HTTP
conn = http.client.HTTPSConnection("api.surveymonkey.com")

# Headers para la solicitud
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Obtener las páginas de la encuesta
conn.request("GET", survey_pages_url, headers=headers)
survey_pages_response = conn.getresponse()
survey_pages_data = json.loads(survey_pages_response.read())

# Obtener la lista completa de preguntas
all_questions = {}
for page in survey_pages_data["data"]:
    page_id = page["id"]
    conn.request("GET", questions_url.format(page_id), headers=headers)
    page_questions_response = conn.getresponse()
    page_questions_data = json.loads(page_questions_response.read())
    for question in page_questions_data["data"]:
        question_id = question["id"]
        question_heading = question["heading"]
        all_questions[question_id] = question_heading

# Obtener las respuestas del collector
conn.request("GET", response_bulk_url, headers=headers)
response_bulk_response = conn.getresponse()
response_bulk_data = json.loads(response_bulk_response.read())

# Obtener la lista completa de preguntas con sus textos
all_questions = {}
print("Todas las preguntas de la encuesta ")
for page in survey_pages_data["data"]:
    page_id = page["id"]
    print(f"Pagina {page_id}")
    conn.request("GET", questions_url.format(page_id), headers=headers)
    page_questions_response = conn.getresponse()
    page_questions_data = json.loads(page_questions_response.read())
    for question in page_questions_data["data"]:
        question_id = question["id"]
        heading = question["heading"]
        all_questions[question_id] = heading
        print(f"- {question_id}: {heading}")

# Recorrer las respuestas de los usuarios
for response in response_bulk_data["data"]:
    response_id = response["id"]
    answered_questions = {}
    unanswered_questions = list(all_questions.keys())  # Lista de IDs de preguntas
    conn.request("GET", response_details_url.format(response_id), headers=headers)
    response_details_response = conn.getresponse()
    response_details_data = json.loads(response_details_response.read())
    for page in response_details_data["pages"]:
        for question in page["questions"]:
            question_id = question["id"]
            answer_text = question.get("answers", [{}])[0].get("simple_text", "No hay respuesta")
            answered_questions[question_id] = answer_text
            if question_id in unanswered_questions:
                unanswered_questions.remove(question_id)
    print()
    print("Respuesta del usuario:", response_id)
    print("Preguntas respondidas:")
    for question_id, answer_text in answered_questions.items():
        print(f"- {question_id}: {answer_text}")
    print("Preguntas no respondidas:", unanswered_questions)
