from sm_api import SurveyMonkeyAPI
from csv_writer import CSVWriter
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    smonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    smonkey_api_url = "api.surveymonkey.com"
    smonkey_survey_id = "412807489"
    
    api = SurveyMonkeyAPI(smonkey_token,smonkey_api_url)
    options = api.get_options(smonkey_survey_id)
    responses = api.get_responses(smonkey_survey_id)

    CSVWriter.write_responses(f"./sm_data/{smonkey_survey_id}_responses.csv", responses, options)
    CSVWriter.write_options(f"./sm_data/{smonkey_survey_id}_options.csv", options)
    print("Archivos CSV generados exitosamente.")

if __name__ == "__main__":
    main()