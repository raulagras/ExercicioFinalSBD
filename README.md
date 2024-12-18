# Proyecto de Integración con API y MongoDB!

Este proyecto consta de dos scripts en Python que interactúan con una API, almacenan datos en una base de datos MongoDB y exportan estos datos a diferentes formatos. El objetivo es recoger información sobre el estado de las bicicletas en diferentes ubicaciones a través de una API, almacenarlos en MongoDB y luego procesar y exportar esos datos usando **pandas** en formatos como **CSV** y **Parquet**.


## Parte Básica 

 - Script 1:
 
	 - Se conecta a la API a intervalos regulares (cada 5 minutos).
	 
	  - El script corre de manera continua hasta que se detenga manualmente.
	  
	  - Obtiene los datos de la API y los almacena en una base de datos MongoDB en la colección "bicis".
	  
	 ***Funcionalidad***

	1.  **Conexión con MongoDB**: Se conecta a la base de datos MongoDB en Atlas utilizando las credenciales y URI configuradas.
	
	2.  **Obtención de datos**: Hace una solicitud a la API de CityBike y obtiene la respuesta en formato JSON.
	
	3.  **Almacenamiento en MongoDB**: Los datos obtenidos se almacenan en una colección llamada `bicis` dentro de la base de datos `baseBicis`.

	4.  **Intervalo de ejecución**: El script se ejecuta cada 5 minutos (o el intervalo que se defina) utilizando la librería `schedule`.
 - Script 2:
 
	 - Lee los datos almacenados en MongoDB y los carga en un DataFrame de pandas.

	 - El script se ejecuta a demanda, descargando y exportando todos los documentos de la base de datos.
	 
	 - Exporta los siguientes campos: `id`, `name`, `timestamp`, `free_bikes`, `empty_slots`, `uid`, `last_updated`, `slots`, `normal_bikes`, `ebikes`.
	 
	- Exporta los datos a los formatos:
			

		 - **CSV**
		 - **Parquet**
		 
	  ***Funcionalidad***

		1.  **Conexión con MongoDB**: Se conecta a la base de datos MongoDB en Atlas utilizando las credenciales y URI configuradas.
	
		2.  **Obtención de datos**: Hace una solicitud a la API de CityBike y obtiene la respuesta en formato JSON.
	
		3.  **Almacenamiento en MongoDB**: Los datos obtenidos se almacenan en una colección llamada `bicis` dentro de la base de datos `baseBicis`.

		4.  **Intervalo de ejecución**: El script se ejecuta cada 5 minutos (o el intervalo que se defina) utilizando la librería `schedule`.

### Requisitos

#### Requisitos del Sistema

 - **Python**
 
 - **MongoDB Atlas** para la base de datos (puedes usar un cluster gratuito).
 
 - **API de CityBike**: Proporciona información sobre redes de bicicletas compartidas.

#### Librerías necesarias

Este proyecto requiere las siguientes librerías de Python:

    pip install pymongo pandas requests schedule pyarrow

 - **pymongo**: Para interactuar con la base de datos MongoDB.
 - **pandas**: Para el manejo y exportación de datos a **CSV** y **Parquet**.
 - **requests**: Para realizar las solicitudes HTTP a la API.
 - **schedule**: Para ejecutar el script a intervalos regulares.
 - **pyarrow**: Necesario para exportar datos a **Parquet**.

### Configuración

#### Configuración de MongoDB

Para usar MongoDB Atlas, primero debes crear una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) y configurar un cluster. Luego, obtendrás la URI de conexión que se utilizará en el script.

La URI de conexión será algo similar a:

    MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
Reemplaza `<username>` y `<password>` con tus credenciales de MongoDB Atlas.

#### Configuración de la API

En este proyecto, se usa la API de CityBike, específicamente la red de bicicletas de **A Coruña**:

    API_URL = "https://api.citybik.es/v2/networks/bicicorunha"
Este URL proporciona datos sobre las bicicletas disponibles, los espacios vacíos, y otros detalles sobre la red de bicicletas.


## Conclusión

Este proyecto proporciona una solución sencilla para interactuar con APIs externas, almacenar datos en MongoDB, y procesar esos datos usando **pandas**. Al final, los datos se pueden exportar en múltiples formatos, lo que permite su uso en otros sistemas o herramientas de análisis.

## Parte Avanzada

Este proyecto consiste en dockerizar un script de Python que interactúa con una base de datos MongoDB, desplegarlo en la nube utilizando OpenStack y automatizar su actualización mediante GitHub. A continuación, se detallan los pasos para configurar y ejecutar el proyecto.


## Requisitos


1. **Dockerizar el script para que se ejecute en un contenedor Docker.** 

2. **Utilizar un servidor MongoDB propio en un contenedor Docker.** 

3. **Publicar la imagen Docker en Docker Hub.**

