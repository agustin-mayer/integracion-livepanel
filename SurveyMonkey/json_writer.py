import csv

def parse_header(header):
    if header == 'ResponseID':
        return None, None, None
    try:
        page_part, question_part = header.split('.')
        page_id = page_part[1:]
        question_parts = question_part.split('_')
        question_id = question_parts[0][1:]
        choice_id = question_parts[1] if len(question_parts) > 1 else ""
        return page_id, question_id, choice_id
    except ValueError:
        return None, None, None

def csv_to_json_and_update(csv_file, api, survey_collector_id):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            user_response_id = row['ResponseID']
            pages = {}
            
            for header, value in row.items():
                page_id, question_id, choice_id = parse_header(header)
                
                if not page_id or not question_id:
                    continue
                
                # Skip answers with value 0 or empty string
                if value == '0' or value.strip() == '':
                    continue
                
                if page_id not in pages:
                    pages[page_id] = {"id": page_id, "questions": []}
                
                question = next((q for q in pages[page_id]["questions"] if q["id"] == question_id), None)
                
                if not question:
                    question = {"id": question_id, "answers": []}
                    pages[page_id]["questions"].append(question)
                
                if choice_id:
                    question["answers"].append({"choice_id": choice_id})
                else:
                    question["answers"].append({"text": value})
            
            user_data = {"pages": list(pages.values())}
            
            print(f"Updating response for user {user_response_id}")
            print(f"Data: {user_data}")
            
            response = api.complete_response(survey_collector_id, user_response_id, user_data)
            print(f"API Response: {response}")
            print("----------------------------")