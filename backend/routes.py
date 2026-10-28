from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import json
from google import genai

# Creamos un Blueprint para agrupar todas las rutas de la aplicación
bp_principal = Blueprint('rutas_principales', __name__)

# Definimos la ruta de nuestra base de datos SQLite nativa
RUTA_BASE_DE_DATOS = os.path.join(os.path.dirname(__file__), '../base_de_datos_cuestionarios.db')

# Inicializamos el cliente moderno de Gemini con la clave del .env
cliente_gemini = genai.Client(api_key=os.getenv('CLAVE_SECRETA_API_GOOGLE_GEMINI'))

def obtener_conexion_db():
    """Función auxiliar para abrir una conexión directa con SQLite"""
    conexion = sqlite3.connect(RUTA_BASE_DE_DATOS)
    conexion.row_factory = sqlite3.Row
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

# Inicializamos la tabla al importar el módulo
inicializar_base_de_datos()


@bp_principal.route('/prueba_de_conexion')
def funcion_para_probar_que_el_servidor_esta_encendido():
    return "¡Hola futuro yo! El servidor web funciona con SQLite nativo."


@bp_principal.route('/registro', methods=['POST'])
def funcion_para_registrar_nuevo_usuario():
    correo = request.form.get('correo_electronico')
    contrasena = request.form.get('contrasena')

    conexion = obtener_conexion_db()
    usuario_existente = conexion.execute(
        'SELECT * FROM usuarios_registrados WHERE correo_electronico_del_usuario = ?', 
        (correo,)
    ).fetchone()

    if usuario_existente:
        conexion.close()
        return "Error: Este correo electrónico ya está registrado.", 400

    contrasena_segura_en_hash = generate_password_hash(contrasena)

    conexion.execute(
        'INSERT INTO usuarios_registrados (correo_electronico_del_usuario, contrasena_cifrada_del_usuario) VALUES (?, ?)',
        (correo, contrasena_segura_en_hash)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))


@bp_principal.route('/login', methods=['POST'])
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
        return redirect(url_for('rutas_principales.mostrar_panel_principal'))
        
    return "Error: Correo electrónico o contraseña incorrectos.", 401


@bp_principal.route('/logout')
def funcion_para_cerrar_sesion():
    session.pop('usuario_id', None)
    return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))


@bp_principal.route('/registro', methods=['GET'])
def mostrar_pagina_de_registro():
    return render_template('pagina_de_registro_de_usuarios.html')


@bp_principal.route('/login', methods=['GET'])
def mostrar_pagina_de_login():
    return render_template('pagina_de_inicio_de_sesion.html')


@bp_principal.route('/panel')
def mostrar_panel_principal():
    if 'usuario_id' not in session:
        return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))
    
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    cuestionarios = conexion.execute(
        'SELECT * FROM cuestionarios_guardados WHERE usuario_id = ?',
        (usuario_id,)
    ).fetchall()
    conexion.close()

    return render_template('panel_de_control_del_usuario.html', lista_de_cuestionarios=cuestionarios)


@bp_principal.route('/crear-cuestionario', methods=['POST'])
def funcion_para_crear_cuestionario():
    if 'usuario_id' not in session:
        return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))
        
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

    return redirect(url_for('rutas_principales.mostrar_panel_principal'))


@bp_principal.route('/api/cuestionarios')
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
    
    return jsonify([dict(row) for row in cuestionarios])


@bp_principal.route('/generar-cuestionario-ia', methods=['POST'])
def funcion_generar_cuestionario_ia():
    if 'usuario_id' not in session:
        return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))
        
    tema = request.form.get('titulo_cuestionario')
    usuario_id = session['usuario_id']

    prompt = (
        f"Genera una tarjeta de estudio técnica y precisa sobre un concepto clave del tema: '{tema}'.\n"
        "REGLA ESTRICTA DE ESCRITURA: Escribe todo el texto, fórmulas y ecuaciones utilizando exclusivamente notación matemática estándar de texto plano (por ejemplo: F_neta = m * a). ESTÁ PROHIBIDO usar comandos LaTeX.\n\n"
        "DEBES RESPONDER ESTRICTAMENTE SIGUIENDO ESTE FORMATO EXACTO:\n"
        "CATEGORIA: [Elige una categoría corta como Ciencias, Historia, Matemáticas, Computación y Tecnología, Literatura, Deportes]\n"
        "PREGUNTA Y EXPLICACION: [Redacta UNA sola pregunta directa y clave sobre el tema, seguida inmediatamente de su explicación técnica detallada y respuesta correcta]"
    )

    contenido_generado = ""
    categoria_asignada = "General"
    
    # Modelo oficial requerido por la API actual de Google GenAI
    modelos_disponibles = ['gemini-3.8-flash']

    for modelo in modelos_disponibles:
        try:
            respuesta_ia = cliente_gemini.models.generate_content(
                model=modelo,
                contents=prompt,
            )
            texto_respuesta = respuesta_ia.text
            
            if "CATEGORIA:" in texto_respuesta and "PREGUNTA Y EXPLICACION:" in texto_respuesta:
                partes = texto_respuesta.split("PREGUNTA Y EXPLICACION:")
                cat_parte = partes[0].replace("CATEGORIA:", "").strip()
                if len(cat_parte) < 30 and len(cat_parte) > 0:
                    categoria_asignada = cat_parte
                contenido_generado = partes[1].strip()
            else:
                contenido_generado = texto_respuesta.strip()
                
            break
        except Exception as e:
            contenido_generado = f"Error al generar contenido con IA: {str(e)}"

    conexion = obtener_conexion_db()
    conexion.execute(
        'INSERT INTO cuestionarios_guardados (usuario_id, titulo_cuestionario, categoria, contenido_pregunta) VALUES (?, ?, ?, ?)',
        (usuario_id, tema, categoria_asignada, contenido_generado)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('rutas_principales.mostrar_panel_principal'))


