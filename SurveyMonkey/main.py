from csv_writer import json_to_csv
from json_writer import save_json_responses, csv_to_json_and_update
from wrapper import SurveyMonkeyAPI
from Livepanel_SDK import LivepanelAuth, APIAccess
from dotenv import load_dotenv
import os
import time
import chardet, csv
import pandas as pd


def get_livepanel_API_access():
        
        livepanel_API_key = os.getenv('LIVEPANEL_API_KEY')
        auth = LivepanelAuth(livepanel_API_key)
        livepanel_API_access = APIAccess(auth)
        return livepanel_API_access
    

def main():

    load_dotenv()
    sMonkey_token = os.getenv("SURVEYMONKEY_API_TOKEN")
    sMonkey_API_url = "api.surveymonkey.com"
    sMonkey_API = SurveyMonkeyAPI(sMonkey_token, sMonkey_API_url)
    livepanel_API_access = get_livepanel_API_access()

    collector_id_1 = "430914330"
    collector_id_2 = "431991261"
    collector_id_3 = "431965638"
    collector_id_4 = "457016504"

    
    responses = sMonkey_API.get_responses(collector_id_3)
    save_json_responses(collector_id_3, responses)
    json_to_csv(collector_id_3, responses)

    
    print(f"Creando nuevo proyecto en Livepanel..")
    datafile = f"data/{collector_id_3}/original_responses.csv"
    response = livepanel_API_access.create_project(datafile)
    print(f"Create Project Response: {response}")
    project_id = response["id"]

    while True:
        project = livepanel_API_access.get_project(project_id)
        project_name = project['name']
        project_status = project['state']
        print(f"Estado del proyecto: {project_status}")

        if project_status == 'CREATED':
            print(f"El proyecto {project_name} esta listo para encolar.")
            break
        else:
            # Espera 15 segundos antes de la próxima verificación
            time.sleep(15)
    
    print(f"Encolando proyecto para procesamiento..")
    livepanel_API_access.enqueue_project_for_processing(project_id)
    print(f"Enqueue Project for Procesing Response: {response}")


    while True:
        project = livepanel_API_access.get_project(project_id)
        project_name = project['name']
        project_status = project['state']
        print(f"Estado del proyecto: {project_status}")

        if project_status == 'FINISHED':
            print(f"El proyecto {project_name} ha sido procesado.")
            break
        else:
            # Espera 15 segundos antes de la próxima verificación
            time.sleep(15)
    
    
    print("Descargando el dataset..")
    save_path_xlsx = f"data/{collector_id_3}/merged_responses.xlsx"
    csv_content = livepanel_API_access.download_dataset(199, 'Merged')

    with open(save_path_xlsx, 'wb') as file:
        file.write(csv_content)
    print(f"Dataset guardado en {save_path_xlsx}")

    # Convertir el archivo XLSX a CSV
    print("Convirtiendo XLSX a CSV...")
    save_path_csv = f"data/{collector_id_3}/merged_responses.csv"
    xlsx_data = pd.read_excel(save_path_xlsx)
    xlsx_data.to_csv(save_path_csv, index=False)
    print(f"Archivo CSV guardado en {save_path_csv}")

    # Procesar el archivo CSV
    print("Convirtiendo las nuevas respuestas de CSV a JSON..")
    csv_to_json_and_update(save_path_csv, sMonkey_API, collector_id_3)
    

if __name__ == "__main__":
    main()
