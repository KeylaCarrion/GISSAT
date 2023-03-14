import mysql.connector


# Conexion basen de datos

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="prueba"
)


