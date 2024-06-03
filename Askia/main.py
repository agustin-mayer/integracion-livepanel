from app.xml_parser import parse_xml_to_csv_headers_only#, parse_responses_and_update_csv

def main():
    xml_file = './data/SurveyStructure.xml'
    csv_file = './data/output.csv'

    # Crear CSV con encabezados
    parse_xml_to_csv_headers_only(xml_file, csv_file)

    # Completar CSV con respuestas de múltiples archivos XML
    response_files = ['./data/response1.xml', './data/response2.xml']  # Agrega más archivos si es necesario
   # parse_responses_and_update_csv(response_files, csv_file)

if __name__ == "__main__":
    main()
