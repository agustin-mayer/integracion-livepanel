import csv
import xml.etree.ElementTree as ET
from app.utils import detect_encoding

def get_modalities_recursive(question_id, root):
    modalities = []
    question = root.find(f'.//Question[@ID="{question_id}"]')
    
    if question is not None:
        modalities_element = question.find('Modalities')
        if modalities_element is not None:
            link_source = modalities_element.attrib.get('LinkSource')
            if link_source:
                linked_question_id = link_source.strip('#')
                modalities += get_modalities_recursive(linked_question_id, root)
            else:
                for modality in modalities_element.findall('Modality'):
                    modality_id = modality.attrib.get('ID')
                    if modality_id:
                        modalities.append(modality_id)
                    else:
                        print(f"Modality without ID attribute in question {question_id}")
    
    return modalities

def parse_survey_structure(xml_file):
    encoding = detect_encoding(xml_file)
    tree = ET.parse(xml_file, parser=ET.XMLParser(encoding=encoding))
    root = tree.getroot()
    
    headers = ['Interview']  # Encabezado de la columna de ID de entrevista
    
    # Recorrer las preguntas y crear encabezados para el CSV
    for question in root.findall('.//Question'):
        question_id = question.attrib.get('ID')
        if not question_id:
            print(f"Question without ID attribute found")
            continue
        
        headers.append(question_id)
        
        # Obtener modalidades recursivamente si existen
        modalities = get_modalities_recursive(question_id, root)
        for modality_id in modalities:
            headers.append(f'Q{question_id}_{modality_id}')
        
        # Si la pregunta es un loop, agregar encabezados para las preguntas internas y submodalidades
        if question.attrib.get('ElementType') == 'loop':
            for modality_id in modalities:
                headers.append(f'Q{question_id}_{modality_id}')  # Encabezado para la modalidad dentro del loop
                for sub_question in question.findall('.//Questions/Question'):
                    sub_question_id = sub_question.attrib.get('ID')
                    if not sub_question_id:
                        print(f"Subquestion without ID attribute found in question {question_id}")
                        continue
                    headers.append(f'Q{question_id}.{modality_id}_{sub_question_id}')
                    # Obtener submodalidades si existen
                    for submodality in sub_question.findall('.//Modality'):
                        submodality_id = submodality.attrib.get('ID')
                        if submodality_id:
                            headers.append(f'Q{question_id}.{modality_id}.{sub_question_id}_{submodality_id}')
                        else:
                            print(f"Submodality without ID attribute found in subquestion {sub_question_id} of question {question_id}")
    
    return headers

def write_to_csv(headers, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

def crear_encabezados(xml_file_path, csv_file_path):
    headers = parse_survey_structure(xml_file_path)
    write_to_csv(headers, csv_file_path)
    print("El archivo CSV inicial con los encabezados se ha generado correctamente.")
