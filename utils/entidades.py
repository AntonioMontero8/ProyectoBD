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

class Servicio:
    def __init__(self):        
        self._folio_servicio = 0
        self._estacionamiento_id = 0
        self._matricula = ""
        self._fecha_entrada = ""
        self._hora_entrada = ""
        self._fecha_salida = ""
        self._hora_salida = ""
        self._folio_precio = 0
        self._tipo_servicio = ""

    def get_folio_servicio(self):
        return self._folio_servicio

    def set_folio_servicio(self, valor):
        self._folio_servicio= valor

    def get_estacionamiento_id(self):
        return self._estacionamiento_id

    def set_estacionamiento_id(self, valor):
        self._estacionamiento_id = valor

    def get_matricula(self):
        return self._matricula

    def set_matricula(self, valor):
        self._matricula = valor

    def get_fecha_entrada(self):
        return self._fecha_entrada

    def set_fecha_entrada(self, valor):
        self._fecha_entrada = valor

    def get_hora_entrada(self):
        return self._hora_entrada

    def set_hora_entrada(self, valor):
        self._hora_entrada = valor

    def get_fecha_salida(self):
        return self._fecha_salida

    def set_fecha_salida(self, valor):
        self._fecha_salida = valor

    def get_hora_salida(self):
        return self._hora_salida

    def set_hora_salida(self, valor):
        self._hora_salida = valor

    def get_folio_precio(self):
        return self._folio_precio

    def set_folio_precio(self, valor):
        self._folio_precio = valor

    def get_tipo_servicio(self):
        return self._tipo_servicio

    def set_tipo_servicio(self, valor):
        self._tipo_servicio = valor

class Precio:
    def __init__(self):        
        self._folio_precio = 0
        self._tipo = ""
        self._monto = 0

    def get_folio_precio(self):
        return self._folio_precio

    def set_folio_precio(self, valor):
        self._folio_precio= valor

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, valor):
        self._tipo = valor

    def get_monto(self):
        return self._monto

    def set_monto(self, valor):
        self._monto = valor

class Estacionamiento:
    def __init__(self):        
        self._estacionamiento_id = 0
        self._nombre = ""
        self._direccion = ""
        self._cantidad_cajones = 0

    def get_estacionamiento_id(self):
        return self._estacionamiento_id

    def set_estacionamiento_id(self, valor):
        self._estacionamiento_id = valor

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_direccion(self):
        return self._direccion

    def set_direccion(self, valor):
        self._direccion = valor
    
    def get_cantidad_cajones(self):
        return self._cantidad_cajones

    def set_cantidad_cajones(self, valor):
        self._cantidad_cajones = valor

class Cobro:
    def __init__(self):        
        self._folio_cobro = ""
        self._folio_servicio = 0
        self._tiempo_estancia = ""
        self._usuario_id = 0
        self._monto_total = 0

    def get_folio_cobro(self):
        return self._folio_cobro

    def set_folio_cobro(self, valor):
        self._folio_cobro = valor

    def get_folio_servicio(self):
        return self._folio_servicio

    def set_folio_servicio(self, valor):
        self._folio_servicio = valor

    def get_tiempo_estancia(self):
        return self._tiempo_estancia

    def set_tiempo_estancia(self, valor):
        self._tiempo_estancia = valor
    
    def get_usuario_id(self):
        return self._usuario_id

    def set_usuario_id(self, valor):
        self._usuario_id = valor
    
    def get_monto_total(self):
        return self._monto_total

    def set_monto_total(self, valor):
        self._monto_total = valor
