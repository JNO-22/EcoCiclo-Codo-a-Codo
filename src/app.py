from flask import Flask, render_template, request
import os
from models.Consultas import Consultas

print(os.path.abspath)

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "src", "template")

app = Flask(__name__, template_folder=template_dir)


consulta = Consultas()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    data = consulta.get_usuarios_reclamos()
    return render_template("services.html", data=data)


@app.route("/contact", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        tipo_consulta = request.form["consulta"]
        mensaje = request.form["mensaje"]
        imagen = request.files["imagen"]
        promocion = request.form.get("promocion")

        consulta.add_user(nombre, email, tipo_consulta, promocion, imagen, mensaje)
        return render_template("contact.html")

    if request.method == "GET":
        return render_template("contact.html")


@app.route("/modify-data", methods=["POST", "GET"])
def modify_data():
    if request.method == "POST":
        
        if request.form["form"] == 'editar':
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            tipo_consulta = request.form["consulta"]
            imagen = request.files['imagen']
            consulta.update_user(id,name, email, message, imagen,tipo_consulta)
            usuarios = consulta.get_usuarios('name', name)
            
        elif request.form["form"] == 'consulta':
            eleccion = request.form["eleccion"]
            data = request.form["datos"]
            usuarios = consulta.get_usuarios(eleccion, data)
            
        elif request.form["form"] == 'borrar':
            name = request.form['name']
            id = request.form['id']
            consulta.delete_user(id)
            usuarios = consulta.get_usuarios('name', name)
            
        
        
        return render_template("modify-data.html", data=usuarios)

    if request.method == "GET":
        return render_template("modify-data.html")


if __name__ == "__main__":
    app.run(debug=True)
