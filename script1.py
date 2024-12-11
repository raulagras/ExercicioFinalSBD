import pymongo
import requests
import schedule
import time
from datetime import datetime, timezone

# Configuración de MongoDB Atlas
MONGO_URI = "mongodb+srv://raulagras04:changeme@cluster0.u3swg.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "baseBicis"
COLLECTION_NAME = "bicis"

# Conexión a MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configuración de la API
API_URL = "http://api.citybik.es/v2/networks/bicicorunha"

# Función para obtener datos de la API
def obtener_datos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
        datos = response.json()

	 # Agregar timestamp a los datos (usando datetime.now con zona horaria UTC)
        datos["timestamp"] = datetime.now(timezone.utc)

        # Insertar los datos en MongoDB
        resultado = collection.insert_one(datos)

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error al insertar datos en MongoDB: {e}")

# Programar la ejecución a intervalos regulares (cada X minutos)
INTERVALO_MINUTOS = 1
schedule.every(INTERVALO_MINUTOS).minutes.do(obtener_datos)

# Llamar inmediatamente a la función para obtener e insertar los datos al iniciar
obtener_datos()

# Ejecutar el script de manera indefinida hasta que el usuario quiera parar
print(f"Iniciando script para consultar la API cada {INTERVALO_MINUTOS} minutos.")
while True:
    schedule.run_pending()
    time.sleep(1)
