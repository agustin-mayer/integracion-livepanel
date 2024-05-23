import requests

def download_dataset(project_id, dataset_type):
    endpoint = f'https://tools.api.stg.livepanel.ai/v2/api/projects/{project_id}/datasets/get_file'
    headers = {'Authorization': 'Api-Key gAAAAABmR5TuuJhySWr5kvjPPlFH55cA-2kKec8IhL3SQ-1xQJDioFVYvIQ5i_3X_cB5w-L0_8NLe1KE1qyKme82U2LJEAR0lbZM2GJUjFkACGzFgRZp7PONZx8Xr8zHYC3MD0mf0ubN'}
    
    try:
        response = requests.get(endpoint, headers=headers, params={'type': dataset_type}, verify=False)
        response.raise_for_status()  # Esto lanzará un error si la solicitud no tuvo éxito
        with open(f'lp_data/{dataset_type}_dataset.csv', 'wb') as f:
            f.write(response.content)
        print(f'Dataset {dataset_type} descargado exitosamente.')
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

if __name__ == '__main__':
    project_id = 135  # ID del proyecto (reemplaza con tu ID real)
    dataset_types = ['Train', 'Predict', 'Predicted', 'Merged']  # Tipos de dataset
    for dataset_type in dataset_types:
        download_dataset(project_id, dataset_type)