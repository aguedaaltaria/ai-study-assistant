"""
NOTA HISTÓRICA Y TÉCNICA:
Se decidió no utilizar SQLAlchemy en este proyecto para mantener una arquitectura 
más minimalista, transparente y directa utilizando SQLite nativo (módulo 'sqlite3' de Python). 
Este archivo se conserva comentado únicamente con fines de documentación y referencia histórica.
"""

# # Importamos SQLAlchemy para gestionar la base de datos relacional
# from flask_sqlalchemy import SQLAlchemy
# 
# # Inicializamos la instancia de la base de datos
# base_de_datos = SQLAlchemy()
# 
# class ModeloDeUsuarioRegistrado(base_de_datos.Model):
#     """
#     Modelo que representa la tabla de usuarios en nuestra base de datos SQLite.
#     Almacena la credencial única, el correo y la contraseña cifrada.
#     """
#     __tablename__ = 'usuarios_registrados'
# 
#     # Identificador numérico autoincremental único para cada usuario
#     identificador_unico_del_usuario = base_de_datos.Column(base_de_datos.Integer, primary_key=True, autoincrement=True)
#     
#     # Correo electrónico único y obligatorio para el inicio de sesión
#     correo_electronico_del_usuario = base_de_datos.Column(base_de_datos.String(120), unique=True, nullable=False)
#     
#     # Contraseña procesada mediante hash seguro (nunca en texto plano)
#     contrasena_cifrada_del_usuario = base_de_datos.Column(base_de_datos.String(255), nullable=False)
# 
#     def __repr__(self):
#         # Representación legible del objeto en la terminal
#         return f'<Usuario Registrado con Correo: {self.correo_electronico_del_usuario}>'