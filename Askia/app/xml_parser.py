import xml.etree.ElementTree as ET
from app.utils import detect_encoding
import csv

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
            modalities = question.find('.//Modalities')
            link_source = modalities.attrib.get('LinkSource')
            if link_source:
                linked_question_id = link_source.strip('#')
                for modality in root.findall(f'.//Question[@ID="{linked_question_id}"]//Modality'):
                    modality_id = modality.attrib['ID']
                    headers.append(f'Q{question_id}_{modality_id}')
            else:
                for modality in modalities.findall('.//Modality'):
                    modality_id = modality.attrib['ID']
                    headers.append(f'Q{question_id}_{modality_id}')
        else:
            headers.append(question_id)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
