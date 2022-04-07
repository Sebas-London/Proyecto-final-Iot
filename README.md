# Proyecto-final-Iot

## Configuracion Raspberry
Para ejecutar el proyecto de manera correcta se deben abrir 2 consolas, en una de ella se iniciara el server para ejecutar la camara, se hace con el siguiente comando : "libcamera-vid -t 0 --inline --listen -o tcp://127.0.0.1:8888", despues de hacer esto se procede a trabajar sobre una consola nueva sin cerrar esta.
En la nueva consola se abre el codigo llamado "led.py" por consola, para ello se debe iniciar el entorno de kivy con el comando "source kivy_venv/bin/activate", luego se accede al sitio donde esta el proyecto "led.py", en mi caso esta en "cd Downloads" y luego de estar dentro con el siguiente comando "python3 led.py" se ejecuta la aplicacion.

## Configuracion NodeMCU Y sensores

Al mismo tiempo se debe abrir el proyecto llamado "MQTT.ino" en un editor de arduino e instalar la libreria llamada "pubsub", luego se conecta el NodeMCU al computador, y se conectan los sensores que se quieren utilizar en los puertos definidos dentro del codigo.
