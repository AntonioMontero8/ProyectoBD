import utils.conexion_BD as conn
import utils.entidades as entidades

class cobro_bd:
    def BuscarCobro(self, Cobro): #Función para el query de buscar servicios por ID
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT folio_cobro, folio_servicio, tiempo_estancia, usuario_id, monto_total FROM cobros WHERE folio_servicio = %s"
        self.cursor1.execute(sql, (Cobro.get_folio_servicio(),))
        resultado = self.cursor1.fetchone()

        if resultado:
            cobro = entidades.Cobro()
            cobro.set_folio_cobro(resultado[0])
            cobro.set_folio_servicio(resultado[1])
            cobro.set_tiempo_estancia(resultado[2])
            cobro.set_usuario_id(resultado[3])
            cobro.set_monto_total(resultado[4])
            self.con.close()
            return cobro
        else:
            self.con.close()
            return None
        
    def Guardar(self, Cobro):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = """
            INSERT INTO cobros (folio_cobro, folio_servicio, tiempo_estancia, usuario_id, monto_total) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            Cobro.get_folio_cobro(),
            Cobro.get_folio_servicio(),
            Cobro.get_tiempo_estancia(),
            Cobro.get_usuario_id(),
            Cobro.get_monto_total()
        )
        try:
            self.cursor1.execute(sql, valores)
            self.con.commit()
            self.con.close()
            return True
        except Exception as e:
            print(f"Error al guardar el cobro: {e}")
            self.con.rollback()
            self.con.close()
            return False