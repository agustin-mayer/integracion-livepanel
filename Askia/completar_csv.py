import os
import csv
import xml.etree.ElementTree as ET
from app.utils import detect_encoding

def load_survey_structure(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        return headers

def process_xml_file(xml_file, headers):
    encoding = detect_encoding(xml_file)  # Utilizamos la función detect_encoding del script utils
    
    try:
        tree = ET.parse(xml_file, parser=ET.XMLParser(encoding=encoding))
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML {xml_file}: {e}")
        return None

    interview_id = root.find('Header/Id').text
    row = [interview_id]
    
    for question_id in headers[1:]:
        value = '0'  # Valor predeterminado si no se menciona la pregunta
        
        answer = root.find(f'.//Answer[@QuestionId="{question_id}"]')
        if answer is not None:
            value = '1' if answer.find('Value') is None else answer.find('Value').text
        
        row.append(value)
    
    return row


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

def main():
    csv_file = "train_dataset.csv"  # Nombre del archivo CSV a completar
    folder_path = "./data/xml_responses"  # Ruta de la carpeta con los archivos XML
    
    process_xml_files_in_folder(folder_path, csv_file)

    print("Los archivos XML se han procesado y el CSV se ha completado correctamente.")

if __name__ == "__main__":
    main()
