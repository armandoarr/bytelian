# Sistema Byteliano

## Como funciona
## Crear base de datos y tablas
Para crear una base de datos e integrar los datos de los archivos csv proporcionados en tablas utilice docker-compose. Para crear el contenedor para esta base de datos y las tablas correspondientes basta con ejecutar en la carpeta **db** el comando:

```bash
$ docker-compose up
```
o

```bash
$ docker-compose up -d
```
si se desea ejecutar en el fondo.

Ejecutar
```bash
$ python load_model()
```
para crear el esquema e insertar datos.
## Tablero de control

Para crear un tablero cree un **notebook de Jupyter**, dashboard.ipynb. Ahí se encuentran las métricas propuestas.
Para todo esto se utiliza pandas.
