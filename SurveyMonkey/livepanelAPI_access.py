import http.client
import json
import os
from dotenv import load_dotenv
import ssl

# Desactiva la verificación del certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

class LivepanelAPI:
    def __init__(self, token, survey_api_url):
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"{token}",
            "Content-Type": "application/json"
        }
        self.conn = http.client.HTTPSConnection(survey_api_url)

    def _api_request(self, method, url, payload=None):
        full_url = f"https://{self.conn.host}{url}"
        print(f"Making request to: {full_url}")

        if payload is not None:
            payload = json.dumps(payload)
            self.conn.request(method, url, headers=self.headers, body=payload)
        else:
            self.conn.request(method, url, headers=self.headers)
        response = self.conn.getresponse()
        response_data = response.read()
        
        # Imprimir el estado de la respuesta para depuración
        print(f"Response status: {response.status}")

        # Verificar si la respuesta está vacía
        if not response_data:
            raise ValueError("Empty response received from the API")

        if response.status != 200:
            raise ValueError(f"API request failed with status {response.status}: {response_data.decode()}")

        return response_data

    def create_project(self, payload): 
        url = f"/v2/projects/"
        return self._api_request("POST", url, payload)

    def get_project(self, project_id):
        url = f"/projects/{project_id}"
        data = self._api_request("GET", url).decode()
        
        # Define the directory to save the datasets
        save_dir = 'datasets'
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the JSON response to a file
        file_path = os.path.join(save_dir, f'project_{project_id}.json')
        with open(file_path, 'w') as file:
            json.dump(json.loads(data), file, indent=4)
        
        print(f'Dataset saved to {file_path}')
        return data

    def download_dataset(self, project_id, file_type):
        url = f"/v2/api/projects/{project_id}/datasets/get_file?type={file_type}"
        data = self._api_request("GET", url)
        
        # Define the directory to save the datasets
        save_dir = 'datasets'
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the binary response to a file
        file_path = os.path.join(save_dir, f'{project_id}_{file_type}.bin')
        with open(file_path, 'wb') as file:
            file.write(data)
        
        print(f'Dataset {file_type} saved to {file_path}')
        return file_path
