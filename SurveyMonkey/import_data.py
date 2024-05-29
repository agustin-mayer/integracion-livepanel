from sm_api_access import SurveyMonkeyAPI
from option_processor import process_options
from json_handler import JSONHandler
from csv_handler import CSVHandler
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    sMonkey_API = SurveyMonkeyAPI(sMonkey_token,sMonkey_API_url)
    
    sMonkey_svy_coll_id = "430914330"
    responses = sMonkey_API.get_responses(sMonkey_svy_coll_id)
    
    sMonkey_svy_id = "412807489"
    survey_data = sMonkey_API.get_options(sMonkey_svy_id)
    CSVHandler.write_options(f"./sm_data/{sMonkey_svy_coll_id}_options.csv", survey_data)
    
    options = process_options(survey_data)
    CSVHandler.write_responses(f"./sm_data/{sMonkey_svy_coll_id}_responses.csv", responses, options)
    JSONHandler.write_responses(f"./sm_data/{sMonkey_svy_coll_id}_responses.json", responses)
    
    print("Archivos CSV y JSON generados exitosamente.")

    """
    livepanel_token = os.getenv("LIVEPANEL_API_TOKEN")
    livepanel_API_url = "tools.api.livepanel.ai"
    livepanel_API = LivepanelAPI(livepanel_token,livepanel_API_url)

    payload = f"./sm_data/{sMonkey_svy_coll_id}_responses.csv"
    livepanelAPI.create_project(train_csv)

    print("Se ha creado un nuevo proyecto en Livepanel.")
    """

if __name__ == "__main__":
    main()