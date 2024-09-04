import csv
import json
import os
import pandas as pd
import uuid

class DataManager:
    def __init__(self, collector_id):
        #self.data_folder = f"data/{collector_id}/{uuid.uuid4().hex}/" 
        self.data_folder = f"data/{collector_id}/" #TESTING
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def get_data_folder(self):
        return self.data_folder

    def save_json_responses(self, responses):
        json_path = os.path.join(self.data_folder, f"original_responses.json")
        with open(json_path, 'w') as json_file:
            json.dump(responses, json_file, indent=4)
        print(f"Respuestas JSON guardadas en {json_path}")

    def json_to_csv(self, response_data):
        csv_path = os.path.join(self.data_folder, f"original_responses.csv")

        response_keys = set()
        choice_questions = set()

        for response in response_data["data"]:
            for page in response["pages"]:
                for question in page["questions"]:
                    question_id = question["id"]
                    page_id = page["id"]
                    question_key = f"P{page_id}.Q{question_id}"
                    if "answers" in question:
                        for answer in question["answers"]:
                            if "choice_id" in answer:
                                if "row_id" in answer:
                                    response_keys.add(f"{question_key}.R{answer['row_id']}_{answer['choice_id']}")
                                    question_key += f".R{answer['row_id']}"
                                else:
                                    response_keys.add(f"{question_key}_{answer['choice_id']}")
                                choice_questions.add(question_key)
                            elif "text" in answer:
                                if "row_id" in answer:
                                    response_keys.add(f"{question_key}_R{answer['row_id']}")
                                elif "other_id" in answer:
                                    response_keys.add(f"{question_key}_O{answer['other_id']}")
                                else:
                                    response_keys.add(f"{question_key}")

        headers = ["ResponseID"] + sorted(list(response_keys))

        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)
            
            for response in response_data["data"]:
                response_row = [response["id"]]
                response_values = {key: ("0" if key.rsplit('_', 1)[0] in choice_questions else "") for key in response_keys}
                for page in response["pages"]:
                    for question in page["questions"]:
                        question_id = question["id"]
                        page_id = page["id"]
                        question_key = f"P{page_id}.Q{question_id}"
                        if "answers" in question:
                            for answer in question["answers"]:
                                if "choice_id" in answer:
                                    if "row_id" in answer:
                                        response_values[f"{question_key}.R{answer['row_id']}_{answer['choice_id']}"] = "1"
                                    else:
                                        response_values[f"{question_key}_{answer['choice_id']}"] = "1"
                                elif "text" in answer:
                                    if "row_id" in answer:
                                        response_values[f"{question_key}_R{answer['row_id']}"] = answer["text"]
                                    elif "other_id" in answer:
                                        response_values[f"{question_key}_O{answer['other_id']}"] = answer["text"]
                                    else:
                                        response_values[f"{question_key}"] = answer["text"]
                response_row.extend([response_values[key] for key in sorted(response_keys)])
                csv_writer.writerow(response_row)
                
        print(f"Datos convertidos y guardados en {csv_path}")

    def clean_header(self, header):
        return header.replace('[|]Validation', '')

    def parse_header(self, header):
        header = self.clean_header(header)
        if header == 'ResponseID':
            return None, None, None, None, None
        try:
            parts = header.split('.')
            page_part = parts[0]
            question_part = parts[1] if len(parts) > 1 else None
            row_part = parts[2] if len(parts) > 2 else None

            page_id = page_part[1:]

            if row_part:
                question_id = question_part[1:] if question_part else None
                row_parts = row_part.split('_')
                row_id = row_parts[0][1:]
                choice_id = row_parts[1] if len(row_parts) > 1 else None
                return page_id, question_id, choice_id, row_id, None
            else:
                question_parts = question_part.split('_') if question_part else []
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
                    return page_id, question_id, None, None, None
        except Exception as e:
            print(f"Error al analizar el encabezado '{header}': {e}")
            return None, None, None, None, None

    def clean_and_save_csv(self, csv_file):
        temp_csv_file = 'temp_cleaned.csv'
        df = pd.read_csv(csv_file)
        df.columns = [self.clean_header(col) for col in df.columns]
        df = df.drop(columns=['Type'], errors='ignore')
        df.to_csv(temp_csv_file, index=False)
        return temp_csv_file

    def process_csv_row(self, row):
        user_response_id = row['ResponseID']
        pages = {}

        for header, value in row.items():
            page_id, question_id, choice_id, row_id, other_id = self.parse_header(header)

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
                if choice_id:
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
        return user_response_id, user_data

    def csv_to_json_and_update(self, api, survey_collector_id):
        csv_path = os.path.join(self.data_folder, f"merged_responses.csv")
        temp_csv_file = self.clean_and_save_csv(csv_path)

        with open(temp_csv_file, 'r', encoding='utf-8', errors='replace') as file:
            csv_reader = csv.DictReader(file)
            
            print("Columnas en el archivo CSV:", csv_reader.fieldnames)

            for row in csv_reader:
                user_response_id, user_data = self.process_csv_row(row)
                
                print(f"Actualizando respuesta del usuario: {user_response_id}")
                print(f"Data: {user_data}")
                
                response = api.complete_response(survey_collector_id, user_response_id, user_data)
                print(f"API Response: {response}")
                print("----------------------------")
                
        print("Respuestas actualizadas con éxito.")
        os.remove(temp_csv_file)


    def xlsx_to_csv(self):
        print("Convirtiendo XLSX a CSV...")
        xlsx_path = os.path.join(self.data_folder, f"merged_responses.xlsx")
        csv_path = os.path.join(self.data_folder, f"merged_responses.csv")

        xlsx_data = pd.read_excel(xlsx_path)
        xlsx_data.to_csv(csv_path, index=False)
        print(f"Archivo CSV guardado en {csv_path}")
