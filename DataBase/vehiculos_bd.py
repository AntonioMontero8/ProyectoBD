import mysql.connector
import utils.conexion_BD as conn
from utils.entidades import Vehiculo
import utils.entidades as entidades

class vehiculos_bd:
    def buscar(self, matricula):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT matricula, modelo, marca, color, cliente_id FROM vehiculos WHERE matricula = %s "
        self.cursor1.execute(sql, (matricula,))
        resultado = self.cursor1.fetchone()
        self.con.close()     
        if resultado:
            return resultado
        else:
            return False
        
    def guardar(self,vehiculo:Vehiculo):
        try:
            self.con = conn.conection().connect()
            self.cursor1 = self.con.cursor()
            sql = """
            INSERT INTO vehiculos
            (matricula, modelo, marca, color, cliente_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (
                vehiculo.get_matricula(),
                vehiculo.get_modelo(),
                vehiculo.get_marca(),
                vehiculo.get_color(),
                vehiculo.get_cliente_id()
            )
            self.cursor1.execute(sql,valores)
            self.con.commit()
            self.con.close() 
            return True, "Vehículo guardado correctamente"
        
        except mysql.connector.Error as e:
            if e.errno == 1062:
                return False, "La matrícula ya existe"

            elif e.errno == 1452:
                return False, "El cliente_id no existe"

            return False, f"Error MariaDB: {e}"
        finally:
            if hasattr(self, 'con') and self.con.is_connected():
                self.con.close()
        
        
    def BuscarPorCliente(self, Cliente):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT matricula, marca, modelo, color, cliente_id FROM vehiculos WHERE cliente_id = %s"
        self.cursor1.execute(sql, (Cliente.get_cliente_id(),))
        resultados = self.cursor1.fetchall()
        
        lista_vehiculos = []
        for res in resultados:
            v = entidades.Vehiculo()
            v.set_matricula(res[0])
            v.set_marca(res[1])
            v.set_modelo(res[2])
            v.set_color(res[3])
            v.set_cliente_id(res[4])
            lista_vehiculos.append(v)
            
        self.con.close()
        return lista_vehiculos

    def eliminar(self, matricula):
        try:
            self.con = conn.conection().connect()
            self.cursor1 = self.con.cursor()
            sql = "DELETE FROM vehiculos WHERE matricula = %s"
            self.cursor1.execute(sql, (matricula,))
            self.con.commit()
            return True, "Vehículo eliminado correctamente"
        except mysql.connector.Error as e:
            return False, f"Error al eliminar: {e}"
        finally:
            if hasattr(self, 'con') and self.con.is_connected():
                self.con.close()

    def editar(self, vehiculo: Vehiculo):
        try:
            self.con = conn.conection().connect()
            self.cursor1 = self.con.cursor()
            sql = """
            UPDATE vehiculos 
            SET modelo = %s, marca = %s, color = %s, cliente_id = %s 
            WHERE matricula = %s
            """
            valores = (
                vehiculo.get_modelo(),
                vehiculo.get_marca(),
                vehiculo.get_color(),
                vehiculo.get_cliente_id(),
                vehiculo.get_matricula()
            )
            self.cursor1.execute(sql, valores)
            self.con.commit()
            return True, "Vehículo actualizado correctamente"
        except mysql.connector.Error as e:
            return False, f"Error al actualizar: {e}"
        finally:
            if hasattr(self, 'con') and self.con.is_connected():
                self.con.close()