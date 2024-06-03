import csv

def update_csv_with_responses(response_data, csv_file):
    # Agregar respuestas al archivo CSV
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(response_data)
