from Loaders import Loader
from Validations import Validator


class Resultado:
    def __init__(
            self,
            codigo_reclamo='',
            fecha_reclamo='',
            fecha_sernac='',
            tipo_contrato='',
            codigo_producto='',
            codigo_origen='',
            descripcion_origen='',
            rut='',
            nombre='',
            fecha_creacion='',
            n_cuenta='',
            linea_sobregiro='',
            n_tarjeta='',
            fecha_vencimiento='',
            cupo_nacional='',
            cupo_internacional=''):

        #Se setean las variables con los valores recibidos
        self.codigo_reclamo = codigo_reclamo
        self.fecha_reclamo = fecha_reclamo
        self.fecha_sernac = fecha_sernac
        self.tipo_contrato = tipo_contrato
        self.codigo_producto = codigo_producto
        self.codigo_origen = codigo_origen
        self.descripcion_origen = descripcion_origen
        self.rut = rut
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.n_cuenta = n_cuenta
        self.linea_sobregiro = linea_sobregiro
        self.n_tarjeta = n_tarjeta
        self.fecha_vencimiento = fecha_vencimiento
        self.cupo_nacional = cupo_nacional
        self.cupo_internacional = cupo_internacional

        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl('resultado.fdl')

    #Metodo para cargar una linea
    def load_line(self, resultado=""):
        #Se separa la linea usando el caracter "#". Se guarda en una lista
        resultado = resultado.split("#")

        #Se recorre la lista y se obtiene el numero de iteracion
        for i, v in enumerate(resultado):
            #Buscamos el atributo que corresponde segun el FDL usando el numero de iteracion
            attrName = self.descriptor[i]

            #Seteamos el atributo que corresponde
            setattr(self, attrName, v)

        #Se devuelve el indice
        return self.codigo_reclamo

    #Metodo que guarda un cruce
    def save_resultado(self, result_file):
        #Se carga el descriptor de resultado desde Resultado.fdl
        loader = Loader()
        self.descriptor = loader.load_fdl('resultado.fdl')

        #Se crea una lista vacia donde iran guardandose los parametros
        #Si algun parametro no existe se guardara un string vacio para no perder
        #la correlacion con el FDL
        result = []

        #Por cada elemento descrito en el FDL buscaremos el valor
        for attrName in self.descriptor:
            #Se guarda el valor al final de la lista de resultado
            result.append(getattr(self, attrName))

        #Se unen todos los resultados separandolos con #, al final se le agrega un salto de linea
        result = "#".join(result) + '\n'

        #Se abre el archivo de resultado en modo de escritura con un puntero al final
        f = open("./Results/" + result_file, "a")
        #Se escribe el resultado
        f.write(result)
        #Se cierra el archivo
        f.close()

    def formatDate(self, value):
        return value[0:4] + "-" + value[4:6] + "-" + value[6:8]

    def validate(self):
        validator = Validator()

        error = []

        if not validator.isInt(self.codigo_reclamo):
            error.append("El codigo de reclamo es erroneo")

        if not validator.isValidDate(self.fecha_reclamo):
            error.append("la fecha de reclamo es erronea")

        if not validator.isValidDate(self.fecha_sernac):
            error.append("la fecha sernac es erronea")

        if not validator.isInt(self.tipo_contrato):
            error.append("El tipo de contrato es erroneo")

        if not validator.isInt(self.codigo_producto):
            error.append("El codigo de producto es erroneo")

        if not validator.isInt(self.codigo_origen):
            error.append("El codigo de origen es erroneo")

        if validator.isEmpty(self.descripcion_origen):
            error.append("la descripcion de origen es erronea")

        if not validator.validRUT(self.rut):
            error.append("El RUT es erroneo")

        if validator.isEmpty(self.nombre):
            error.append("El nombre es erroneo")

        if not validator.isValidDate(self.fecha_creacion):
            error.append("la fecha de creacion es erronea")

        # Si los 2 numeros de producto son nulos hay un error
        if (not validator.isInt(self.n_cuenta)) and (not validator.isInt(self.n_tarjeta)):
            error.append("El reclamo no esta asociado a una cuenta ni a una tarjeta")

        # Si viene la tarjeta y la cuenta completa, hay un error, solo puede ser 1
        if validator.isInt(self.n_cuenta) and validator.isInt(self.n_tarjeta):
            error.append("El reclamo esta asociaco a una cuenta y a una tarjeta")

        if validator.isInt(self.n_cuenta):
            if not validator.isBoolean(self.linea_sobregiro):
                error.append("La informacion sobre linea de sobregiro es erronea")
        else:
            if not validator.isValidDate(self.fecha_vencimiento):
                error.append("la fecha de vencimiento es erronea")
            if not validator.isInt(self.cupo_nacional):
                error.append("El cupo nacional es erroneo")
            if not validator.isInt(self.cupo_internacional):
                error.append("El cupo internacional es erroneo")

        isValid = False if len(error) else True

        return {"isValid": isValid, "errors": error}

    def isDuplicated(self, cursor):
        error = []

        # No se puede tener un codigo de reclamo que ya exista en la DB
        if cursor.execute("SELECT * FROM reclamos WHERE codigo_reclamo = %s", self.codigo_reclamo):
            error.append("El codigo de reclamo ya fue ingresado")

        # Verificar si el rut existe, si existe el nombre para el rut debe coincidir
        if cursor.execute("SELECT * FROM clientes WHERE rut = %s", self.rut):
            cliente = cursor.fetchone()

            nombre = cliente[1]

            if nombre != self.nombre:
                error.append("El nombre asociado al RUT en la base de datos no coincide")

        # Si nos llega un codigo de origen que ya existe en la DB tiene que tener la misma descripcion
        if cursor.execute("SELECT * FROM codigos WHERE codigo = %s", self.codigo_origen):
            codigo = cursor.fetchone()

            descripcion = codigo[1]

            if descripcion != self.descripcion_origen:
                error.append("La descripcion asociada al codigo de origen en la base de datos no coincide")

        # Si nos llega un codigo de producto que ya existe en la DB tiene que tener la misma info que ya se ingreso
        if cursor.execute("SELECT * FROM productos WHERE codigo_producto = %s", self.codigo_producto):
            producto = cursor.fetchone()

            tipo_contrato = str(producto[1])
            
            # Dejamos la fecha en formato YYYYMMDD
            fecha_sernac = producto[2].strftime("%Y%m%d")

            if tipo_contrato != self.tipo_contrato:
                error.append("El tipo de contrato asociado al codigo de producto en la base de datos no coincide")
            if fecha_sernac != self.fecha_sernac:
                error.append("La fecha sernac asociada al codigo de producto en la base de datos no coincide")

        # Si nos llega un numero de tarjeta que ya existe en la DB tiene que tener la misma info que ya se ingreso
        if cursor.execute("SELECT * FROM tarjetas WHERE numero_tarjeta = %s", self.n_tarjeta):
            tarjeta = cursor.fetchone()

            fecha_creacion = tarjeta[1].strftime("%Y%m%d")
            fecha_vencimiento = tarjeta[2].strftime("%Y%m%d")

            cupo_nacional = str(tarjeta[3])
            cupo_internacional = str(tarjeta[4])

            rut = tarjeta[5]

            if fecha_creacion != self.fecha_creacion:
                error.append("La fecha de creacion de la tarjeta existente en la base de datos no coincide")
            if fecha_vencimiento != self.fecha_vencimiento:
                error.append("La fecha de creacion de la tarjeta existente en la base de datos no coincide")
            if cupo_nacional != self.cupo_nacional:
                error.append("El cupo nacional asociado a la tarjeta en la base de datos no coincide")
            if cupo_internacional != self.cupo_internacional:
                error.append("El cupo internacional asociado a la tarjeta en la base de datos no coincide")
            if rut != self.rut:
                error.append("El RUT asociado a la tarjeta en la base de datos no coincide")

        # Si nos llega un numero de cuenta que ya existe en la DB debe tener los mismos datos
        if cursor.execute("SELECT * FROM cuentas WHERE numero_cuenta = %s", self.n_cuenta):
            cuenta = cursor.fetchone()

            linea_sobregiro = str(cuenta[1])
            
            fecha_creacion = cuenta[2].strftime("%Y%m%d")
            rut = cuenta[3]

            if fecha_creacion != self.fecha_creacion:
                error.append("La fecha de creacion de la cuenta existente en la base de datos no coincide")
            if linea_sobregiro != self.linea_sobregiro:
                error.append("La informacion sobre la linea de sobregiro de la cuenta en la base de datos no coincide")
            if rut != self.rut:
                error.append("El RUT asociado a la cuenta en la base de datos no coincide")

        isDuplicated = True if len(error) else False

        return {"isDuplicated": isDuplicated, "errors": error}

    def __repr__(self):
        string = "<Resultado"

        for attrName in self.descriptor:
            string += " %s='%s'" % (attrName, getattr(self, attrName))

        string += ">"
        return string
