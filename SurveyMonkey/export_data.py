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

    collector_id_1 = "430914330"
    collector_id_2 = "431991261"
    collector_id_3 = "431965638"
    collector_id_4 = "457016504" 

    csv_file = f'./data/{collector_id_3}/original_responses.csv'

    csv_to_json_and_update(csv_file, api, collector_id_3)
    
    
    
if __name__ == "__main__":
    main()