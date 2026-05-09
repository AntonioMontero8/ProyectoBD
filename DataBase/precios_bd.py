import utils.conexion_BD as conn
import utils.entidades as entidades

class precio_bd:
    def obtener_todos(self):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT folio_precio, tipo, monto FROM precios"
        self.cursor1.execute(sql)
        precios = self.cursor1.fetchall()
        lista_precios = []
        if precios:
            for fila in precios:
                precio = entidades.Precio()
                precio.set_folio_precio(fila[0])
                precio.set_tipo(fila[1])
                precio.set_monto(fila[2])
                lista_precios.append(precio)
        
        self.con.close()

        return lista_precios