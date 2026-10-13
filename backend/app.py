# Importamos Flask y las herramientas necesarias
from flask import Flask
from backend.modelos import base_de_datos, ModeloDeUsuarioRegistrado
from dotenv import load_dotenv
import os

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# Inicializamos la aplicación indicando las rutas personalizadas de carpetas
aplicacion_web_principal = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend',
    static_url_path='/'
)

# Configuramos la clave secreta de la aplicación
aplicacion_web_principal.secret_key = os.getenv('CLAVE_SECRETA_APLICACION_FLASK')

# Configuramos la conexión a SQLite en la raíz del proyecto
aplicacion_web_principal.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../base_de_datos_cuestionarios.db'
aplicacion_web_principal.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vinculamos SQLAlchemy con nuestra aplicación Flask
base_de_datos.init_app(aplicacion_web_principal)

# Ruta temporal de prueba
@aplicacion_web_principal.route('/prueba_de_conexion')
def funcion_para_probar_que_el_servidor_esta_encendido():
    return "¡Hola futuro yo! El servidor funciona y el modelo de usuarios está integrado."

if __name__ == '__main__':
    aplicacion_web_principal.run(debug=True)