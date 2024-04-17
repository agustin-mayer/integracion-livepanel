import http.client
import json

conn = http.client.HTTPSConnection("api.surveymonkey.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
}

conn.request("GET", "/v3/surveys/412807489/responses/bulk", headers=headers)

res = conn.getresponse()
data_bytes = res.read()
# Decodificar los datos binarios en una cadena
data_str = data_bytes.decode("utf-8")
# Cargar la cadena JSON en un objeto Python
data = json.loads(data_str)
print(data_str)

def identificar_preguntas_incompletas(respuesta):
    preguntas_incompletas = []
    # Recorrer cada página en la respuesta
    for page in respuesta["pages"]:
        # Recorrer cada pregunta en la página
        for pregunta in page["questions"]:
            # Verificar si la pregunta no tiene respuestas
            print('entre')
            if pregunta["answers"]==[]:
                # Agregar la pregunta a la lista de preguntas incompletas]
                print("entre aca")
                preguntas_incompletas.append(pregunta)
    return preguntas_incompletas

# Recorrer cada respuesta en el JSON de respuestas
for respuesta in data["data"]:
    id_respuesta = respuesta["id"]
    preguntas_incompletas = identificar_preguntas_incompletas(respuesta)
    if preguntas_incompletas:
        print(f"Preguntas incompletas en la respuesta {id_respuesta}:")
        for pregunta in preguntas_incompletas:
            id_pregunta = pregunta["id"]
            print(f"- ID de pregunta: {id_pregunta}")
    else:
        print("No hay preguntas incompletas en la respuesta.")