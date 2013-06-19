import CuentasCorrientes
import CuentasVistas
import Tarjetas
import Reclamos
import Productos
import Codigos
import Resultados
import os


class Cruce:
    def __init__(self):
        #Se cargan los archivos

        #Cuentas Corrientes
        self.CtasCtes = {}
        self.load_file(
            "Cuentas_CtaCte.txt",
            CuentasCorrientes.CuentaCorriente,
            "CtasCtes")

        #Cuentas Vistas
        self.CtasVistas = {}
        self.load_file(
            "Cuentas_Ctas_Vistas.txt",
            CuentasVistas.CuentaVista,
            "CtasVistas")

        #Tarjetas
        self.Tarjetas = {}
        self.load_file(
            "Tarjetas.txt",
            Tarjetas.Tarjeta,
            "Tarjetas")

        #Reclamos
        self.Reclamos = {}
        self.load_file(
            "Origen_reclamo.txt",
            Reclamos.Reclamo,
            "Reclamos")

        #Productos
        self.Productos = {}
        self.load_file(
            "Sernac.txt",
            Productos.Producto,
            "Productos")

        #Codigos
        self.Codigos = {}
        self.load_file(
            "Codigos_genericos.txt",
            Codigos.Codigo,
            "Codigos")

        #Una vez cargados todos los archivos empezamos el proceso de cruce
        self.cruce()

        print "=== Cruce terminado correctamente ==="

    #Carga un archivo linea a linea, es agnostico a la clase que se va a ocupar
    def load_file(self, file, className, dictionary):
        #Todos los archivos de data van en el directorio "Data"
        f = open("./Data/" + file)
        for line in f:
            #Removemos los "\n" que recibe cuando lee la linea completa
            line = line.rstrip()

            #Se instancia la clase
            instance = className()

            #Le pasamos la linea leida al metodo load_cuenta,
            #La clase se preocupa del FDL y devuelve el indice
            instance_id = instance.load_line(line)

            #Se agrega el objeto creado al diccionario indicado en la llamada
            objVar = getattr(self, dictionary)
            objVar[instance_id] = instance
            setattr(self, dictionary, objVar)

    def deleteResults(self):
        #Seteamos el directorio a limpiar
        folder = './Results/'

        #Se obtienen todos los archivos de este directorio
        for the_file in os.listdir(folder):
            #Se crea el path completo del archivo (directorio + nombre de archivo)
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    #Si el archivo existe se elimina
                    os.unlink(file_path)
            except Exception, e:
                print e

    def cruce(self):
        #Se eliminan los resultados de cruces anteriores
        self.deleteResults()

        #Iteramos sobre todos los reclamos
        for i, reclamo in self.Reclamos.iteritems():
            #Definimos las variables que se guardaran en el archivo
            #Se setean como string vacio, que es el valor por omision que se escribira
            codigo_reclamo = ''
            fecha_reclamo = ''
            fecha_sernac = ''
            tipo_contrato = ''
            codigo_producto = ''
            codigo_origen = ''
            descripcion_origen = ''
            rut = ''
            nombre = ''
            fecha_creacion = ''
            n_cuenta = ''
            linea_sobregiro = ''
            n_tarjeta = ''
            fecha_vencimiento = ''
            cupo_nacional = ''
            cupo_internacional = ''

            #Se instancian clases vacias, en caso de que no se pueda hacer el cruce
            cuenta = CuentasCorrientes.CuentaCorriente()
            tarjeta = Tarjetas.Tarjeta()
            producto = Productos.Producto()
            codigo = Codigos.Codigo()

            #Si es tarjeta la informacion personal (nombre, rut) se obtienen de "tarjeta"
            #si no, de "cuenta", para eso se usa este flag
            is_cuenta = 0

            #Revisamos si el numero de producto esta dentro de las cuentas corrientas
            if reclamo.numero_producto in self.CtasCtes:
                cuenta = self.CtasCtes[reclamo.numero_producto]
                is_cuenta = 1

            #Revisamos si el numero de producto esta dentro de las cuentas vista
            if reclamo.numero_producto in self.CtasVistas:
                cuenta = self.CtasVistas[reclamo.numero_producto]
                is_cuenta = 1

            #Revisamos si el numero de producto esta dentro de las tarjetas de credito
            if reclamo.numero_producto in self.Tarjetas:
                tarjeta = self.Tarjetas[reclamo.numero_producto]

            #Se trata de cruzar el codigo de producto
            if reclamo.codigo_producto in self.Productos:
                producto = self.Productos[reclamo.codigo_producto]

            #Se trata de cruzar el codigo de origen
            if reclamo.codigo_origen in self.Codigos:
                codigo = self.Codigos[reclamo.codigo_origen]

            #Se setean las variables segun los cruces anteriores
            codigo_reclamo = reclamo.codigo_reclamo
            fecha_reclamo = reclamo.fecha
            fecha_sernac = producto.fecha_sernac
            tipo_contrato = producto.tipo_contrato
            codigo_producto = producto.codigo_producto
            codigo_origen = codigo.codigo
            descripcion_origen = codigo.descripcion

            n_cuenta = cuenta.n_cuenta
            linea_sobregiro = cuenta.linea_sobregiro

            n_tarjeta = tarjeta.n_tarjeta
            fecha_vencimiento = tarjeta.fecha_vencimiento
            cupo_nacional = tarjeta.cupo_nacional
            cupo_internacional = tarjeta.cupo_internacional

            #Si es cuenta obtenemos la informacion personal desde la variable "cuenta"
            #si no desde "tarjeta"
            if is_cuenta:
                nombre = cuenta.nombre
                rut = cuenta.rut
                fecha_creacion = cuenta.fecha_creacion
            else:
                nombre = tarjeta.nombre
                rut = tarjeta.rut
                fecha_creacion = tarjeta.fecha_creacion

            #Se instancia "Resultado" con los valores seteados anteriormente
            resultado = Resultados.Resultado(
                codigo_reclamo,
                fecha_reclamo,
                fecha_sernac,
                tipo_contrato,
                codigo_producto,
                codigo_origen,
                descripcion_origen,
                rut,
                nombre,
                fecha_creacion,
                n_cuenta,
                linea_sobregiro,
                n_tarjeta,
                fecha_vencimiento,
                cupo_nacional,
                cupo_internacional)

            #Si esta definida la variable resultado.descripcion origen significa que tenemos el
            #banco al que corresponde, por lo que se guarda en ese archivo
            #si no se guarda en otros.txt
            if resultado.descripcion_origen == '':
                result_file = 'otros.txt'
            else:
                result_file = resultado.descripcion_origen + ".txt"

            #Se guardan los resultados en el archivo correspondiente
            resultado.save_resultado(result_file)

#Iniciamos el proceso
Cruce()
