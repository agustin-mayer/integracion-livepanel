import pandas as pd

input_path = r'.\data\Encuesta de música_19 de junio de 2024_13.49_numerico.csv'
output_path = r'.\data\train_dataset.csv'

df = pd.read_csv(input_path)

# Eliminar la segunda y tercer fila (índices 0 y 1)
df = df.drop([0, 1]).reset_index(drop=True)

# Filtrar las columnas necesarias (ResponseId y las preguntas)
columns_to_keep = ['ResponseId'] + [col for col in df.columns if col.startswith('Q')]
filtered_df = df[columns_to_keep]

filtered_df.to_csv(output_path, index=False)

print("El archivo ha sido procesado y guardado en:", output_path)
