import csv
import json
import os
import pandas as pd  # Añadido para manipulación de CSV

def save_json_responses(collector_id, responses):
    """
    Guarda las respuestas JSON en un archivo.
    """
    data_folder = f"./data/{collector_id}/"
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    json_path = os.path.join(data_folder, "original_responses.json")

    with open(json_path, 'w') as json_file:
        json.dump(responses, json_file, indent=4)
    print(f"Respuestas JSON guardadas en {json_path}")

def clean_header(header):
    """
    Limpia el encabezado de la columna para eliminar la parte '[|]Validation'.
    """
    return header.replace('[|]Validation', '')

def parse_header(header):
    """
    Analiza el encabezado de una columna del CSV para extraer la información de la página, pregunta,
    elección, fila y otro id. Devuelve una tupla con (page_id, question_id, choice_id, row_id, other_id).
    """
    header = clean_header(header)  # Limpia el encabezado

    if header == 'ResponseID':
        return None, None, None, None, None
    try:
        parts = header.split('.')  # Salida esperada: ['P1', 'Q2_CID'] o ['P1', 'Q2', 'R3_CID']
        
        page_part = parts[0]
        question_part = parts[1] if len(parts) > 1 else None
        row_part = parts[2] if len(parts) > 2 else None

        page_id = page_part[1:]  # Quitar el prefijo 'P'

        if row_part:
            question_id = question_part[1:] if question_part else None
            row_parts = row_part.split('_')
            row_id = row_parts[0][1:]  # Quitar el prefijo 'R'
            choice_id = row_parts[1] if len(row_parts) > 1 else None
            return page_id, question_id, choice_id, row_id, None
        else:
            question_parts = question_part.split('_') if question_part else []
            question_id = question_parts[0][1:]  # Quitar el prefijo 'Q'
            if len(question_parts) > 1:
                if question_parts[1].startswith('R'):
                    row_id = question_parts[1][1:]  # Quitar el prefijo 'R'
                    return page_id, question_id, None, row_id, None
                elif question_parts[1].startswith('O'):
                    other_id = question_parts[1][1:]  # Quitar el prefijo 'O'
                    return page_id, question_id, None, None, other_id
                else:
                    choice_id = question_parts[1]
                    return page_id, question_id, choice_id, None, None
            else:
                return page_id, question_id, None, None, None
    except Exception as e:
        print(f"Error al analizar el encabezado '{header}': {e}")
        return None, None, None, None, None

def csv_to_json_and_update(csv_file, api, survey_collector_id):
    """
    Convierte un archivo CSV a formato JSON y actualiza las respuestas usando la API de SurveyMonkey.
    """
    # Limpia los encabezados del CSV
    temp_csv_file = 'temp_cleaned.csv'
    df = pd.read_csv(csv_file)
    df.columns = [clean_header(col) for col in df.columns]
    df = df.drop(columns=['Type'], errors='ignore')
    df.to_csv(temp_csv_file, index=False)

    with open(temp_csv_file, 'r', encoding='utf-8', errors='replace') as file:
        csv_reader = csv.DictReader(file)
        
        # Imprimir los nombres de las columnas para depuración
        print("Columnas en el archivo CSV:", csv_reader.fieldnames)

        for row in csv_reader:
            user_response_id = row['ResponseID']
            pages = {}
            
            for header, value in row.items():
                page_id, question_id, choice_id, row_id, other_id = parse_header(header)
                
                if not page_id or not question_id:
                    continue
                
                if value == '0' or value.strip() == '':
                    continue
                
                if page_id not in pages:
                    pages[page_id] = {"id": page_id, "questions": []}
                
                question = next((q for q in pages[page_id]["questions"] if q["id"] == question_id), None)
                
                if not question:
                    question = {"id": question_id, "answers": []}
                    pages[page_id]["questions"].append(question)
                
                if row_id:
                    if choice_id:  # Preguntas Net Promoter Score
                        question["answers"].append({"row_id": row_id, "choice_id": choice_id})
                    else:
                        question["answers"].append({"row_id": row_id, "text": value})
                elif other_id:
                    question["answers"].append({"other_id": other_id, "text": value})
                elif choice_id:
                    question["answers"].append({"choice_id": choice_id})
                else:
                    question["answers"].append({"text": value})
            
            user_data = {"pages": list(pages.values())}
            
            print(f"Actualizando respuesta del usuario: {user_response_id}")
            print(f"Data: {user_data}")
            
            response = api.complete_response(survey_collector_id, user_response_id, user_data)
            print(f"API Response: {response}")
            print("----------------------------")
            
    print("Respuestas actualizadas con éxito.")
    os.remove(temp_csv_file)  # Elimina el archivo temporal
 