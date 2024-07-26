from data_manager import DataManager
from surveymonkey_manager import SurveyMonkeyAPI
from livepanel_manager import LivepanelManager

def main():
    sMonkey_API = SurveyMonkeyAPI()
    
    collector_id = "430914330"
    collector_id_2 = "431991261"
    collector_id_3 = "431965638"
    collector_id_4 = "457016504"
    
    data_manager = DataManager()

    #Obtener respuestas JSON de SurveyMonkey
    responses = sMonkey_API.get_responses(collector_id)
    data_manager.save_json_responses(collector_id, responses)
    data_manager.json_to_csv(collector_id, responses)

    #Crear nuevo proyecto Livepanel
    livepanel_manager = LivepanelManager()

    datafile = f"data/{collector_id}/original_responses.csv"
    project_id = livepanel_manager.create_project(datafile)

    #Encolar el proyecto para procesamiento y entrenamiento
    livepanel_manager.wait_for_status(project_id, 'CREATED')
    livepanel_manager.enqueue_project_for_processing(project_id) 

    #Descargar el dataset
    livepanel_manager.wait_for_status(project_id, 'FINISHED')  
    save_path_xlsx = f"data/{collector_id}/merged_responses.xlsx"
    livepanel_manager.download_dataset(save_path_xlsx, project_id)

    # Convertir el archivo XLSX a CSV
    save_path_csv = f"data/{collector_id}/merged_responses.csv"
    data_manager.xlsx_to_csv(save_path_xlsx, save_path_csv)

    # Procesar el archivo CSV
    data_manager.csv_to_json_and_update(save_path_csv, sMonkey_API, collector_id)
    
if __name__ == "__main__":
    main()
