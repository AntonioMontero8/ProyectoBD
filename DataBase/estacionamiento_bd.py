import utils.conexion_BD as conn
import utils.entidades as entidades

class estacionamiento_bd:
    def Buscar(self, Estacionamiento):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT nombre, direccion, cantidad_cajones FROM estacionamientos WHERE estacionamiento_id = %s"
        self.cursor1.execute(sql, (Estacionamiento.get_estacionamiento_id(),))
        resultado = self.cursor1.fetchone()
        if resultado:
            estacionamiento = entidades.Estacionamiento()
            estacionamiento.set_estacionamiento_id(Estacionamiento.get_estacionamiento_id())
            estacionamiento.set_nombre(resultado[0])
            estacionamiento.set_direccion(resultado[1])
            estacionamiento.set_cantidad_cajones(resultado[2])
            return estacionamiento
        else:
            if self.con.is_connected():
                self.cursor1.close()
                self.con.close()
                return None  # No se encontró el estacionamiento

    def Guardar(self, Estacionamiento):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "INSERT INTO estacionamientos (nombre, direccion, cantidad_cajones) VALUES (%s, %s, %s)"
        self.cursor1.execute(sql, (Estacionamiento.get_nombre(), Estacionamiento.get_direccion(), Estacionamiento.get_cantidad_cajones()))
        self.con.commit()
        if self.con.is_connected():
            self.cursor1.close()
            self.con.close()

    def Editar(self, Estacionamiento):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "UPDATE estacionamientos SET nombre = %s, direccion = %s, cantidad_cajones = %s WHERE estacionamiento_id = %s"
        self.cursor1.execute(sql, (
            Estacionamiento.get_nombre(), 
            Estacionamiento.get_direccion(), 
            Estacionamiento.get_cantidad_cajones(),
            Estacionamiento.get_estacionamiento_id()
        ))
        self.con.commit()
        if self.con.is_connected():
            self.cursor1.close()
            self.con.close()

    def Borrar(self, Estacionamiento):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "DELETE FROM estacionamientos WHERE estacionamiento_id = %s"
        self.cursor1.execute(sql, (Estacionamiento.get_estacionamiento_id(),))
        self.con.commit()
        if self.con.is_connected():
            self.cursor1.close()
            self.con.close()