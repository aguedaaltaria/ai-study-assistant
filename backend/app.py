from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import sqlite3
from google import genai
import os

load_dotenv()

aplicacion_web_principal = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend',
    static_url_path='/'
)

aplicacion_web_principal.secret_key = os.getenv('CLAVE_SECRETA_APLICACION_FLASK')

# Definimos la ruta de nuestra base de datos SQLite nativa
RUTA_BASE_DE_DATOS = os.path.join(os.path.dirname(__file__), '../base_de_datos_cuestionarios.db')

# Inicializamos el cliente moderno de Gemini con la clave de tu .env
cliente_gemini = genai.Client(api_key=os.getenv('CLAVE_SECRETA_API_GOOGLE_GEMINI'))

def obtener_conexion_db():
    """Función auxiliar para abrir una conexión directa con SQLite"""
    conexion = sqlite3.connect(RUTA_BASE_DE_DATOS)
    conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conexion


def inicializar_base_de_datos():
    conexion = obtener_conexion_db()
    conexion.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_registrados (
            identificador_unico_del_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            correo_electronico_del_usuario TEXT UNIQUE NOT NULL,
            contrasena_cifrada_del_usuario TEXT NOT NULL
        )
    ''')
    
    conexion.execute('''
        CREATE TABLE IF NOT EXISTS cuestionarios_guardados (
            id_cuestionario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo_cuestionario TEXT NOT NULL,
            categoria TEXT DEFAULT 'General',
            contenido_pregunta TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios_registrados (identificador_unico_del_usuario)
        )
    ''')
    conexion.commit()
    conexion.close()


# Inicializamos la tabla al arrancar el servidor
inicializar_base_de_datos()


# Ruta histórica de prueba de conexión
@aplicacion_web_principal.route('/prueba_de_conexion')
def funcion_para_probar_que_el_servidor_esta_encendido():
    return "¡Hola futuro yo! El servidor web funciona con SQLite nativo."


# Ruta 1: Registro de nuevos usuarios (Procesa los datos del formulario por POST)
@aplicacion_web_principal.route('/registro', methods=['POST'])
def funcion_para_registrar_nuevo_usuario():
    correo = request.form.get('correo_electronico')
    contrasena = request.form.get('contrasena')

    conexion = obtener_conexion_db()
    
    # Verificamos si el usuario ya existe
    usuario_existente = conexion.execute(
        'SELECT * FROM usuarios_registrados WHERE correo_electronico_del_usuario = ?', 
        (correo,)
    ).fetchone()

    if usuario_existente:
        conexion.close()
        return "Error: Este correo electrónico ya está registrado.", 400

    contrasena_segura_en_hash = generate_password_hash(contrasena)

    # Insertamos el nuevo usuario nativamente
    conexion.execute(
        'INSERT INTO usuarios_registrados (correo_electronico_del_usuario, contrasena_cifrada_del_usuario) VALUES (?, ?)',
        (correo, contrasena_segura_en_hash)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('mostrar_pagina_de_login'))


# Ruta 2: Inicio de sesión / Login (Procesa credenciales por POST)
@aplicacion_web_principal.route('/login', methods=['POST'])
def funcion_para_iniciar_sesion():
    correo = request.form.get('correo_electronico')
    contrasena = request.form.get('contrasena')

    conexion = obtener_conexion_db()
    usuario = conexion.execute(
        'SELECT * FROM usuarios_registrados WHERE correo_electronico_del_usuario = ?', 
        (correo,)
    ).fetchone()
    conexion.close()

    if usuario and check_password_hash(usuario['contrasena_cifrada_del_usuario'], contrasena):
        session['usuario_id'] = usuario['identificador_unico_del_usuario']
        # Redirigimos al panel de control en lugar de mostrar texto
        return redirect(url_for('mostrar_panel_principal'))
        
    return "Error: Correo electrónico o contraseña incorrectos.", 401


# Ruta 3: Cierre de sesión / Logout
@aplicacion_web_principal.route('/logout')
def funcion_para_cerrar_sesion():
    session.pop('usuario_id', None)
    return "Has cerrado sesión exitosamente."


# Ruta 4: Muestra el formulario HTML de registro en el navegador (Método GET)
@aplicacion_web_principal.route('/registro', methods=['GET'])
def mostrar_pagina_de_registro():
    return render_template('pagina_de_registro_de_usuarios.html')


# Ruta 5: Muestra el formulario HTML de inicio de sesión en el navegador (Método GET)
@aplicacion_web_principal.route('/login', methods=['GET'])
def mostrar_pagina_de_login():
    return render_template('pagina_de_inicio_de_sesion.html')


# Ruta 6: Panel Principal / Dashboard (Protegida por sesión)
@aplicacion_web_principal.route('/panel')
def mostrar_panel_principal():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_pagina_de_login'))
    
    usuario_id = session['usuario_id']

    conexion = obtener_conexion_db()
    
    # Consultamos los cuestionarios de este usuario específico
    cuestionarios = conexion.execute(
        'SELECT * FROM cuestionarios_guardados WHERE usuario_id = ?',
        (usuario_id,)
    ).fetchall()
    
    conexion.close()

    # Renderizamos el panel pasando la lista de cuestionarios
    return render_template('panel_de_control_del_usuario.html', lista_de_cuestionarios=cuestionarios)


# Ruta 7: Muestra la plantilla base principal (Provisional)
@aplicacion_web_principal.route('/base')
def mostrar_plantilla_base():
    return render_template('plantilla_base_principal.html')


# Ruta 8: Muestra el cuestionario dinámico (Provisional)
@aplicacion_web_principal.route('/cuestionario')
def mostrar_cuestionario():
    return render_template('vista_de_cuestionario_dinamico.html')

# Ruta 9: Procesar y guardar un nuevo cuestionario (POST)
@aplicacion_web_principal.route('/crear-cuestionario', methods=['POST'])
def funcion_para_crear_cuestionario():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_pagina_de_login'))
        
    titulo = request.form.get('titulo_cuestionario')
    pregunta = request.form.get('contenido_pregunta')
    usuario_id = session['usuario_id']

    conexion = obtener_conexion_db()
    conexion.execute(
        'INSERT INTO cuestionarios_guardados (usuario_id, titulo_cuestionario, contenido_pregunta) VALUES (?, ?, ?)',
        (usuario_id, titulo, pregunta)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('mostrar_panel_principal'))


# Ruta 10: Devuelve los cuestionarios del usuario autenticado en formato JSON
@aplicacion_web_principal.route('/api/cuestionarios')
def api_obtener_cuestionarios():
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    cuestionarios = conexion.execute(
        'SELECT * FROM cuestionarios_guardados WHERE usuario_id = ?',
        (usuario_id,)
    ).fetchall()
    conexion.close()
    
    # Convertimos los registros de SQLite a una lista de diccionarios JSON
    return jsonify([dict(row) for row in cuestionarios])


@aplicacion_web_principal.route('/generar-cuestionario-ia', methods=['POST'])
def funcion_generar_cuestionario_ia():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_pagina_de_login'))
        
    tema = request.form.get('titulo_cuestionario')
    usuario_id = session['usuario_id']

    # Prompt estructurado exigiendo una categoría clara
    prompt = (
        f"Genera una pregunta de estudio técnica sobre el tema: '{tema}'. "
        "Devuelve la respuesta estrictamente en el siguiente formato:\n"
        "CATEGORIA: [Elige una categoría corta y general como Historia, Matemáticas, Computación y Tecnología, Literatura, Deportes, Ciencias, o crea una nueva si ninguna encaja]\n"
        "PREGUNTA Y EXPLICACION: [Tu contenido detallado aquí]"
    )

    contenido_generado = ""
    categoria_asignada = "General"
    modelos_disponibles = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']

    for modelo in modelos_disponibles:
        try:
            respuesta_ia = cliente_gemini.models.generate_content(
                model=modelo,
                contents=prompt,
            )
            texto_respuesta = respuesta_ia.text
            
            # Extraemos de forma inteligente la categoría y el contenido usando Python
            if "CATEGORIA:" in texto_respuesta and "PREGUNTA Y EXPLICACION:" in texto_respuesta:
                partes = texto_respuesta.split("PREGUNTA Y EXPLICACION:")
                cat_parte = partes[0].replace("CATEGORIA:", "").strip()
                if len(cat_parte) < 30: # Evitamos textos muy largos por error de la IA
                    categoria_asignada = cat_parte
                contenido_generado = partes[1].strip()
            else:
                contenido_generado = texto_respuesta.strip()
                
            break
        except Exception as e:
            if modelo == modelos_disponibles[-1]:
                contenido_generado = f"Error al generar contenido con IA: {str(e)}"
            continue

    # Guardamos el título, la categoría asignada por la IA y el contenido en SQLite
    conexion = obtener_conexion_db()
    conexion.execute(
        'INSERT INTO cuestionarios_guardados (usuario_id, titulo_cuestionario, categoria, contenido_pregunta) VALUES (?, ?, ?, ?)',
        (usuario_id, tema, categoria_asignada, contenido_generado)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('mostrar_panel_principal'))


# Ruta para eliminar un cuestionario específico por su ID
@aplicacion_web_principal.route('/eliminar-cuestionario/<int:id_cuestionario>', methods=['POST'])
def funcion_eliminar_cuestionario(id_cuestionario):
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    
    # Aseguramos que el cuestionario pertenezca al usuario autenticado antes de borrarlo
    conexion.execute(
        'DELETE FROM cuestionarios_guardados WHERE id_cuestionario = ? AND usuario_id = ?',
        (id_cuestionario, usuario_id)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('mostrar_panel_principal'))


if __name__ == '__main__':
    aplicacion_web_principal.run(debug=True)