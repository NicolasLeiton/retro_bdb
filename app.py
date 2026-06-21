from flask import Flask, render_template, url_for, redirect, jsonify

app = Flask(__name__)


@app.route("/")
def inicio():
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    respuesta = {
        "success": True,
        "message": "Login fallido"
    }
    if respuesta["success"]:
        return jsonify(respuesta)
    
    return jsonify(respuesta)

@app.route("/registrar_user", methods=["POST"])
def registro_user():
    respuesta = {
        "success": True,
        "message": "Login fallido"
    }
    if respuesta["success"]:
        return jsonify(respuesta)
    
    return jsonify(respuesta)



@app.route("/registro")
def registro_page():
    return render_template("registro.html")

@app.route("/registro", methods=["POST"])
def registro_cv():
    respuesta = {
        "success": False,
        "message": "Registro fallido"
    }
    return jsonify(respuesta)



if __name__ == "__main__":
    app.run(debug=True)

