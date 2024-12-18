import pymongo
import requests
import schedule
import time
from datetime import datetime, timezone

# Configuración de MongoDB
MONGO_URI = "mongodb://meu-mongo:27017"
DATABASE_NAME = "baseTiempo"
COLLECTION_NAME = "clima"

# Conexión a MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configuración de la API
API_URL = "https://www.el-tiempo.net/api/json/v2/provincias/01"

# Función para obtener datos de la API
def obtener_datos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
        datos = response.json()

        # Asegúrate de que los datos que recibes tengan la estructura esperada
        if "origen" in datos and "ciudades" in datos:
            # Obtener la información de las ciudades y el clima actual
            ciudades = datos["ciudades"]
            
            # Crear una lista de documentos con el timestamp y los datos de cada ciudad
            documentos = []
            for ciudad in ciudades:
                documento = {
                    "timestamp": datetime.now(timezone.utc),  # Agregar timestamp
                    "provincia": ciudad["nameProvince"],
                    "ciudad": ciudad["name"],
                    "estado_cielo": ciudad["stateSky"]["description"],
                    "temperatura_max": ciudad["temperatures"]["max"],
                    "temperatura_min": ciudad["temperatures"]["min"],
                    "descripcion_origen": datos["origen"]["descripcion"]
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

# Programar la ejecución a intervalos regulares (cada X minutos)
INTERVALO_MINUTOS = 5
schedule.every(INTERVALO_MINUTOS).minutes.do(obtener_datos)

# Llamar inmediatamente a la función para obtener e insertar los datos al iniciar
obtener_datos()

# Ejecutar el script de manera indefinida hasta que el usuario quiera parar
print(f"Iniciando script para consultar la API cada {INTERVALO_MINUTOS} minutos.")
while True:
    schedule.run_pending()
    time.sleep(1)
