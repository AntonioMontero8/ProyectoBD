import utils.conexion_BD as conn
import utils.entidades as entidades

class cliente_bd:
    def Buscar(self, Cliente):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT cliente_id, nombre, telefono,email, rfc, CP_domicilio_fiscal, regimen_fiscal, tipo_cliente_park, tipo_cliente_pens FROM clientes WHERE cliente_id = %s"
        self.cursor1.execute(sql, (Cliente.get_cliente_id(),))
        resultado = self.cursor1.fetchone()

        if resultado:
            client = entidades.Cliente()
            client.set_cliente_id(resultado[0])
            client.set_nombre(resultado[1])
            client.set_telefono(resultado[2])
            client.set_email(resultado[3])
            client.set_rfc(resultado[4])
            client.set_CP_domicilio_fiscal(resultado[5])
            client.set_regimen_fiscal(resultado[6])
            client.set_tipo_cliente_park(resultado[7])
            client.set_tipo_cliente_pens(resultado[8])
            self.con.close()
            return client
        else:
            self.con.close()
            return None
        
    def Guardar(self, Cliente):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        self.sql = "INSERT INTO clientes(nombre, telefono, email, rfc, CP_domicilio_fiscal, regimen_fiscal) values (%s, %s, %s ,%s, %s, %s)"
        self.cursor1.execute(self.sql, (Cliente.get_nombre(), Cliente.get_telefono(), Cliente.get_email(), Cliente.get_rfc(), Cliente.get_CP_domicilio_fiscal(), Cliente.get_regimen_fiscal()))
        self.con.commit()
        self.con.close()
        
    def Borrar(self, Cliente):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        cliente = entidades.Cliente()
        cliente.set_cliente_id(Cliente.get_cliente_id())
        sql = "DELETE FROM clientes WHERE cliente_id = %s"
        self.cursor1.execute(sql, (cliente.get_cliente_id(),))
        self.con.commit()
        if self.con.is_connected():
            self.cursor1.close()
            self.con.close()
    
    def Editar(self, Cliente):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        self.sql = """
                    UPDATE clientes 
                    SET nombre = %s, telefono = %s, email = %s, rfc = %s, CP_domicilio_fiscal = %s, regimen_fiscal = %s
                    WHERE cliente_id = %s
                """ 
        self.cursor1.execute(self.sql, (
            Cliente.get_nombre(), 
            Cliente.get_telefono(), 
            Cliente.get_email(), 
            Cliente.get_rfc(), 
            Cliente.get_CP_domicilio_fiscal(), 
            Cliente.get_regimen_fiscal()
            ,Cliente.get_cliente_id()
        ))
        self.con.commit()
        if self.con.is_connected():
            self.cursor1.close()
            self.con.close()
        
    def Actualizar_Visitas_Dias(self, cliente_id, cantidad, tipo_servicio):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        try:
            # Aquí depende del tipo de servicio para saber qué sumar
            if "estacionamiento" in tipo_servicio or "parking" in tipo_servicio:
                sql = "UPDATE clientes SET visitas = visitas + %s WHERE cliente_id = %s"
            else:
                sql = "UPDATE clientes SET tiempo_pension = tiempo_pension + %s WHERE cliente_id = %s"
            
            self.cursor1.execute(sql, (cantidad, cliente_id))
            self.con.commit()
            self.con.close()
            return True
        except Exception as e:
            print(f"Error al sumar visitas/días al cliente: {e}")
            self.con.rollback()
            self.con.close()
            return False    
    