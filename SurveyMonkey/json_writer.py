import csv
import json
import os

def save_json_responses(collector_id, responses):
    data_folder = f"./data/{collector_id}/"
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    json_path = os.path.join(data_folder, "original_responses.json")

    with open(json_path, 'w') as json_file:
        json.dump(responses, json_file, indent=4)
    print(f"Respuestas JSON guardadas en {json_path}")

def parse_header(header):
    if header == 'ResponseID':
        return None, None, None, None, None
    try:
        parts = header.split('.')  # Salida: ['P1', 'Q2_CID'] o ['P1', 'Q2', 'R3_CID']
        
        page_part = parts[0]
        question_part = parts[1]
        row_part = parts[2] if len(parts) > 2 else None

        page_id = page_part[1:]

        if (row_part):
            question_id = question_part[1:]
            row_parts = row_part.split('_')
            row_id = row_parts[0][1:]
            choice_id = row_parts[1]
            return page_id, question_id, choice_id, row_id, None
        else:
            question_parts = question_part.split('_')
            question_id = question_parts[0][1:]
            if len(question_parts) > 1:
                if question_parts[1].startswith('R'):
                    row_id = question_parts[1][1:]
                    return page_id, question_id, None, row_id, None
                elif question_parts[1].startswith('O'):
                    other_id = question_parts[1][1:]
                    return page_id, question_id, None, None, other_id
                else:
                    choice_id = question_parts[1]
                    return page_id, question_id, choice_id, None, None
            else:
                return page_id, question_id, "", None, None
    except ValueError:
        return None, None, None, None

def csv_to_json_and_update(csv_file, api, survey_collector_id):
    with open(csv_file, 'r', encoding='latin1') as file:
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
                    if choice_id: #preguntas net promoter score
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
            
    print("Respuestas actualizadas con exito.")
