from data_manager import DataManager
from surveymonkey_manager import SurveyMonkeyManager
from livepanel_manager import LivepanelManager

def main():
    surveymonkey_manager = SurveyMonkeyManager()
    
    collector_id = "430914330"
    collector_id_2 = "431991261"
    collector_id_3 = "431965638"
    collector_id_4 = "457016504"
    collector_id_5 = "432303728"
    
    data_manager = DataManager(collector_id_5)
    data_folder = data_manager.get_data_folder()
    
    livepanel_manager = LivepanelManager(data_folder)

    #SE OMITEN LAS DESCARGAS PARA TESTING
    #Obtener respuestas JSON de SurveyMonkey
    responses = surveymonkey_manager.get_responses(collector_id_5)
    data_manager.save_json_responses(responses)
    data_manager.json_to_csv(responses)
    """
    #Crear nuevo proyecto Livepanel
    project_id = livepanel_manager.create_project()

    #Encolar el proyecto para procesamiento y entrenamiento
    livepanel_manager.wait_for_status(project_id, 'CREATED')
    livepanel_manager.enqueue_project_for_processing(project_id) 

    #Descargar el dataset
    livepanel_manager.wait_for_status(project_id, 'FINISHED')  
    livepanel_manager.download_dataset(project_id)

    # Convertir el archivo XLSX a CSV
    data_manager.xlsx_to_csv()

    # Procesar el archivo CSV
    data_manager.csv_to_json_and_update(surveymonkey_manager, collector_id)
    """
if __name__ == "__main__":
    main()
