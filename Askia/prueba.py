import xml.etree.ElementTree as ET
import csv
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def parse_xml_to_csv_headers_only(xml_file, csv_file):
    encoding = detect_encoding(xml_file)
    with open(xml_file, 'r', encoding=encoding) as file:
        xml_content = file.read().replace('encoding="Unicode"', 'encoding="UTF-8"')
    
    root = ET.fromstring(xml_content)
    headers = ['USER']

    for question in root.findall('.//Question'):
        question_id = question.attrib['ID']
        element_type = question.attrib.get('ElementType')
        
        if element_type == 'loop':
            for modality in question.findall('.//Modality'):
                modality_id = modality.attrib['ID']
                headers.append(f'Q{question_id}_{modality_id}')
        else:
            headers.append(question_id)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

xml_file = './SurveyStructure.xml'
csv_file = './output.csv'

parse_xml_to_csv_headers_only(xml_file, csv_file)
