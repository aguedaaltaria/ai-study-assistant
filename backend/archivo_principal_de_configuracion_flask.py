# Importamos las herramientas principales para levantar nuestro servidor web
from flask import Flask

# Importamos la herramienta para leer nuestro archivo oculto .env
from dotenv import load_dotenv
import os

# ¡Hola futuro yo! 
# Primero debemos cargar las variables de entorno ANTES de arrancar la aplicación.
# Esto garantiza que la clave secreta de la API y de Flask estén listas en memoria.
load_dotenv()

# Inicializamos nuestra aplicación web.
# Le indicamos a Flask que los archivos HTML (template_folder) y 
# los estáticos como CSS/JS (static_folder) están en la carpeta "frontend".
aplicacion_web_principal = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend',
    static_url_path='/'
)

# Asignamos la clave secreta a la aplicación para proteger las sesiones de los usuarios.
aplicacion_web_principal.secret_key = os.getenv('CLAVE_SECRETA_APLICACION_FLASK')

# Configuramos la ruta de nuestra base de datos local SQLite.
aplicacion_web_principal.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../base_de_datos_cuestionarios.db'

# Apagamos el rastreo de modificaciones de SQLAlchemy para ahorrar memoria RAM.
aplicacion_web_principal.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creamos una ruta de prueba rápida para verificar que el servidor escucha peticiones.
@aplicacion_web_principal.route('/prueba_de_conexion')
def funcion_para_probar_que_el_servidor_esta_encendido():
    # Este texto es el que leerás en el navegador cuando entres a la ruta.
    return "¡Hola futuro yo! El servidor web de Flask está funcionando perfectamente y listo para el Día 2."

# Condición para encender el servidor solo si ejecutamos este archivo directamente.
if __name__ == '__main__':
    # Encendemos el servidor en modo "debug" (depuración) para recargas automáticas al guardar cambios.
    aplicacion_web_principal.run(debug=True)