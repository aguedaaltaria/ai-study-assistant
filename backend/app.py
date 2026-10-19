from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

aplicacion_web_principal = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend',
    static_url_path='/'
)

aplicacion_web_principal.secret_key = os.getenv('CLAVE_SECRETA_APLICACION_FLASK')

# Importamos y registramos el Blueprint con todas las rutas
from routes import bp_principal
aplicacion_web_principal.register_blueprint(bp_principal)

if __name__ == '__main__':
    aplicacion_web_principal.run(debug=True)