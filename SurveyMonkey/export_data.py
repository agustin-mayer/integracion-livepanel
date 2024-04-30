from survey_api import SurveyAPI
from csv_writer import CSVWriter

def main():
    survey_id = "412807489"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
    survey_api_url = "api.surveymonkey.com"
    
    api = SurveyAPI(token,survey_api_url)
    options = api.get_options(survey_id)
    responses = api.complete_response(survey_id, response_id, payload)

    print("Respuesta actualizada.")

if __name__ == "__main__":
    main()