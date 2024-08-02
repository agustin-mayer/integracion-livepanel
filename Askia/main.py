from app.crear_encabezados import crear_encabezados
from app.procesar_archivos import process_xml_files_in_folder

def main():
    xml_file_path = "./data/dataset2/SurveyStructure.xml"
    csv_file_path = "./data/dataset2/train_dataset2.csv"
    folder_path = "./data/dataset2/xml_responses"

    crear_encabezados(xml_file_path, csv_file_path)

    process_xml_files_in_folder(folder_path, csv_file_path)

if __name__ == "__main__":
    main()
