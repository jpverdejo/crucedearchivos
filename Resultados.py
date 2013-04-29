from Loaders import Loader


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

    #Metodo que guarda un cruce
    def save_resultado(self):
        #Si esta definida la variable self.descripcion origen significa que tenemos el
        #banco al que corresponde, por lo que se guarda en ese archivo
        #si no se guarda en otros.txt
        if self.descripcion_origen == '':
            result_file = 'otros.txt'
        else:
            result_file = self.descripcion_origen + ".txt"

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
