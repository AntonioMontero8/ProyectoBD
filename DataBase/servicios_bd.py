import utils.conexion_BD as conn
import utils.entidades as entidades

class servicios_bd:
    def Buscar(self, Servicio): #Función para el query de buscar servicios por ID
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT folio_servicio, estacionamiento_id, matricula, fecha_entrada, hora_entrada, fecha_salida, hora_salida, folio_precio, tipo_servicio FROM servicios WHERE folio_servicio = %s"
        self.cursor1.execute(sql, (Servicio.get_folio_servicio(),))
        resultado = self.cursor1.fetchone()

        if resultado:
            servicio = entidades.Servicio()
            servicio.set_folio_servicio(resultado[0])
            servicio.set_estacionamiento_id(resultado[1])
            servicio.set_matricula(resultado[2])
            servicio.set_fecha_entrada(resultado[3])
            servicio.set_hora_entrada(resultado[4])
            servicio.set_fecha_salida(resultado[5])
            servicio.set_hora_salida(resultado[6])
            servicio.set_folio_precio(resultado[7])
            servicio.set_tipo_servicio(resultado[8])
            self.con.close()
            return servicio
        else:
            self.con.close()
            return None
        
    def Guardar_Servicio(self, Servicio): #Función para almacenar servicios por primera vez (con datos vacios en el registro)
            self.con = conn.conection().connect()
            self.cursor1 = self.con.cursor()
            
            sql = """
                INSERT INTO servicios 
                (estacionamiento_id, matricula, fecha_entrada, hora_entrada, fecha_salida, hora_salida, folio_precio, tipo_servicio) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Comprobamos los datos vacios para cambiarlos a formato valido en MySQL y evitar errores
            fecha_salida = Servicio.get_fecha_salida() if Servicio.get_fecha_salida() else None
            hora_salida = Servicio.get_hora_salida() if Servicio.get_hora_salida() else None
            folio_precio = Servicio.get_folio_precio() if Servicio.get_folio_precio() != 0 else None

            valores = (
                Servicio.get_estacionamiento_id(),
                Servicio.get_matricula(),
                Servicio.get_fecha_entrada(),
                Servicio.get_hora_entrada(),
                fecha_salida,
                hora_salida,
                folio_precio,
                Servicio.get_tipo_servicio()
            )
            
            try:
                self.cursor1.execute(sql, valores)
                self.con.commit() #Almacenamos la entrada en la base de datos
                
                #Conseguimos el folio para que se continue almacenando de manera correcta
                nuevo_folio = self.cursor1.lastrowid
                Servicio.set_folio_servicio(nuevo_folio)
                
                self.con.close()
                return True
                
            except Exception as e:
                print(f"Error al insertar en la base de datos: {e}")
                self.con.rollback() #Cancelamos la transacción en caso de error
                self.con.close()
                return False