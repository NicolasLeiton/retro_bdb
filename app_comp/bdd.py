from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os, psycopg2

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def agregar_usuario(email, password, analist=False):
    try:
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO USERS(EMAIL, PASSWORD, ANALIST)
            VALUES (%s, %s, %s)
        ''',
        (email, generate_password_hash(password), analist))
        conn.commit()
        cursor.close()
        return {
        "success": True,
        "message": "Usuario creado"
    }
    except Exception as e:
        return {
        "success": False,
        "message": e
        }

def agregar_registro(email, fullname, phone, career, semester, cv):
    try:
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO INTERNS(EMAIL, FULLNAME, PHONE, DEGREE, SEMESTER, CV_ROUTE)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (email, fullname, phone, career, semester, cv))
        conn.commit()
        cursor.close()
        return {
        "success": True,
        "message": "Datos registrados exitosamente"
        }
    except Exception as e:
        return {
        "success": False,
        "message": e
        }

def verificar_usuario(email, password):
    try:
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE EMAIL= %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user== None:
            return {
                "success": False,
                "message": "El usuario no existe"
                }

        if not check_password_hash(user[1], password):
            return {
                "success": False,
                "message": "Contraseña incorrecta"
                }
        
        return {
        "success": True,
        "message": "Inicio de sesión existoso",
        "is_analist": user[2]
    }
    except Exception as e:
        return {
        "success": False,
        "message": e
        }
