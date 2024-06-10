from sMonkeyAPI_access import SurveyMonkeyAPI
from livepanelAPI_access import LivepanelAPI
from json_writer import csv_to_json_and_update
from dotenv import load_dotenv
import os


def main():
    """
    livepanel_token = os.getenv("LIVEPANEL_API_TOKEN")
    livepanel_API_url = "tools.api.livepanel.ai"
    livepanel_API = LivepanelAPI(livepanel_token,livepanel_API_url)
    payload = livepanel_API.get_project(131)
    print("Se obtuvieron las respuestas completas desde Livepanel.")    """
    
    load_dotenv()
    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    api = SurveyMonkeyAPI(sMonkey_token, sMonkey_API_url)

    survey_collector_id = "430914330" 
    csv_file = f'{survey_collector_id}_responses.csv' #luego payload de livepanel

    csv_to_json_and_update(csv_file, api, survey_collector_id)

    
    print("Respuestas actualizadas con exito.")
    
    
if __name__ == "__main__":
    main()