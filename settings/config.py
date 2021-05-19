import os



## App settings
name = "Prueba Aeelen"

host = "0.0.0.0"

port = int(os.environ.get("PORT", 5000))

debug = False

contacts = "http://www5.diputados.gob.mx/index.php/camara/Centros-de-Estudio/CESOP"

code = "https://github.com/Aeelen-Miranda/DashPython/"

#fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'



## File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"



## DB
