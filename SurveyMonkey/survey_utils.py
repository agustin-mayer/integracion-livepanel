import http.client
import json

def get_survey_details(survey_id, token):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    survey_details_url = f"/v3/surveys/{survey_id}/details"
    conn.request("GET", survey_details_url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    return data

def get_question_options(survey_id, token):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    survey_details_url = f"/v3/surveys/{survey_id}/details"
    conn.request("GET", survey_details_url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    options = {}
    for page in data["pages"]:
        for question in page["questions"]:
            if "answers" in question:
                for choice in question["answers"]["choices"]:
                    options[choice["id"]] = f"{choice['id']}"
            elif question["family"] == "open_ended":
                options[question["id"]] = f"{question['id']}"
    return options

def get_collector_responses(collector_id, token):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response_url = f"/v3/collectors/{collector_id}/responses/bulk"
    conn.request("GET", response_url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    return data