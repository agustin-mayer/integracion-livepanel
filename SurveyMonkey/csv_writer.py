import csv 

def write_responses(filename, response_data):
    # Crear un conjunto para almacenar todas las claves de respuesta únicas
    response_keys = set()

    # Recorrer las respuestas y almacenar las claves de respuesta únicas
    for response in response_data["data"]:
        for page in response["pages"]:
            for question in page["questions"]:
                question_id = question["id"]
                page_id = page["id"]
                question_key = f"P{page_id}.Q{question_id}"
                if "answers" in question:
                    for answer in question["answers"]:
                        choice_id = answer.get("choice_id")
                        if choice_id:
                            response_keys.add(f"{question_key}_{choice_id}")
                        elif "text" in answer:
                            response_keys.add(f"{question_key}")

    # Crear la lista de encabezados con los IDs de las preguntas
    headers = ["ResponseID"] + list(response_keys)

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        
        for response in response_data["data"]:
            response_row = [response["id"]]
            response_values = {key: "0" for key in response_keys}  # Inicializar todas las respuestas como "0"
            for page in response["pages"]:
                for question in page["questions"]:
                    question_id = question["id"]
                    page_id = page["id"]
                    question_key = f"P{page_id}.Q{question_id}"
                    if "answers" in question:
                        for answer in question["answers"]:
                            choice_id = answer.get("choice_id")
                            if choice_id:
                                response_values[f"{question_key}_{choice_id}"] = "1"
                            elif "text" in answer:
                                response_values[f"{question_key}"] = answer["text"]
            response_row.extend(response_values.values())
            csv_writer.writerow(response_row)
    print("Las respuestas se guardaron con éxito.")
