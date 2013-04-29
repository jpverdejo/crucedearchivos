from Loaders import Loader


class Reclamo:
    """Define la informacion pivote de un reclamo"""

    def __init__(self):
        #Se definen las variables necesarias como un string vacio
        self.codigo_origen = self.codigo_producto = self.numero_producto = self.codigo_reclamo = self.fecha = ''

        #Se carga el FDL
        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl('Origen_reclamo.fdl')

    #Metodo para cargar una linea
    def load_line(self, reclamo=""):
        #Se separa la linea usando el caracter "#". Se guarda en una lista
        reclamo = reclamo.split("#")

        #Se recorre la lista y se obtiene el numero de iteracion
        for i, v in enumerate(reclamo):
            #Buscamos el atributo que corresponde segun el FDL usando el numero de iteracion
            attrName = self.descriptor[i]

            #Seteamos el atributo que corresponde
            setattr(self, attrName, v)

        #Se devuelve el indice
        return self.codigo_reclamo

    def __repr__(self):
        return "<Reclamo codigo_origen='%s', codigo_producto='%s', numero_producto='%s', codigo_reclamo='%s', fecha='%s'>" % (self.codigo_origen, self.codigo_producto, self.numero_producto, self.codigo_reclamo, self.fecha)
