import utils.conexion_BD as conn

class reportes_bd:
    def obtener_datos_meses(self, anio):
        self.con = conn.conection().connect()
        self.cursor = self.con.cursor()
        
        # Consultamos las entradas
        sql_ent = "SELECT SUBSTRING(fecha_entrada, 6, 2), COUNT(*) FROM servicios WHERE SUBSTRING(fecha_entrada, 1, 4) = %s GROUP BY SUBSTRING(fecha_entrada, 6, 2)"
        self.cursor.execute(sql_ent, (anio,))
        entradas = dict(self.cursor.fetchall())
        
        # Consultamos las salidas
        sql_sal = "SELECT SUBSTRING(fecha_salida, 6, 2), COUNT(*) FROM servicios WHERE SUBSTRING(fecha_salida, 1, 4) = %s AND fecha_salida != '' GROUP BY SUBSTRING(fecha_salida, 6, 2)"
        self.cursor.execute(sql_sal, (anio,))
        salidas = dict(self.cursor.fetchall())
        
        self.con.close()
        return entradas, salidas

    def obtener_ingresos(self, anio):
        self.con = conn.conection().connect()
        self.cursor = self.con.cursor()
        sql = """
            SELECT s.tipo_servicio, SUM(c.monto_total) 
            FROM cobros c 
            JOIN servicios s ON c.folio_servicio = s.folio_servicio 
            WHERE SUBSTRING(s.fecha_salida, 1, 4) = %s 
            GROUP BY s.tipo_servicio
        """
        self.cursor.execute(sql, (anio,))
        ingresos = dict(self.cursor.fetchall())
        self.con.close()
        return ingresos

    def obtener_horarios(self, anio):
        self.con = conn.conection().connect()
        self.cursor = self.con.cursor()
        sql = "SELECT SUBSTRING(hora_entrada, 1, 2), COUNT(*) FROM servicios WHERE SUBSTRING(fecha_entrada, 1, 4) = %s GROUP BY SUBSTRING(hora_entrada, 1, 2)"
        self.cursor.execute(sql, (anio,))
        horarios = dict(self.cursor.fetchall())
        self.con.close()
        return horarios

    def llamar_sp_historico(self):
        self.con = conn.conection().connect()
        self.cursor = self.con.cursor()
        self.cursor.callproc('SP_Top_Ingresos_Anuales')
        resultados = []
        for result in self.cursor.stored_results():
            resultados = result.fetchall()
        self.con.close()
        return resultados