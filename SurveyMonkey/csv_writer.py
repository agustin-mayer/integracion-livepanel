import csv
import json

def write_responses(filename, response_data):
    response_keys = set()
    choice_questions = set()

    # Se obtienen los ID de las preguntas para el encabezado de columna
    for response in response_data["data"]:
        for page in response["pages"]:
            for question in page["questions"]:
                question_id = question["id"]
                page_id = page["id"]
                question_key = f"P{page_id}.Q{question_id}"
                if "answers" in question:
                    for answer in question["answers"]:
                        if "choice_id" in answer:
                            response_keys.add(f"{question_key}_{answer['choice_id']}")
                            choice_questions.add(question_key)
                        elif "text" in answer:
                            if "row_id" in answer:
                                response_keys.add(f"{question_key}_R{answer['row_id']}")
                            else:
                                response_keys.add(f"{question_key}")

    
    headers = ["ResponseID"] + sorted(list(response_keys))

    #se cargan las respuestas en el CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
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
                                response_values[f"{question_key}_{answer['choice_id']}"] = "1"
                            elif "text" in answer:
                                if "row_id" in answer:
                                    response_values[f"{question_key}_R{answer['row_id']}"] = answer["text"]
                                else:
                                    response_values[f"{question_key}"] = answer["text"]
            response_row.extend([response_values[key] for key in sorted(response_keys)])
            csv_writer.writerow(response_row)
    print("Las respuestas se guardaron con éxito.")