4. **Desplegar la aplicación en la nube (OpenStack) con Docker.**

 5. **Automatizar la actualización del contenedor Docker desde GitHub.**

## Instrucciones

### 1. Dockerizar el Script de Python
Crea un archivo `Dockerfile` en el directorio del proyecto para construir la imagen Docker del script.

### 2. Configurar MongoDB en un Contenedor Docker

Utiliza un archivo `docker-compose.yml` para configurar la base de datos MongoDB junto con la aplicación Python.

Ejecuta el siguiente comando para levantar ambos servicios:

    docker-compose up --build


### 3. Publicar la Imagen Docker en Docker Hub

 1. Inicia sesión en Docker Hub:

    docker login
  

 2. Construye la imagen Docker:
 

    docker build -t <dockerhub_username>/python-app .
    

 3. Sube la imagen al Docker Hub:
 
	 docker push <dockerhub_username>/python-app


### 4. Desplegar en la Nube con OpenStack
 1. Configura Openstack
 
     -   Crea una instancia de máquina virtual.
     
	     -   La instancia debe llevar tu nombre: por ejemplo, sbd-tu_nombre
    
			-   Escoge una imagen de instalación ubuntu22.04
    
			-   Utiliza un conjunto de reglas de firewall ajustado: por ejemplo, open4all
    
			-   Añade tu llave RSA, así como la llave RSA del profesor (para que tambien el tenga acceso)
    
			-   Instala docker en tu máquina virtual siguiendo las instrucciones que tienes mas abajo
    
			-   Asegúrate de que tienes acceso a la máquina virtual en la nube
     
	-   Acceso a la máquina virtual en la nube.
	
		   Para acceder ás máquinas virtuais (por ssh) tes dúas opcións:

		1. Activar a VPN ao CESGA

		2. Realizar un salto sobre unha máquina intermedia.

  

			Desde tu pc local en la clase tienes acceso a la máquina hadoop.cesga.es y en esa máquina tienes acceso a las máquinas virtuales, por lo que puedes hacer un SSH Jump.

			En lugar de conectarte á máquina destino directamente con:

			`ssh cesgaxuser@ip_máquina_virtual`

			utiliza un ssh jump

			`ssh -J usuario_hadoop@hadoop.cesga.es cesgaxuser@ip_máquina_virtual
`

 - Desplegar contenedores en OpenStack:
 
	
	 - Copia el archivo `docker-compose.yml` al servidor. 
	 
	 - 	 Ejecuta los siguientes comandos para iniciar los servicios:
		
				docker-compose up --build -d

 3.  Cálculo del número de documentos

	 - Suponiendo que la API consulta datos cada 5 minutos durante las vacaciones:
					 
			Días de vacaciones: N
			Total de documentos = (24 horas * 12 consultas/hora) * N días * 49 documentos por consulta.

### 5. Automatizar Actualizaciones desde GitHub

Es posible configurar una automatización en GitHub para que la imagen se construya con cada nuevo push al repositorio y automáticamente se envíe al registro (hub.docker.com).

 - **Pasos necesarios:**
 
	1.  Crear un token de acceso para GitHub en Docker Hub.
	
	2.  Configurar las credenciales de acceso GitHub >> Docker Hub.
	
	3.  Definir un Workflow que construya la imagen y la envíe al registro.

- **Crear token de acceso en Docker Hub**

	Docker Hub:  
Ir a **My Account > Security > New Access Token**.

- **Configurar credenciales en GitHub**

	Repositorio de GitHub:  
Ir a **Settings > Secrets and Variables > Actions > Repository Secrets** y añadir:

	-   `DOCKER_USERNAME`: nombre_de_usuario_hub
	-   `DOCKERHUB_TOKEN`: token_hub
- **Configurar Workflow en GitHub**

En el repositorio, ir a **Actions > Set up a workflow 		yourself** y definir el siguiente archivo YAML:

    name: ci
    on: 
	    push: 
		    branches: 
			    - main
	jobs: 
		build: 
			runs-on: ubuntu-latest
			steps: 
				- 
					name: Checkout
					uses: actions/checkout@v4
				- 
					name: Login to Docker Hub
					uses: docker/login-action@v3
					with:
						username: ${{ secrets.DOCKER_USERNAME }} 
						password: ${{ secrets.DOCKERHUB_TOKEN }}
				- 
					name: Set up Docker Buildx
					uses: docker/setup-buildx-action@v3
				- 
					name: Build and push
					uses: docker/build-push-action@v5
					with: 
     						context: . 
						push: true 
						tags: ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
### Funcionamiento

-   El Workflow se ejecutará automáticamente y una nueva imagen creada con el código actual del repositorio será enviada al registro de Docker Hub.
-   Ante cada nuevo push al repositorio, el Workflow volverá a ejecutarse, actualizando la imagen en Docker Hub con la última versión del código.
