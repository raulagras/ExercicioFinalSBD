import pymongo
import pandas as pd
import os
from datetime import datetime
import requests

# Cargar URI de MongoDB desde una variable de entorno
MONGO_URI = os.getenv("MONGO_URI", "mongodb://meu-mongo:27017")
DATABASE_NAME = "baseClima"
COLLECTION_NAME = "clima"

# Conexión a MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configuración de la API
API_URL = "https://www.el-tiempo.net/api/json/v2/provincias/01"

# Definir los campos que necesitamos exportar (adaptados a la nueva estructura)
required_fields = ["_id", "name", "stateSky", "temperatures", "timestamp"]

# Función para obtener los datos de la API
def obtener_datos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
        datos = response.json()

        # Asegúrate de que los datos que recibes tengan la estructura esperada
        if "ciudades" in datos:
            ciudades = datos["ciudades"]
            
            # Crear una lista de documentos con el timestamp y los datos de cada ciudad
            documentos = []
            for ciudad in ciudades:
                documento = {
                    "timestamp": datetime.now(),  # Agregar timestamp
                    "provincia": ciudad["nameProvince"],
                    "ciudad": ciudad["name"],
                    "estado_cielo": ciudad["stateSky"]["description"],  # Descripción del estado del cielo
                    "temperatura_max": ciudad["temperatures"]["max"],   # Temperatura máxima
                    "temperatura_min": ciudad["temperatures"]["min"]    # Temperatura mínima
                }
                documentos.append(documento)

            # Insertar todos los documentos de las ciudades a la vez
            if documentos:
                resultado = collection.insert_many(documentos)
                print(f"Se insertaron {len(resultado.inserted_ids)} documentos.")
            else:
                print("No se encontraron ciudades para insertar.")
        else:
            print("Error: Estructura de datos inesperada en la respuesta de la API.")

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error al insertar datos en MongoDB: {e}")

# Función para cargar los datos desde MongoDB y convertirlos a un DataFrame
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
            df.to_csv('datos_clima.csv', index=False)
            print("Datos exportados a CSV correctamente.")

            # Exportar a Parquet
            df.to_parquet('datos_clima.parquet', index=False)
            print("Datos exportados a Parquet correctamente.")

        except Exception as e:
            print(f"Error al exportar los datos: {e}")
    else:
        print("No hay datos para exportar.")

# Ejecutar el script para obtener y exportar los datos
if __name__ == "__main__":
    # Primero obtener datos de la API
    obtener_datos()

    # Cargar los datos desde MongoDB y exportarlos
    df_clima = cargar_datos()
    exportar_datos(df_clima)
