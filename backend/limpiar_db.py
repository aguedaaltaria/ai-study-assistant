import sys
import os

# Añadimos la ruta raíz para que Python encuentre el módulo backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import obtener_conexion_db

# Abrimos conexión directa y borramos todos los registros de la tabla
conexion = obtener_conexion_db()
conexion.execute('DELETE FROM usuarios_registrados')
conexion.commit()
conexion.close()

print("¡Todos los usuarios de prueba han sido eliminados con éxito de la base de datos nativa!")