import mysql.connector
import pandas as pd


class ModelPozos:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.conexion.cursor()

    def insertPozos_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            cursor = self.conexion.cursor()
            for i, row in df.iterrows():
                datos = (row['Pozos'], row['X'], row['Y'], row['Direccion'], row['Colonia'])
                cursor.execute(
                    "INSERT INTO pozo (Pozos, X, Y, Direccion, Colonia, tipo_idtipo) VALUES (%s, %s, %s, %s, %s, 1)",
                    datos)
            self.conexion.commit()
            cursor.close()

        except Exception as e:
            print("Error al insertar los datos", e)

        finally:
            self.cursor.close()

    def obtenerPozos(self):
        consulta = f"SELECT Pozos, X, Y, direccion  FROM pozo"
        self.cursor.execute(consulta)
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.conexion.close()
