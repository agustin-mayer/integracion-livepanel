import json
import csv

class JSONWriter:
    @staticmethod
    def write_responses(file_path, responses):
        with open(file_path, 'w') as file:
            json.dump(responses, file, indent=4)
    
    @staticmethod
    def write_final_responses(survey_id, csv_path, initial_json_path):
        # Leer datos del archivo JSON inicial
        with open(initial_json_path, 'r') as json_file:
            initial_data = json.load(json_file)

        # Leer datos del archivo CSV
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_data = [row for row in csv_reader]

        final_responses = []

        for initial_response in initial_data["data"]:
            user_response_id = initial_response["id"]
            csv_row = next((row for row in csv_data if row["User Response ID"] == user_response_id), None)

            if csv_row:
                final_response = {
                    "custom_variables": initial_response["custom_variables"],
                    "custom_value": initial_response["custom_value"],
                    "date_created": initial_response["date_created"],
                    "response_status": initial_response["response_status"],
                    "ip_address": initial_response["ip_address"],
                    "recipient_id": initial_response.get("recipient_id", ""),
                    "pages": []
                }

                for page in initial_response["pages"]:
                    final_page = {
                        "id": page["id"],
                        "questions": []
                    }
                    for question in page["questions"]:
                        final_question = {
                            "id": question["id"],
                            "variable_id": "",
                            "answers": []
                        }
                        for answer in question["answers"]:
                            choice_id = answer.get("choice_id")
                            if choice_id:
                                answer_from_csv = csv_row.get(choice_id, "")
                                final_answer = {
                                    "choice_id": choice_id,
                                    "row_id": "",
                                    "col_id": "",
                                    "other_id": "",
                                    "text": answer_from_csv
                                }
                                final_question["answers"].append(final_answer)
                            else:
                                final_answer = {
                                    "choice_id": "",
                                    "row_id": "",
                                    "col_id": "",
                                    "other_id": "",
                                    "text": answer.get("text", "")
                                }
                                final_question["answers"].append(final_answer)
                        final_page["questions"].append(final_question)
                    final_response["pages"].append(final_page)

                final_responses.append(final_response)

        # Crear la ruta del archivo de salida
        output_json_path = f"lp_data/{survey_id}_final_responses.json"

        # Escribir los datos combinados en el archivo JSON final
        with open(output_json_path, 'w', encoding='utf-8') as output_file:
            json.dump(final_responses, output_file, ensure_ascii=False, indent=4)

        return final_responses