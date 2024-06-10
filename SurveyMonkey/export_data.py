from sMonkeyAPI_access import SurveyMonkeyAPI
from livepanelAPI_access import LivepanelAPI
from json_writer import JSONWriter
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    """
    livepanel_token = os.getenv("LIVEPANEL_API_TOKEN")
    livepanel_API_url = "tools.api.livepanel.ai"
    livepanel_API = LivepanelAPI(livepanel_token,livepanel_API_url)

    payload = livepanel_API.get_project(131)

    print("Se obtuvieron las respuestas completas desde Livepanel.")
    """

    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    sMonkey_API = SurveyMonkeyAPI(sMonkey_token,sMonkey_API_url)
    
    sMonkey_svy_coll_id = "430914330"
    csv_path =f"lp_data/{sMonkey_svy_coll_id}_predicted.csv"
    initial_json_path = f"sm_data/{sMonkey_svy_coll_id}_responses.json"
    payload_data = JSONWriter.write_final_responses(sMonkey_svy_coll_id, csv_path, initial_json_path)

    #print(payload_data)
    sMonkey_API.post_responses(sMonkey_svy_coll_id, payload_data)

    
    print("Respuestas actualizadas con exito.")
    
    
if __name__ == "__main__":
    main()