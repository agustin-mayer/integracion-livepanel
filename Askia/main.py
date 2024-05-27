import xml.etree.ElementTree as ET
import csv

interviewer_id = 383

# Leer y modificar el contenido del archivo XML
with open(f'./entradas/xml/intvw{interviewer_id}.xml', 'rb') as file:
    xml_content = file.read()

# Reemplazar la declaración de codificación
xml_content = xml_content.replace(b'encoding="Unicode"', b'encoding="UTF-8"')

# Decodificar el contenido usando la codificación correcta
xml_content = xml_content.decode('utf-16')  # Assuming the original encoding was UTF-16

# Analizar el contenido XML modificado
root = ET.fromstring(xml_content)

# Abrir el archivo CSV para escritura
with open(f'./entradas/csv/intvw{interviewer_id}.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Escribir el encabezado
    header = ['User', 'QuestionId', 'Value']
    csvwriter.writerow(header)
    
    # Obtener el User ID
    user_id = root.find('Header/User').text
    
    # Extraer datos de respuestas
    for answer in root.findall('Answer'):
        question_id = answer.attrib['QuestionId']
        value = answer.find('Value').text
        
        row = [user_id, question_id, value]
        csvwriter.writerow(row)
    
    # Extraer datos de respuestas dentro de bucles
    for loop in root.findall('Loop'):
        for item in loop.findall('Item'):
            for answer in item.findall('Answer'):
                question_id = answer.attrib['QuestionId']
                value = answer.find('Value').text
                
                row = [user_id, question_id, value]
                csvwriter.writerow(row)

print("El archivo CSV ha sido creado exitosamente.")
