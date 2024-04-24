from survey_api import SurveyAPI
from csv_writer import CSVWriter

def main():
    survey_id = "412807489"
    collector_id = "430914330"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

    api = SurveyAPI(token)
    question_options = api.get_question_options(survey_id)
    responses_data = api.get_collector_responses(collector_id)

    CSVWriter.write_responses("survey_responses.csv", responses_data, question_options)
    CSVWriter.write_choice_options("survey_choices.csv", question_options)
    print("Archivos CSV generados exitosamente.")

if __name__ == "__main__":
    main()