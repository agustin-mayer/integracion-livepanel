from csv_writer import write_responses
from sm_api_access import SurveyMonkeyAPI
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    sMonkey_API = SurveyMonkeyAPI(sMonkey_token, sMonkey_API_url)
    
    sMonkey_svy_coll_id = "430914330"
    responses = sMonkey_API.get_responses(sMonkey_svy_coll_id)
    
    # Escribir las respuestas en un archivo CSV directamente desde los datos JSON
    write_responses(f"{sMonkey_svy_coll_id}_responses.csv", responses)
    print("Las respuestas se guardaron con éxito.")

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
