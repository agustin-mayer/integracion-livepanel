import csv

class CSVHandler:
    @staticmethod
    def write_responses(filename, response_data, question_options):
        # Crear la lista de encabezados con los IDs de las preguntas/opciones
        headers = ["User Response ID"] + [key[1] if key[1] else key[0] for key in question_options.keys()]
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)
            
            for response in response_data["data"]:
                response_row = [response["id"]] + ["0"] * len(question_options)
                for page in response["pages"]:
                    for question in page["questions"]:
                        if "answers" in question:
                            for answer in question["answers"]:
                                choice_id = answer.get("choice_id")
                                if choice_id:
                                    # Buscar la posición del choice_id en la lista de encabezados
                                    try:
                                        column_index = headers.index(choice_id)
                                        response_row[column_index] = "1"
                                    except ValueError:
                                        print(f"Choice ID {choice_id} not found in question_options")
                                elif "text" in answer:
                                    # Es una pregunta de texto libre
                                    try:
                                        column_index = headers.index(question["id"])
                                        response_row[column_index] = answer["text"]
                                    except ValueError:
                                        print(f"Question ID {question['id']} for open-ended response not found in question_options")
                csv_writer.writerow(response_row)

    @staticmethod
    def write_options(filename, data):
        options = {}
        for page in data["pages"]:
            page_id = page["id"]
            for question in page["questions"]:
                question_id = question["id"]
                if "answers" in question:
                    for choice in question["answers"]["choices"]:
                        choice_id = choice["id"]
                        choice_text = choice.get("text", f"Choice {choice_id}")
                        options[question_id, choice_id] = choice_text
                elif question["family"] == "open_ended":
                    question_text = question["headings"][0]["heading"]
                    options[(question_id, None)] = question_text 
        
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Choice ID", "Option"])
            for (question_id, choice_id), option in options.items():
                csv_writer.writerow([choice_id if choice_id else question_id, option])
