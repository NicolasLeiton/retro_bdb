from flask import Flask, render_template, url_for, redirect, jsonify, session, request
from app_comp import bdd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def inicio():
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    session.clear()
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    respuesta = bdd.verificar_usuario(email, password)

    if respuesta["success"]:
        session["user_id"] = email
        session["is_analist"] = respuesta["is_analist"]
    
    return jsonify(respuesta)


@app.route("/registrar_user", methods=["POST"])
def registro_user():
    email = request.form.get("email")
    password = request.form.get("password")

    respuesta = bdd.agregar_usuario(email, password)
    if respuesta["success"]:
        session["user_id"] = email
        session["is_analist"] = False
    
    return jsonify(respuesta)



@app.route("/registro")
def registro_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    return render_template("registro.html")

@app.route("/registro", methods=["POST"])
def registro_cv():
    
    email = session["user_id"]
    print(email)
    phone = request.form.get("phone")
    fullname = request.form.get("fullname")
    career = request.form.get("career")
    semester = request.form.get("semester")

    cv = request.files.get("cv")

    if cv:
        ruta = secure_filename(email).replace(".", "_")
        ruta = f"uploads/{ruta}.pdf"
        cv.save(ruta)
    respuesta = bdd.agregar_registro(email, fullname, phone, career, semester, ruta)
    print(ruta, respuesta)
    return jsonify(respuesta)



if __name__ == "__main__":
    app.run(debug=True)

