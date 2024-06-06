import os
import csv
from procesar_respuestas import load_survey_structure, process_xml_file

def process_xml_files_in_folder(folder_path, csv_file):
    headers = load_survey_structure(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.xml'):
                xml_file = os.path.join(folder_path, filename)
                row = process_xml_file(xml_file, headers)
                if row:
                    writer.writerow(row)
    print("Los archivos XML se han procesado y el CSV se ha completado correctamente.")
