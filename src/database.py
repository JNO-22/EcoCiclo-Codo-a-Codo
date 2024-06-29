import mysql.connector
import base64

database = mysql.connector.connect(
    host="localhost", user="root", password="Zilex189", database="python_db"
)


def get_usuarios():
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email, consulta, promocion FROM usuarios")
    users = list(cursor)
    cursor.execute("SELECT imagen FROM usuarios")
    image = list(cursor)
    for user in users:
        user["imagen"] = base64.b64encode(image[users.index(user)]["imagen"]).decode("utf-8")
    return users
    


def add_user(nombre, email, consulta, mensaje, promocion, imagen):
    print(imagen)
    cursor = database.cursor(dictionary=True)
    if promocion:
        promocion = 1
    else:
        promocion = 0
        
    if imagen:
        imagen_data = file_data(imagen)
        cursor.execute("INSERT INTO usuarios (nombre, email, consulta, mensaje, promocion, imagen) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, email, consulta, mensaje, promocion, imagen_data))
    else:
        cursor.execute("INSERT INTO usuarios (nombre, email, consulta, mensaje, promocion) VALUES (%s, %s, %s, %s, %s)", (nombre, email, consulta, mensaje, promocion))

    database.commit()
    return cursor.lastrowid

def file_data (imagen):
    content = imagen.read()
    return content

