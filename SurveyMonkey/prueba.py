import csv
import json

def parse_header(header):
    try:
        page_part, question_part = header.split('.')
        page_id = page_part[1:]
        question_parts = question_part.split('_')
        question_id = question_parts[0][1:]
        choice_id = question_parts[1] if len(question_parts) > 1 else ""
        return page_id, question_id, choice_id
    except ValueError:
        return None, None, None

def csv_to_json(csv_file):
    json_data = []

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        for row in csv_reader:
            user_response_id = row[0]
            pages = {}
            
            for i, value in enumerate(row[1:], start=1):
                header = headers[i]
                page_id, question_id, choice_id = parse_header(header)

                if not page_id or not question_id:
                    print(f"Skipping invalid header at column {i}: {header}")
                    continue
                
                if page_id not in pages:
                    pages[page_id] = {"id": page_id, "questions": []}
                
                question_exists = False
                for question in pages[page_id]["questions"]:
                    if question["id"] == question_id:
                        question["answers"].append({
                            "choice_id": choice_id,
                            "row_id": "",
                            "col_id": "",
                            "other_id": "",
                            "text": value
                        })
                        question_exists = True
                        break
                
                if not question_exists:
                    pages[page_id]["questions"].append({
                        "id": question_id,
                        "variable_id": "",
                        "answers": [{
                            "choice_id": choice_id,
                            "row_id": "",
                            "col_id": "",
                            "other_id": "",
                            "text": value
                        }]
                    })
            
            user_data = {"User Response ID": user_response_id, "pages": list(pages.values())}
            json_data.append(user_data)
    
    return json_data

csv_file = '430914330_responses.csv'
json_data = csv_to_json(csv_file)

with open('output.json', 'w') as outfile:
    json.dump(json_data, outfile, indent=2)
