import xml.etree.ElementTree as ET
import chardet

# Ruta al archivo XML
file_path = './SurveyStructure.xml'  # Reemplazar con la ruta correcta si es necesario

# Detectar la codificación del archivo
with open(file_path, 'rb') as raw_file:
    raw_data = raw_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Función para explorar el árbol XML y mostrar las etiquetas y atributos
def explore_xml(element, indent=0):
    print(" " * indent + f"Tag: {element.tag}, Attributes: {element.attrib}")
    for child in element:
        explore_xml(child, indent + 2)

# Decodificar los datos crudos y parsear el contenido XML
decoded_data = raw_data.decode(encoding)
tree = ET.ElementTree(ET.fromstring(decoded_data))
root = tree.getroot()
# Explorar el árbol XML a partir de la raíz
explore_xml(root)
