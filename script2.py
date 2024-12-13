import pymongo
import pandas as pd
import os
from datetime import datetime

# Cargar URI de MongoDB desde una variable de entorno
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DATABASE_NAME = "baseBicis"
COLLECTION_NAME = "bicis"

# Conexión a MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Definir los campos que necesitamos exportar
required_fields = ["_id", "name", "timestamp", "free_bikes", "empty_slots", "uid", "last_updated", "slots", "normal_bikes", "ebikes"]

# Función para obtener los datos de MongoDB y cargarlos en un DataFrame
def cargar_datos():
    try:
        # Obtener todos los documentos de la colección
        documentos = collection.find()

        # Convertir los documentos en una lista de diccionarios
        datos = []
        for doc in documentos:
            # Convertir _id a string
            doc["_id"] = str(doc["_id"]) if "_id" in doc else None
            # Filtrar y manejar campos faltantes
            filtered_data = {key: doc.get(key, None) for key in required_fields}
            # Convertir el campo timestamp a formato datetime si existe
            if filtered_data.get("timestamp"):
                try:
                    filtered_data["timestamp"] = pd.to_datetime(filtered_data["timestamp"])
                except ValueError:
                    filtered_data["timestamp"] = None
            datos.append(filtered_data)

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(datos)

        # Verificar si se cargaron los datos correctamente
        print(f"Datos cargados correctamente: {len(df)} registros.")
        print(df.head())

        return df

    except pymongo.errors.PyMongoError as e:
        print(f"Error al acceder a MongoDB: {e}")
        return None

# Función para exportar los datos a CSV y Parquet
def exportar_datos(df):
    if df is not None and not df.empty:
        try:
            # Exportar a CSV
            df.to_csv('datos_bicis.csv', index=False)
            print("Datos exportados a CSV correctamente.")

            # Exportar a Parquet
            df.to_parquet('datos_bicis.parquet', index=False)
            print("Datos exportados a Parquet correctamente.")

        except Exception as e:
            print(f"Error al exportar los datos: {e}")
    else:
        print("No hay datos para exportar.")

# Ejecutar el script para obtener y exportar los datos
if __name__ == "__main__":
    df_bicis = cargar_datos()
    exportar_datos(df_bicis)
