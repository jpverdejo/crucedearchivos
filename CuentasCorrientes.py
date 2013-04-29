from Loaders import Loader


class CuentaCorriente():
    """Define una cuenta corriente"""

    def __init__(self):
        #Se definen las variables necesarias como un string vacio
        self.n_cuenta = self.linea_sobregiro = self.fecha_creacion = self.rut = self.nombre = ''

        #Se carga el FDL
        self.load_fdl()

    #Metodo que carga el FDL
    def load_fdl(self):
        #Usamos el metodo definido en Loader y se guarda la info en self.descriptor
        loader = Loader()
        self.descriptor = loader.load_fdl('Cuentas_CtaCte.fdl')

    #Metodo para cargar una linea
    def load_line(self, cuenta=""):
        #Se separa la linea usando el caracter "#". Se guarda en una lista
        cuenta = cuenta.split("#")

        #Se recorre la lista y se obtiene el numero de iteracion
        for i, v in enumerate(cuenta):
            #Buscamos el atributo que corresponde segun el FDL usando el numero de iteracion
            attrName = self.descriptor[i]

            #Seteamos el atributo que corresponde
            setattr(self, attrName, v)

        #Se devuelve el indice
        return self.n_cuenta

    def __repr__(self):
        return "<CuentaCorriente n_cuenta='%s', linea_sobregiro='%s', fecha_creacion='%s', rut='%s', nombre='%s'>" % (self.n_cuenta, self.linea_sobregiro, self.fecha_creacion, self.rut, self.nombre)
