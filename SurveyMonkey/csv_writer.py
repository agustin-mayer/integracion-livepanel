import csv

def write_responses(filename, response_data, question_options):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["User Response ID"] + list(question_options.values()))
        for response in response_data["data"]:
            response_row = [response["id"]] + ["0"] * len(question_options)
            for page in response["pages"]:
                for question in page["questions"]:
                    if "answers" in question:
                        for answer in question["answers"]:
                                choice_id = answer.get("choice_id")
                                if choice_id in question_options:
                                    column_index = list(question_options.keys()).index(choice_id)
                                    response_row[column_index + 1] = "1"
                                else: #si el choice id no es una columna
                                    column_index = list(question_options.keys()).index(question["id"])
                                    text_response = ""
                                    for answer in question["answers"]:
                                        if "text" in answer:
                                            text_response += answer.get("text") + " "
                                    response_row[column_index + 1] = text_response.strip()
            csv_writer.writerow(response_row)