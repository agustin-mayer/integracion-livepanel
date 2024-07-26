import os
import time
from dotenv import load_dotenv
from Livepanel_SDK import LivepanelAuth, APIAccess
import uuid

class LivepanelManager:
    def __init__(self, data_folder):
        load_dotenv()
        self.api = self.get_livepanel_API_access()
        self.data_folder = data_folder

    def get_livepanel_API_access(self):
        livepanel_API_key = os.getenv('LIVEPANEL_API_KEY')
        auth = LivepanelAuth(livepanel_API_key)
        return APIAccess(auth)
    
    def create_project(self):
        print("Creando nuevo proyecto en Livepanel..")
        
        datafile = os.path.join(self.data_folder, f"original_responses.csv")
        project_name = f"Proyecto_{uuid.uuid4().hex}"
        
        response = self.api.create_project(datafile, project_name)
        
        print(f"Create Project Response: {response}")
        return response["id"]

    def wait_for_status(self, project_id, desired_status, check_interval=15):
        while True:
            project = self.api.get_project(project_id)
            project_name = project['name']
            project_status = project['state']

            if project_status == desired_status:
                print(f"El proyecto {project_name} alcanzo el estado: {project_status}.")
                break
            else:
                print(f"Estado del proyecto: {project_status}")
                time.sleep(check_interval)
    
    def enqueue_project_for_processing(self, project_id):
        print("Encolando proyecto para procesamiento..")
        response = self.api.enqueue_project_for_processing(project_id)
        print(f"Enqueue Project for Processing Response: {response}")

    def download_dataset(self, project_id):
        print("Descargando el dataset..")
        
        save_path_xlsx = os.path.join(self.data_folder, f"merged_responses.xlsx")
        csv_content = self.api.download_dataset(project_id, 'Merged')
        with open(save_path_xlsx, 'wb') as file:
            file.write(csv_content)
        print(f"Dataset guardado en {save_path_xlsx}")
