class Loader(object):
    #Metodo que carga el FDL
    def load_fdl(self, fdl_file):
        #Se abre el FDL indicado
        f = open("./FDL/" + fdl_file)

        #Se lee la linea
        descriptor = f.readline()

        #Se devuelve una lista separando la linea con el caracter "#"
        return descriptor.split("#")
