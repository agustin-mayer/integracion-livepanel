import csv

class CSVHandler:
    @staticmethod
    def write_responses(filename, response_data, question_options):
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["user_response_id", "page_id", "question_id", "choice_id", "response"])
            for response in response_data["data"]:
                user_id = response["id"]
                user_responses = set()  # Conjunto para rastrear respuestas únicas del usuario
                for page in response["pages"]:
                    page_id = page["id"]
                    for question in page["questions"]:
                        question_id = question["id"]
                        for choice_id in question_options.keys():
                            page_id_option, question_id_option, choice = choice_id
                            if page_id_option == page_id and question_id_option == question_id:
                                # Verificar si esta respuesta ya ha sido registrada para evitar duplicados
                                if choice_id in user_responses:
                                    continue
                                respuesta_usuario = "0"  # Por defecto, la opción no ha sido seleccionada
                                for answer in question["answers"]:
                                    if answer.get("choice_id") == choice:
                                        if answer.get("text", ""):
                                            respuesta_usuario =answer.get("text", "")
                                            choice = "no_choices"
                                        else:
                                            respuesta_usuario = "1" # Marcar como seleccionada si el usuario eligió esta opción
                                        break
                                # Escribir la fila en el CSV
                                csv_writer.writerow([user_id, page_id, question_id, choice, respuesta_usuario])
                                user_responses.add(choice_id)


    @staticmethod
    def write_options(filename, question_options):
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["(PageID, QuestionID, ChoiceID)", "Option text"])
            for choice_id, option in question_options.items():
                csv_writer.writerow([choice_id, option])


    @staticmethod
    def process_csv(csv_file):
        responses = {}
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                response_id = row['user_response_id']
                page_id = row['page_id']
                question_id = row['question_id']
                choice_id = row['choice_id']
                response = row['response']
                if response_id not in responses:
                    responses[response_id] = {
                        'ip_address': '127.0.0.1',
                        'pages': []
                    }
                page = next((p for p in responses[response_id]['pages'] if p['id'] == page_id), None)
                if not page:
                    page = {'id': page_id, 'questions': []}
                    responses[response_id]['pages'].append(page)
                question = next((q for q in page['questions'] if q['id'] == question_id), None)
                if not question:
                    question = {'id': question_id, 'answers': []}
                    page['questions'].append(question)
                if choice_id != 'no_choices':
                    question['answers'].append({'choice_id': choice_id})
                else:
                    question['answers'].append({'text': response})
        return responses