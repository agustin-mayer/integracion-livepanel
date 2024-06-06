import csv
import xml.etree.ElementTree as ET
from app.utils import detect_encoding

def parse_survey_structure(xml_file):
    encoding = detect_encoding(xml_file)
    tree = ET.parse(xml_file, parser=ET.XMLParser(encoding=encoding))
    root = tree.getroot()
    
    headers = ['Interview']  # Encabezado de la columna de ID de entrevista
    
    # Recorrer las preguntas y crear encabezados para el CSV
    for question in root.findall('.//Question'):
        question_id = question.attrib['ID']
        headers.append(question_id)
        
        # Si la pregunta tiene modalidades, agregar encabezados adicionales
        modalities = question.find('Modalities')
        if modalities is not None:
            link_source = modalities.attrib.get('LinkSource')
            if link_source:
                linked_question_id = link_source.strip('#')
                for modality in root.findall(f'.//Question[@ID="{linked_question_id}"]//Modality'):
                    modality_id = modality.attrib['ID']
                    headers.append(f'Q{question_id}_{modality_id}')
            else:
                for modality in modalities.findall('Modality'):
                    modality_id = modality.attrib['ID']
                    headers.append(f'Q{question_id}_{modality_id}')
    
    return headers

def write_to_csv(headers, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

def main():
    # Rutas de los archivos
    xml_file_path = "./data/SurveyStructure.xml"
    csv_file_path = "train_dataset.csv" 

    # Obtener encabezados y datos
    headers = parse_survey_structure(xml_file_path)

    # Escribir al archivo CSV
    write_to_csv(headers, csv_file_path)

    print("El archivo CSV inicial con los encabezados se ha generado correctamente.")

if __name__ == "__main__":
    main()
