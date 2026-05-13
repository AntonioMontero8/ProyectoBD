import utils.conexion_BD as conn
import utils.entidades as entidades

class usuario_bd:
    def HacerLogin(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT usuario_id, tipo_usuario FROM usuarios WHERE username = %s AND password = %s AND estado = 1"
        self.cursor1.execute(sql, (Usuario.get_username(), Usuario.get_password()))
        resultado = self.cursor1.fetchone()
        self.con.close()
        if resultado:
            return resultado[0], resultado[1]  # Retorna Id y tipo_usuario
        else:
            return False  # Usuario inválido

    def Buscar(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "SELECT usuario_id, nombre, username, password, tipo_usuario FROM usuarios WHERE usuario_id = %s AND estado = 1"
        self.cursor1.execute(sql, (Usuario.get_usuario_id(),))
        resultado = self.cursor1.fetchone()

        if resultado:
            usuario = entidades.Usuario()
            usuario.set_usuario_id(resultado[0])
            usuario.set_nombre(resultado[1])
            usuario.set_username(resultado[2])
            usuario.set_password(resultado[3])
            usuario.set_tipo_usuario(resultado[4])
            self.con.close()
            return usuario
        else:
            self.con.close()
            return None

    def Guardar(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "INSERT INTO usuarios(nombre, username, password, tipo_usuario) VALUES (%s, %s, %s, %s)"
        self.cursor1.execute(sql, (
            Usuario.get_nombre(),
            Usuario.get_username(),
            Usuario.get_password(),
            Usuario.get_tipo_usuario()
        ))
        self.con.commit()
        self.con.close()

    def Editar(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = """
            UPDATE usuarios
            SET nombre = %s, username = %s, password = %s, tipo_usuario = %s
            WHERE usuario_id = %s
        """
        self.cursor1.execute(sql, (
            Usuario.get_nombre(),
            Usuario.get_username(),
            Usuario.get_password(),
            Usuario.get_tipo_usuario(),
            Usuario.get_usuario_id()
        ))
        self.con.commit()
        self.con.close()

    def Borrar(self, Usuario):
        self.con = conn.conection().connect()
        self.cursor1 = self.con.cursor()
        sql = "UPDATE usuarios SET estado = 0 WHERE usuario_id = %s"
        self.cursor1.execute(sql, (Usuario.get_usuario_id(),))
        self.con.commit()
        self.con.close()