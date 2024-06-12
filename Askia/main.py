from app.crear_encabezados import crear_encabezados
from app.procesar_archivos import process_xml_files_in_folder

def main():
    # Rutas de los archivos
    xml_file_path = "./data/SurveyStructure.xml"
    csv_file_path = "./data/train_dataset3.csv"
    folder_path = "./data/xml_responses"

    # Crear encabezados
    crear_encabezados(xml_file_path, csv_file_path)

    # Procesar archivos XML y completar el CSV
    process_xml_files_in_folder(folder_path, csv_file_path)

if __name__ == "__main__":
    main()
