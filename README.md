# kc-api

Este repositorio contiene todos los archivos necesario para levantar el app engine de Viajes 3B en Google Cloud. 

- app.yaml: contiene los parámetros de configuración.
- requirements.txt: contiene las librerías y versiones específicas necesarias para hacer funcionar el main.py
- main.py: contiene el código de todas las queries y funciones que puede necesitar la página web para ofrecerle al usuario los contenidos deseados. 

En las carpetas se recoge el código necesario para ejecutar los sistemas tres sistemas de recomendación de apartamentos, restaurantes, actividades y puntos de interés, a saber por distancias, por popularidad (rate) y por tags o categorías (comida china, comida india, romántico, etc.). 

## enviroment variables
MYSQL_HOST=*bbdd_connection*

MYSQL_USER= *user*

MYSQL_PASSWORD=*password*

MYSQL_DATABASE=*bbdd_name*

BUCKET_NAME=*bucker_name*

GOOGLE_APPLICATION_CREDENTIALS=*path_to_credentials*

MAX_RESULTS=*number* by default its 5