@bp_principal.route('/eliminar-cuestionario/<int:id_cuestionario>', methods=['POST'])
def funcion_eliminar_cuestionario(id_cuestionario):
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    conexion.execute(
        'DELETE FROM cuestionarios_guardados WHERE id_cuestionario = ? AND usuario_id = ?',
        (id_cuestionario, usuario_id)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('rutas_principales.mostrar_panel_principal'))


@bp_principal.route('/api/exportar-json', methods=['GET'])
def exportar_cuestionarios_json():
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    cursor.execute(
        'SELECT titulo_cuestionario, categoria, contenido_pregunta FROM cuestionarios_guardados WHERE usuario_id = ?',
        (usuario_id,)
    )
    filas = cursor.fetchall()
    conexion.close()

    lista_cuestionarios = [{"titulo_cuestionario": f[0], "categoria": f[1], "contenido_pregunta": f[2]} for f in filas]
    datos_json = json.dumps(lista_cuestionarios, ensure_ascii=False, indent=4)

    return Response(
        datos_json,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=respaldo_cuestionarios_studyai.json"}
    )


@bp_principal.route('/api/importar-json', methods=['POST'])
def importar_cuestionarios_json():
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401

    if 'archivo_json' not in request.files:
        return jsonify({"error": "No se proporcionó ningún archivo"}), 400

    archivo = request.files['archivo_json']
    try:
        contenido = archivo.read().decode('utf-8')
        cuestionarios = json.loads(contenido)
        
        usuario_id = session['usuario_id']
        conexion = obtener_conexion_db()
        
        for item in cuestionarios:
            conexion.execute(
                'INSERT INTO cuestionarios_guardados (usuario_id, titulo_cuestionario, categoria, contenido_pregunta) VALUES (?, ?, ?, ?)',
                (usuario_id, item.get('titulo_cuestionario', 'Sin título'), item.get('categoria', 'General'), item.get('contenido_pregunta', ''))
            )
        conexion.commit()
        conexion.close()
        
        return redirect(url_for('rutas_principales.mostrar_panel_principal'))
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo JSON: {str(e)}"}), 400


@bp_principal.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas_estudio():
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM cuestionarios_guardados WHERE usuario_id = ?', (usuario_id,))
    total_preguntas = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT categoria) FROM cuestionarios_guardados WHERE usuario_id = ?', (usuario_id,))
    total_categorias = cursor.fetchone()[0]
    
    cursor.execute('SELECT categoria, COUNT(*) FROM cuestionarios_guardados WHERE usuario_id = ? GROUP BY categoria', (usuario_id,))
    desglose = cursor.fetchall()
    conexion.close()
    
    return jsonify({
        "total_preguntas": total_preguntas,
        "total_categorias": total_categorias,
        "desglose": [{"categoria": fila[0], "cantidad": fila[1]} for fila in desglose]
    })


@bp_principal.route('/repaso', methods=['GET'])
def vista_repaso():
    if 'usuario_id' not in session:
        return redirect(url_for('rutas_principales.mostrar_pagina_de_login'))
    return render_template('repaso.html')

@bp_principal.route('/api/repaso/preguntas', methods=['GET'])
def api_obtener_preguntas_repaso():
    if 'usuario_id' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    usuario_id = session['usuario_id']
    conexion = obtener_conexion_db()
    
    # Seleccionamos las preguntas del usuario de forma aleatoria (RANDOM)
    preguntas = conexion.execute(
        'SELECT * FROM cuestionarios_guardados WHERE usuario_id = ? ORDER BY RANDOM()',
        (usuario_id,)
    ).fetchall()
    conexion.close()
    
    return jsonify([dict(fila) for row in preguntas for fila in [row]]) # o [dict(row) for row in preguntas]