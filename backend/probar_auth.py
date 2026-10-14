import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import aplicacion_web_principal

with aplicacion_web_principal.test_client() as cliente:
    print("=== 1. PROBANDO REGISTRO DE USUARIO (NATIVO) ===")
    r1 = cliente.post('/registro', data={
        'correo_electronico': 'agueda_vanilla@prueba.com',
        'contrasena': 'password_123'
    })
    print("Código HTTP:", r1.status_code)
    print("Respuesta:", r1.get_data(as_text=True))

    print("\n=== 2. PROBANDO LOGIN CORRECTO ===")
    r2 = cliente.post('/login', data={
        'correo_electronico': 'agueda_vanilla@prueba.com',
        'contrasena': 'password_123'
    })
    print("Código HTTP:", r2.status_code)
    print("Respuesta:", r2.get_data(as_text=True))

    print("\n=== 3. PROBANDO LOGOUT ===")
    r3 = cliente.get('/logout')
    print("Código HTTP:", r3.status_code)
    print("Respuesta:", r3.get_data(as_text=True))