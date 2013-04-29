from Loaders import Loader


class Producto:
    """Define la informacion del sernac acerca de un producto"""

    def __init__(self):
        #Se definen las variables necesarias como un string vacio
        self.fecha_sernac = self.tipo_contrato = self.codigo_producto = ''

        #Se carga el FDL
        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl('Sernac.fdl')

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
        return self.codigo_producto

    def __repr__(self):
        return "<Producto fecha_sernac='%s', tipo_contrato='%s', codigo_producto='%s'>" % (self.fecha_sernac, self.tipo_contrato, self.codigo_producto)
