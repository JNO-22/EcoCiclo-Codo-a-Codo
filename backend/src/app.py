from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import database as db
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "src", "template")

app = Flask(__name__, template_folder=template_dir)


@app.route("/form", methods=["POST", "GET"])
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

print(db.get_usuarios())
