import sys
import os

# Añadimos la ruta actual al sistema para que Python encuentre la carpeta backend sin problemas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import aplicacion_web_principal
from backend.modelos import base_de_datos, ModeloDeUsuarioRegistrado

# Abrimos el contexto de la aplicación para que SQLAlchemy reconozca la base de datos
with aplicacion_web_principal.app_context():
    # ¡Paso clave! Creamos físicamente las tablas antes de insertar nada
    base_de_datos.create_all()
    
    # Creamos un usuario de prueba
    usuario_de_prueba = ModeloDeUsuarioRegistrado(
        correo_electronico_del_usuario="agueda@prueba.com",
        contrasena_cifrada_del_usuario="hash_falso_de_prueba_123"
    )
    
    # Agregamos y guardamos en la base de datos
    base_de_datos.session.add(usuario_de_prueba)
    base_de_datos.session.commit()
    
    # Consultamos los usuarios guardados
    usuarios_guardados = ModeloDeUsuarioRegistrado.query.all()
    print("¡Éxito! Usuarios encontrados en la base de datos:", usuarios_guardados)