import xml.etree.ElementTree as ET
import csv

# Analizar el archivo XML
tree = ET.parse('./entradas/intvw383.xml')
root = tree.getroot()

# Abrir el archivo CSV para escritura
with open('output.csv', 'w', newline='') as csvfile:
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
