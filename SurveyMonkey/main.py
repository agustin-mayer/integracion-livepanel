import json
from json_to_csv import write_responses

def main():
    # Cargar el archivo JSON de las respuestas
    filename = './sm_data/430914330_responses.json'
    with open(filename, "r", encoding="utf-8") as file:
        response_data = json.load(file)

    # Escribir las respuestas en un archivo CSV
    write_responses("responses.csv", response_data)

if __name__ == "__main__":
    main()
