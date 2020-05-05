# Flask Cisco Collaboration

Es un proyecto para crear una REST API con Flask para el Cisco Unified Communications Maanger.

La documentación del proyecto se puede encontrar en: https://flaskciscocollab.readthedocs.io/.

La documentación de la API la puedes encontrar en: https://flaskciscocollab.docs.apiary.io/.

Para crear la documentación tenemos que ejecutar el comando
sphinx-build -b html .\source .\templates

Para ejecutar la aplicación con gunicorn, tenemos que ejecutar el siguiente comando:
```
gunicorn --workers 1 --threads 1 --timeout 60  --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:8443 app:app
```
