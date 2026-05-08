import utils.conexion_BD as conn
import utils.entidades as entidades

class usuario_bd:
    def HacerLogin(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT usuario_id, perfil FROM usuarios WHERE username = %s AND password = %s"
        self.cursor1.execute(sql, (Usuario.get_username(), Usuario.get_password()))
        resultado = self.cursor1.fetchone()
        self.con.close()     
        if resultado:
            return resultado[0], resultado[1]  # Retorna Id y perfil
        else:
            return False  # Usuario inválido