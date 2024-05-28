from sm_api import SurveyMonkeyAPI
from csv_reader import CSVReader
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    smonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    smonkey_api_url = "api.surveymonkey.com"
    smonkey_survey_id = "412807489"
    
    api = SurveyMonkeyAPI(smonkey_token,smonkey_api_url)
    
    csv_file = os.path.join("sm_data", f"{smonkey_survey_id}_responses.csv")
    payload_data = CSVReader.create_payload(csv_file)

    api.complete_responses(smonkey_survey_id, payload_data)
    

    print("Respuesta actualizada.")

if __name__ == "__main__":
    main()