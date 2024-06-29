from flask import Flask, render_template, request
import database as db
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "src", "template")

app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    usuarios = db.get_usuarios()
    return render_template("services.html", usuario=usuarios)

@app.route("/contact", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        consulta = request.form["consulta"]
        mensaje = request.form["mensaje"]
        imagen = request.files["imagen"]
        promocion = request.form.get("promocion")
        
        db.add_user(nombre, email, consulta, mensaje, promocion, imagen)
        return render_template("contact.html")

    if request.method == "GET":
        return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
