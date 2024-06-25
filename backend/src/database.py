import mysql.connector
import base64

database = mysql.connector.connect(
    host="localhost", user="root", password="Zilex189", database="python_db"
)


def get_usuarios():
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    return users


def add_user(nombre, email, consulta, mensaje, promocion, imagen):
    cursor = database.cursor(dictionary=True)
    if promocion:
        promocion = 1
    else:
        promocion = 0
        
    if imagen:
        with open(imagen, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, consulta, mensaje, promocion, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, email, consulta, mensaje, promocion, encoded_image),
        )
    else:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, consulta, mensaje, promocion) VALUES (%s, %s, %s, %s, %s)",
            (nombre, email, consulta, mensaje, promocion),
        )

    database.commit()
    return cursor.lastrowid
