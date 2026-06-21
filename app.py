from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def registro():
    return render_template("registro.html")


@app.route("/login")
def login():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)

