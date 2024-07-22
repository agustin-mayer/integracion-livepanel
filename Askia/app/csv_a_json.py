import csv
import json

# Función para determinar si una respuesta es una pregunta en bucle
def es_pregunta_bucle(cabecera):
    return cabecera.startswith('L') and ('_' in cabecera or '.' in cabecera)

# Función para obtener los LoopItemIds de una pregunta en bucle
def obtener_loop_ids(cabecera):
    partes_punto = cabecera.split('.')
    loop_item_ids = []
    if len(partes_punto) > 1:
        loop_item_ids.append(partes_punto[1].split('Q')[0])
        subpartes = partes_punto[0].replace('L', '')
        loop_item_ids.insert(0, subpartes)
    return loop_item_ids

# Función para obtener el QuestionId y la Data
def obtener_question_id_y_data(cabecera, valor):
    partes = cabecera.split('_')
    if len(partes) > 1:
        question_id = partes[0].replace('Q', '')
        modality_id = partes[1]
        return question_id, modality_id
    else:
        return cabecera.replace('Q', ''), valor

# Leer el archivo CSV y convertirlo en JSON
def csv_a_json(ruta_csv, ruta_json):
    with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabeceras = next(reader)

        respuestas = []

        for fila in reader:
            interview_id = int(fila[0])
            for i, valor in enumerate(fila[1:], start=1):
                # Omite valores "0"
                if valor == "0":
                    continue

                respuesta = {
                    "InterviewId": interview_id,
                    "Data": None,
                    "LoopItemIds": [],
                    "QuestionId": None
                }

                cabecera = cabeceras[i]
                
                if es_pregunta_bucle(cabecera):
                    loop_item_ids = obtener_loop_ids(cabecera)
                    question_partes = cabecera.split('Q')
                    if len(question_partes) > 1:
                        question_id = question_partes[0].replace('L', '').split('.')[0]
                        modality_id = question_partes[1].split('_')[1]

                        respuesta["LoopItemIds"].extend(loop_item_ids)
                        respuesta["QuestionId"] = question_id
                        respuesta["Data"] = int(modality_id) if valor == "1" else valor
                else:
                    partes = cabecera.split('_')
                    if len(partes) > 1:
                        question_id, modality_id = obtener_question_id_y_data(cabecera, valor)
                        respuesta["Data"] = int(modality_id) if valor == "1" else valor
                        respuesta["QuestionId"] = question_id
                    else:
                        respuesta["Data"] = int(valor) if valor.isdigit() else valor
                        respuesta["QuestionId"] = cabecera.replace('Q', '')

                if respuesta["QuestionId"] and respuesta["Data"] is not None:
                    respuestas.append(respuesta)

        estructura_json = {
            "Responses": respuestas
        }

    with open(ruta_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(estructura_json, jsonfile, ensure_ascii=False, indent=4)

# Rutas de archivos
ruta_csv = '../data/dataset2/train_dataset2.csv'
ruta_json = '../data/dataset2/updated_responses.json'

# Ejecutar la conversión
csv_a_json(ruta_csv, ruta_json)
