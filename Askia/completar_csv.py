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
    
    header_map = {header: '0' for header in headers[1:]}  # Mapeo inicial con valor predeterminado

    # Procesar respuestas directas
    for question_id in headers[1:]:
        answer = root.find(f'.//Answer[@QuestionId="{question_id}"]')
        if answer is not None:
            header_map[question_id] = '1' if answer.find('Value') is None else answer.find('Value').text

    # Procesar loops
    for loop in root.findall('.//Loop'):
        loop_question_id = loop.attrib['QuestionId']
        header_map[loop_question_id] = '1'

        # Marcar los ítems dentro del loop
        for item in loop.findall('.//Item'):
            modality_id = item.attrib['modalityId']
            item_header = f'Q{loop_question_id}_{modality_id}'
            if item_header in header_map:
                header_map[item_header] = '1'
                print(f"item{header_map[item_header]}")



    row.extend(header_map[header] for header in headers[1:])
    
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
