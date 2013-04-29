from Loaders import Loader


class Codigo:
    """Define los codigos de instituciones"""

    def __init__(self):
        #Se definen las variables del objeto como string vacio
        self.codigo = self.descripcion = ''

        #Se carga el FDL
        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl("Codigos_genericos.fdl")

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

        #Devolvemos el indice
        return self.codigo

    def __repr__(self):
        return "<Codigo codigo:%s descripcion:%s>" % (self.codigo, self.descripcion)
