class Usuario:
    def __init__(self):
        self._usuario_id = 0
        self._nombre = ""
        self._email = ""
        self._username = ""
        self._password = ""
        self._tipo_usuario = ""

    def get_usuario_id(self):
        return self._usuario_id

    def set_usuario_id(self, valor):
        self._usuario_id = valor

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_email(self):
        return self._email

    def set_email(self, valor):
        self._email = valor

    def get_username(self):
        return self._username

    def set_username(self, valor):
        self._username = valor

    def get_password(self):
        return self._password

    def set_password(self, valor):
        self._password = valor

    def get_tipo_usuario(self):
        return self._tipo_usuario

    def set_tipo_usuario(self, valor):
        self._tipo_usuario = valor
        
class Cliente:
    def __init__(self):        
        self._cliente_id = 0
        self._nombre = ""
        self._telefono = ""
        self._email = ""
        self._rfc = ""
        self._CP_domicilio_fiscal = ""
        self._regimen_fiscal = ""
        self._tipo_cliente_park = ""
        self._tipo_cliente_pens = ""
        self._visitas = 0
        self._tiempo_pension = 0

    def get_cliente_id(self):
        return self._cliente_id

    def set_cliente_id(self, valor):
        self._cliente_id = valor

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_telefono(self):
        return self._telefono

    def set_telefono(self, valor):
        self._telefono = valor

    def get_email(self):
        return self._email

    def set_email(self, valor):
        self._email = valor

    def get_rfc(self):
        return self._rfc

    def set_rfc(self, valor):
        self._rfc = valor

    def get_CP_domicilio_fiscal(self):
        return self._CP_domicilio_fiscal

    def set_CP_domicilio_fiscal(self, valor):
        self._CP_domicilio_fiscal = valor

    def get_regimen_fiscal(self):
        return self._regimen_fiscal

    def set_regimen_fiscal(self, valor):
        self._regimen_fiscal = valor

    def get_tipo_cliente_park(self):
        return self._tipo_cliente_park

    def set_tipo_cliente_park(self, valor):
        self._tipo_cliente_park = valor

    def get_tipo_cliente_pens(self):
        return self._tipo_cliente_pens

    def set_tipo_cliente_pens(self, valor):
        self._tipo_cliente_pens = valor

    def get_visitas(self):
        return self._visitas

    def set_visitas(self, valor):
        self._visitas = valor

    def get_tiempo_pension(self):
        return self._tiempo_pension

    def set_tiempo_pension(self, valor):
        self._tiempo_pension = valor
        

class Vehiculo:
    def __init__(self):
        self._matricula = ""
        self._modelo = ""
        self._marca = ""
        self._color = ""
        self._cliente_id = 0

    def get_matricula(self):
        return self._matricula

    def set_matricula(self, valor):
        self._matricula = valor

    def get_modelo(self):
        return self._modelo

    def set_modelo(self, valor):
        self._modelo = valor

    def get_marca(self):
        return self._marca

    def set_marca(self, valor):
        self._marca = valor

    def get_color(self):
        return self._color

    def set_color(self, valor):
        self._color = valor

    def get_cliente_id(self):
        return self._cliente_id

    def set_cliente_id(self, valor):
        self._cliente_id = valor
