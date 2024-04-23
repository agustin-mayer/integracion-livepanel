import http.client
import json
import csv

# Definir la URL del endpoint
survey_id = "412807489"
survey_details_url = f"/v3/surveys/{survey_id}/details"

# Token de autorización
token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

# Configuración de la conexión HTTP
conn = http.client.HTTPSConnection("api.surveymonkey.com")

# Headers para la solicitud
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Función para obtener las opciones de las preguntas
def get_question_options():
    conn.request("GET", survey_details_url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    options = {}
    for page in data["pages"]:
        for question in page["questions"]:
            if "answers" in question:
                for choice in question["answers"]["choices"]:
                    options[choice["id"]] = f"{choice['id']}"
            elif question["family"] == "open_ended":
                options[question["id"]] = f"{question['id']}"
    return options

# Obtener las opciones de las preguntas
question_options = get_question_options()

# Obtener las respuestas del collector
response_bulk_url = "/v3/collectors/430914330/responses/bulk"
conn.request("GET", response_bulk_url, headers=headers)
response_bulk_response = conn.getresponse()
response_bulk_data = json.loads(response_bulk_response.read())

# Lista para almacenar los IDs de respuesta de usuario
response_ids = []

# Crear y abrir el archivo CSV en modo escritura
with open("encuesta_respuestas.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Crear el escritor CSV
    csv_writer = csv.writer(csvfile)

    # Escribir encabezados de columna
    csv_writer.writerow(["User Response ID"] + list(question_options.values()))

    # Recorrer las respuestas de los usuarios y completar la tabla
    for response in response_bulk_data["data"]:
        response_id = response["id"]  # Obtener el ID de respuesta de usuario
        response_ids.append(response_id)  # Agregar el ID a la lista
        response_row = [response_id] + ["0"] * len(question_options)  # Inicializar una fila con 0s
        for page in response["pages"]:
            for question in page["questions"]:
                if "answers" in question:
                    for answer in question["answers"]:
                        choice_id = answer.get("choice_id")
                        if choice_id in question_options:
                            # Obtener el índice de la columna correspondiente al ID de la opción
                            column_index = list(question_options.keys()).index(choice_id)
                            # Marcar la opción seleccionada con un 1 en la fila
                            response_row[column_index + 1] = "1"
                elif question["family"] == "open_ended":
                    # Obtener el índice de la columna correspondiente al ID de la pregunta
                    column_index = list(question_options.keys()).index(question["id"])
                    # Obtener el texto de la respuesta de texto libre
                    text_response = ""
                    for answer in question["answers"]:
                        if "text" in answer:
                            text_response += answer["text"] + " "
                    # Agregar el texto de la respuesta como valor en la columna correspondiente
                    response_row[column_index + 1] = text_response.strip()
        # Escribir la fila en el archivo CSV
        csv_writer.writerow(response_row)

print("Archivo CSV generado exitosamente.")
