import os
import csv
import xml.etree.ElementTree as ET
from app.utils import detect_encoding

def load_responses_to_csv(xml_responses_folder, csv_file):
    # Verificar si el archivo CSV ya existe
    csv_exists = os.path.exists(csv_file)

    # Obtener todos los IDs de pregunta y modalidades posibles
    all_question_ids = set()
    all_modalities = set()
    
    # Primera pasada para recolectar todos los IDs de preguntas y modalidades
    for filename in os.listdir(xml_responses_folder):
        if filename.endswith(".xml"):
            xml_file = os.path.join(xml_responses_folder, filename)
            with open(xml_file, 'r', encoding=detect_encoding(xml_file)) as file:
                xml_content = file.read()
            root = ET.fromstring(xml_content)
            
            # Recoger todas las preguntas simples
            for answer in root.findall('.//Answer'):
                question_id = answer.attrib['QuestionId']
                all_question_ids.add(question_id)
            
            # Recoger todas las preguntas tipo Loop y sus modalidades
            for loop in root.findall('.//Loop'):
                question_id = loop.attrib['QuestionId']
                all_question_ids.add(question_id)
                for item in loop.findall('.//Item'):
                    modality_id = item.attrib['modalityId']
                    all_modalities.add(f"Q{question_id}_{modality_id}")
    
    # Escribir las respuestas en el archivo CSV
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['InterviewID'] + sorted(all_question_ids) + sorted(all_modalities))
        if not csv_exists:
            writer.writeheader()  # Escribir encabezados solo si es un nuevo archivo CSV

        # Segunda pasada para procesar y escribir las respuestas
        for filename in os.listdir(xml_responses_folder):
            if filename.endswith(".xml"):
                xml_file = os.path.join(xml_responses_folder, filename)
                with open(xml_file, 'r', encoding=detect_encoding(xml_file)) as file:
                    xml_content = file.read()
                root = ET.fromstring(xml_content)
                
                # Extraer el ID de la encuesta
                interview_id = root.find('.//Header/Id').text
                
                # Inicializar diccionario de respuestas para esta entrevista con 0s
                interview_responses = {qid: '0' for qid in all_question_ids}
                interview_responses.update({modality: '0' for modality in all_modalities})
                interview_responses['InterviewID'] = interview_id

                # Extraer las respuestas de cada Answer
                for answer in root.findall('.//Answer'):
                    question_id = answer.attrib['QuestionId']
                    value = answer.findtext('Value')
                    if value:
                        interview_responses[question_id] = value
                
                # Extraer las respuestas de cada Loop
                for loop in root.findall('.//Loop'):
                    question_id = loop.attrib['QuestionId']
                    for item in loop.findall('.//Item'):
                        modality_id = item.attrib['modalityId']
                        interview_responses[f"Q{question_id}_{modality_id}"] = '1'

                writer.writerow(interview_responses)

    print("Responses successfully loaded to CSV.")
