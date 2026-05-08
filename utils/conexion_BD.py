import mysql.connector

class conection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "estacionamiento"
        self.conn = None
        
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
            return self.conn
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            print("Conexión cerrada.")