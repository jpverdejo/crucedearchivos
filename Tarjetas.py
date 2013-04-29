from Loaders import Loader


class Tarjeta:
    """Define las cuentas corrientes"""

    def __init__(self):
        #Se definen las variables necesarias como un string vacio
        self.n_tarjeta = self.fecha_creacion = self.fecha_vencimiento = self.cupo_nacional = self.cupo_internacional = self.rut = self.nombre = ''

        #Se carga el FDL
        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl('Tarjetas.fdl')

    #Metodo para cargar una linea
    def load_line(self, tarjeta=""):
        #Se separa la linea usando el caracter "#". Se guarda en una lista
        tarjeta = tarjeta.split("#")

        #Se recorre la lista y se obtiene el numero de iteracion
        for i, v in enumerate(tarjeta):
            #Buscamos el atributo que corresponde segun el FDL usando el numero de iteracion
            attrName = self.descriptor[i]

            #Seteamos el atributo que corresponde
            setattr(self, attrName, v)

        #Se devuelve el indice
        return self.n_tarjeta

    def __repr__(self):
        return "<Tarjeta n_tarjeta = '%s', fecha_creacion = '%s', fecha_vencimiento = '%s', cupo_nacional = '%s', cupo_internacional= '%s', rut = '%s', nombre = '%s'>" % (self.n_tarjeta, self.fecha_creacion, self.fecha_vencimiento, self.cupo_nacional, self.cupo_internacional, self.rut, self.nombre)
