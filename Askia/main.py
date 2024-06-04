# main.py

import os
from app.xml_parser import parse_xml_to_csv_headers_only
from app.response_loader import load_responses_to_csv

xml_file = './data/SurveyStructure.xml'
csv_file = './data/output.csv'
xml_responses_folder = './data/xml_responses'

# Generar los encabezados del CSV
parse_xml_to_csv_headers_only(xml_file, csv_file)

# Cargar las respuestas en el CSV
load_responses_to_csv(xml_responses_folder, csv_file)
