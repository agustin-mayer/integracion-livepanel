from csv_writer import write_responses
from json_writer import save_original_responses
from sMonkeyAPI_access import SurveyMonkeyAPI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    sMonkey_API = SurveyMonkeyAPI(sMonkey_token, sMonkey_API_url)
    
    sMonkey_svy_coll_id = "430914330"
    
    directory = f"./data/{sMonkey_svy4_coll_id}/"

    responses = sMonkey_API.get_responses(sMonkey_svy4_coll_id)

    if not os.path.exists(directory):
        os.makedirs(directory)

    save_original_responses(os.path.join(directory, "original_responses.json"), responses)
    write_responses(os.path.join(directory, "original_responses.csv"), responses)

    """
    livepanel_token = os.getenv("LIVEPANEL_API_TOKEN")
    livepanel_API_url = "tools.api.livepanel.ai"
    livepanel_API = LivepanelAPI(livepanel_token,livepanel_API_url)
    payload = f"./sm_data/{sMonkey_svy_coll_id}_responses.csv"
    livepanelAPI.create_project(train_csv)
    print("Se ha creado un nuevo proyecto en Livepanel.") """

if __name__ == "__main__":
    main()
