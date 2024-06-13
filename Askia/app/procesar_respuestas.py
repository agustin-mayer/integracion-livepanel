import xml.etree.ElementTree as ET
from app.utils import detect_encoding
import csv

def load_survey_structure(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        return headers
    
def clean_text(text):
    if text:
        return text.replace('\n', '').replace('\r', '').strip()
    return text

def process_xml_file(xml_file, headers):
    encoding = detect_encoding(xml_file)
    
    try:
        tree = ET.parse(xml_file, parser=ET.XMLParser(encoding=encoding))
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML {xml_file}: {e}")
        return None

    interview_id = root.find('Header/Id').text if root.find('Header/Id') is not None else 'Unknown'
    row = [interview_id]
    
    header_map = {header: '0' for header in headers[1:]}  # Mapeo inicial con valor predeterminado

    # Procesar respuestas directas
    for question_id in headers[1:]:
        answer = root.find(f'.//Answer[@QuestionId="{question_id}"]')
        if answer is not None:
            values = [clean_text(val.text) for val in answer.findall('Value')]
            if values:
                for value in values:
                    key = f'Q{question_id}_{value}'
                    if key in header_map:
                        header_map[key] = '1'
                    else:
                        print(f"Log: Columna para {key} no encontrada. Registrando valor en la columna principal {question_id}.")
                        header_map[question_id] = value
            else:
                header_map[question_id] = '1' if answer.find('Value') is None else clean_text(answer.find('Value').text)
                
    # Procesar loops
    for loop in root.findall('.//Loop'):
        loop_question_id = loop.attrib['QuestionId']
        for item in loop.findall('.//Item'):
            modality_id = item.attrib['modalityId']
            found_answer = False
            for answer in item.findall('.//Answer'):
                found_answer = True
                sub_question_id = answer.attrib['QuestionId']
                value = '1' if answer.find('Value') is None else clean_text(answer.find('Value').text)
                loop_header_detail = f'Q{loop_question_id}.{modality_id}.{sub_question_id}_{value}'
                loop_header = f'Q{loop_question_id}.{modality_id}_{sub_question_id}'
                if loop_header_detail in header_map:
                    header_map[loop_header_detail] = '1'
                elif loop_header in header_map:
                    header_map[loop_header] = value
                else:
                    print(f"Log: Columna para {loop_header_detail} o {loop_header} no encontrada. Registrando valor en la columna principal {loop_question_id}.")
                    header_map[loop_question_id] = value
            
            if not found_answer:
                # Si no se encuentran respuestas dentro del Item, registrar '1' en Q{loop_question_id}_{modality_id}
                loop_header = f'Q{loop_question_id}_{modality_id}'
                if loop_header in header_map:
                    header_map[loop_header] = '1'
                else:
                    print(f"Log: Columna para {loop_header} no encontrada. Registrando valor en la columna principal {loop_question_id}.")
                    header_map[loop_question_id] = '1'

    row.extend(header_map[header] for header in headers[1:])
    
    return row
