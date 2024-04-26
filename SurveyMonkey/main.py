from survey_api import SurveyAPI
from csv_writer import CSVWriter

def main():
    survey_id = "412807489"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

    api = SurveyAPI(token)
    options = api.get_options(survey_id)
    responses = api.get_responses(survey_id)

    CSVWriter.write_responses(f"./data/{survey_id}_responses.csv", responses, options)
    CSVWriter.write_choice_options(f"./data/{survey_id}_options.csv", options)
    print("Archivos CSV generados exitosamente.")

if __name__ == "__main__":
    main()