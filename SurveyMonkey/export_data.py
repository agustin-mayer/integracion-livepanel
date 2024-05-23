from sm_api import SurveyMonkeyAPI
from csv_reader import CSVReader
import os

def main():
    survey_id = "412807489"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
    survey_api_url = "api.surveymonkey.com"
    
    api = SurveyMonkeyAPI(token,survey_api_url)
    
    csv_file = os.path.join("data", f"{survey_id}_responses.csv")
    payload_data = CSVReader.create_payload(csv_file)

    api.complete_responses(survey_id, payload_data)
    

    print("Respuesta actualizada.")

if __name__ == "__main__":
    main()