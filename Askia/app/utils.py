import chardet

def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']
    except Exception as e:
        print(f"Error al detectar la codificación del archivo {file_path}: {e}")
        return 'utf-8'  # Si no se puede detectar la codificación, se devuelve 'utf-8' como predeterminado
