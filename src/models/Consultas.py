from flask import jsonify
import mysql.connector
import base64

import mysql.connector.errorcode

class Consultas:
    def __init__(self):
        # editar en python anywhere ### ALERTA
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Zilex189",
            database="python_db",
            
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {'python_db'}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {'python_db'}")
                self.conn.database = "python_db"
            else:
                print(err)
                self.conn.close()
                raise err

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS consultas 
            (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), 
            email VARCHAR(255), consulta VARCHAR(255), promocion BOOLEAN,
            imagen LONGBLOB, mensaje LONGTEXT)"""
        )
        self.conn.commit()
        self.cursor.close()

    def get_usuarios(self, eleccion, data):
        self.cursor = self.conn.cursor(dictionary=True)
        if eleccion == "name":
            self.cursor.execute(
                "SELECT * FROM consultas WHERE REGEXP_LIKE (nombre, %s)", (data,)
            )
        elif eleccion == "mail":
            self.cursor.execute(
                "SELECT * FROM consultas WHERE REGEXP_LIKE (email, %s)", (data,)
            )
        users = list(self.cursor)
        for user in users:
            if user["imagen"] is not None:
                user["imagen"] = base64.b64encode(user["imagen"]).decode("utf-8")
            else:
                user["imagen"] = ""
        self.cursor.close()
        return users

    def get_usuarios_reclamos(self):
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute("SELECT * FROM consultas WHERE consulta = 'reporte'")
        users = list(self.cursor)
        for user in users:
            if user["imagen"] is not None:
                user["imagen"] = base64.b64encode(user["imagen"]).decode("utf-8")
            else:
                user["imagen"] = ""
        self.cursor.close()
        return users

    def add_user(self, nombre, email, consulta, promocion, imagen, mensaje):
        self.cursor = self.conn.cursor(dictionary=True)
        try:
            if promocion:
                promocion = 1
            else:
                promocion = 0

            if imagen:
                imagen_data = file_data(imagen)
                self.cursor.execute(
                    "INSERT INTO consultas (nombre, email, consulta, promocion, imagen, mensaje) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, email, consulta, promocion, imagen_data, mensaje),
                )
            else:
                self.cursor.execute(
                    "INSERT INTO consultas (nombre, email, consulta, promocion, mensaje) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, email, consulta, promocion, mensaje),
                )
            self.conn.commit()
            print("Data inserted successfully")
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)
        self.cursor.close()

    def update_user(self, id, nombre, email, mensaje, imagen, consulta):
        self.cursor = self.conn.cursor(dictionary=True)
        query = "UPDATE consultas SET"
        values = []
        if imagen:
            imagen = file_data(imagen)
        else:
            imagen = None
        for key, value in locals().items():
            if key != "self" and key != "query" and key != "values" and key != "id":
                if value is not None:
                    query += f" {key} = %s,"
                    values.append(value)

        query = query[:-1] + f" WHERE id = {id}"
        print(query, tuple(values))
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        print("Data updated successfully")
        self.cursor.close()
        
    def delete_user(self, id):
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute(f"DELETE FROM consultas WHERE id = {id}")
        self.conn.commit()
        print("Data deleted successfully")
        self.cursor.close()
        
def file_data(imagen):
    content = imagen.read()
    return content
