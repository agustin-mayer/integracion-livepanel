from SurveyMonkey.survey_api import SurveyMonkeyAPI
from csv_writer import CSVWriter
import os

def main():
    survey_id = "412807489"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"
    survey_api_url = "api.surveymonkey.com"

    """Usa la informacion del CSV que tiene todas las respuestas actuales del usuario y con esa informacion
    actualiza cada respuesta.(En definitiva no cambia ninguna).

    Para ver cambios: Editar el archivo surveyid_responses.csv manualmente y ejecutar export_data.py
    despues se puede importar nuevamente la data o checkear el endpoint get responses by survey id 
    para verificar los cambios"""
    
    csv_file = os.path.join("data", f"{survey_id}_responses.csv")
    payload_data = CSVWriter.process_csv(csv_file)

    api = SurveyMonkeyAPI(token,survey_api_url)
    api.complete_responses(survey_id, payload_data)
    

    print("Respuesta actualizada.")

if __name__ == "__main__":
    main()