import pymongo
import requests
import schedule
import time
from datetime import datetime, timezone

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://raulagras04:changeme@cluster0.u3swg.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "baseBicis"
COLLECTION_NAME = "bicis"

# Conexión a MongoDB
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

        # Asegúrate de que los datos que recibes tengan la estructura esperada
        if "network" in datos and "stations" in datos["network"]:
            estaciones = datos["network"]["stations"]

            # Crear una lista de documentos con el timestamp y los datos de cada bicicleta
            documentos = []
            for estacion in estaciones:
                documento = estacion.copy()  # Copiar el diccionario de cada estación
                documento["timestamp"] = datetime.now(timezone.utc)  # Agregar timestamp a cada documento
                documentos.append(documento)

            # Insertar todos los documentos de las bicicletas a la vez
            if documentos:
                resultado = collection.insert_many(documentos)
                print(f"Se insertaron {len(resultado.inserted_ids)} documentos.")
            else:
                print("No se encontraron estaciones para insertar.")
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
