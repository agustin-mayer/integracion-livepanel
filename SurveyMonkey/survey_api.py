import http.client
import json

class SurveyAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.conn = http.client.HTTPSConnection("api.surveymonkey.com")

    def _api_request(self, method, url):
        self.conn.request(method, url, headers=self.headers)
        response = self.conn.getresponse()
        data = json.loads(response.read())
        return data

    def get_survey_details(self, survey_id):
        url = f"/v3/surveys/{survey_id}/details"
        return self._api_request("GET", url)

    def get_options(self, survey_id):
        url = f"/v3/surveys/{survey_id}/details"
        data = self._api_request("GET", url)
        options = {}
        for page in data["pages"]:
            for question in page["questions"]:
                if "answers" in question:
                    for choice in question["answers"]["choices"]:
                        choice_id = choice["id"]
                        choice_text = choice.get("text", f"Choice {choice_id}")
                        options[choice_id] = choice_text
                elif question["family"] == "open_ended":
                    question_id = question["id"]
                    question_text = question["headings"][0]["heading"]
                    options[question_id] = question_text
        return options

    def get_responses(self, survey_id):
        url = f"/v3/surveys/{survey_id}/responses/bulk"
        return self._api_request("GET", url)
