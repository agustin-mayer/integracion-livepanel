import survey_utils
import csv_writer

def main():
    survey_id = "412807489"
    collector_id = "430914330"
    token = "rFQ8cH5B5PWvIzyh2svCaRRENKcGqvgPvFqgJZucojFF4gSBsu6fzXZ2Z2A5Vy3uSjq4rZgsMznPQ.W9fakshPiaoOCyBsLv5pUqz1gkVqSeUMbmgmPnToA-ttzQ4fiD"

    question_options = survey_utils.get_question_options(survey_id, token)
    responses_data = survey_utils.get_collector_responses(collector_id, token)

    csv_writer.write_responses("survey_responses.csv", responses_data, question_options)

    print("Archivo CSV generado exitosamente.")

if __name__ == "__main__":
    main()
