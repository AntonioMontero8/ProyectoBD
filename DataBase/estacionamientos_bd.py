import utils.conexion_BD as conn
import utils.entidades as entidades

class estacionamiento_bd:
    def Buscar(self, Estacionamiento):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT estacionamiento_id, nombre, direccion, cantidad_cajones FROM estacionamientos WHERE estacionamiento_id = %s"
        self.cursor1.execute(sql, (Estacionamiento.get_estacionamiento_id(),))
        result = self.cursor1.fetchone()
        if result:
            parking  = entidades.Estacionamiento()
            parking.set_estacionamiento_id(result[0])
            parking.set_nombre(result[1])
            parking.set_direccion(result[2])
            parking.set_cantidad_cajones(result[3])
        
            self.con.close()
            return parking
        else:
            self.con.close()
            return None