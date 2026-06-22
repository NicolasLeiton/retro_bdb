from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os, psycopg2
from flask import jsonify
load_dotenv()

#Realizar conexion
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
# ---CREATE---
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

def agregar_registro(email, fullname, phone, career, semester, cv=None):
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

# -- READ --
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

def lista_postulados():
    try:
        
        cursor = conn.cursor()
        cursor.execute("SELECT EMAIL, IS_VIABLE FROM INTERNS")
        data = cursor.fetchall()
        cursor.close()
        lista = []
        for i in range(len(data)):
            lista.append({"email":data[i][0],
                          "viable":data[i][1]})
            
        
        return lista
        
    except Exception as e:
        return {"error": e}

def datos_practicante(email):
    try:
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INTERNS WHERE EMAIL= %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user== None:
            return {"error": "El usuario no existe"}
        
        data = {"email": user[0],
                "fullname": user[1],
                "phone": user[2],
                "degree":user[3],
                "semester":user[4],
                "cv_route":user[5],
                "viable":user[6]
                }
        return data
    except Exception as e:
        return {"error": e}
    


# -- UPDATE --
def cambiar_viable(email, viable):
    try:
        
        cursor = conn.cursor()
        cursor.execute("UPDATE INTERNS SET IS_VIABLE=%s  WHERE EMAIL= %s", (viable, email))
        conn.commit()
        cursor.close()
        return {"mensaje": "cambio realizado"}, 200
    except Exception as e:
        return {"error": e}, 500

# -- DELETE --
def borrar_postulacion(email):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM INTERNS WHERE EMAIL= %s", (email,))
        conn.commit()
        cursor.close()
        return {"success": True,
                "message": "Postulación eliminada correctamente"}
    except Exception as e:
        return {
            "success": False,
            "error": e}
    