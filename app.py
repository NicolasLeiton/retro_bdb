from flask import Flask, render_template, url_for, redirect, jsonify, session, request, send_file
from app_comp import bdd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def inicio():
    return redirect(url_for("login_page"))

# -- PAGINA DE LOGIN  --
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


# -- PAGINA DE REGISTRO --
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

# Funcion para verificar permisos
def verificar_analista():
    return "is_analist" not in session or session["is_analist"]==False

# -- PAGINA RECLUTADOR --
@app.route("/reclutador")
def reclutador():
    if verificar_analista():
        return redirect(url_for("login_page"))
    return render_template("reclutador.html")

@app.route("/lista_practicantes")
def lista():
    if verificar_analista():
        return redirect(url_for("login_page"))
    return jsonify(bdd.lista_postulados())

@app.route("/practicante")
def practicante():
    if verificar_analista():
        return redirect(url_for("login_page"))
    email = request.args.get("email")
    return jsonify(bdd.datos_practicante(email))

@app.route("/marcar_viable", methods=["POST"])
def marcar_viable():
    if verificar_analista():
        return redirect(url_for("login_page"))
    
    datos = request.get_json()
    email = datos.get("email")
    viable = datos.get("viable")
    print(email, viable)
    return bdd.cambiar_viable(email, viable)

@app.route("/descargar_cv")
def descargar_cv():
    if verificar_analista():
        return redirect(url_for("login_page"))
    ruta = request.args.get("cv_route")
    return send_file(
        ruta,
        as_attachment=True
    )

# Iniciar app
if __name__ == "__main__":
    app.run(debug=True)

