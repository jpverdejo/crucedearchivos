from Resultados import Resultado
import MySQLdb
import datetime
import sys


class Inyector:
    def __init__(self):

        DB_host = "127.0.0.1"
        DB_user = "root"
        DB_pass = ""
        DB_name = "EdA"

        args = sys.argv

        if len(args) < 2:
            print "Tienes que ingresar un archivo de entrada, por ejemplo: python %s entrada.txt" % (args[0])
            return

        # Leemos el nombre de archivo desde los argumentos
        filename = args[1]

        # Creamos variables globales necesarias para la ejecucion
        self.reclamos = {}

        self.cargados = []
        self.duplicados = []
        self.erroneos = []
        self.fallaCarga = []

        self.errors = {}

        try:
            # Tratamos de cargar el archivo
            self.load_file(
                filename,
                Resultado,
                "reclamos")
        except IOError as e:
            print "El archivo de entrada (%s) no existe" % (filename)
            return

        self.con = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_pass, db=DB_name)

        self.cursor = self.con.cursor()

        self.validate()

        self.findDuplicated()

        self.loadDB()

        now = datetime.datetime.now()
        sufix_files = now.strftime("_%Y-%m-%d_%H-%M-%S")

        filename_erroneos = "erroneos%s.txt" % sufix_files
        filename_duplicados = "duplicados%s.txt" % sufix_files
        filename_fallaCarga = "fallaCarga%s.txt" % sufix_files
        filename_cargados = "cargados%s.txt" % sufix_files

        # Creamos el archivo de resultado con los registros erroneos y sus errores
        for reclamo in self.erroneos:
            #Se abre el archivo de resultado en modo de escritura con un puntero al final
            f = open("./Results/" + filename_erroneos, "a")
            for error in self.errors[reclamo.codigo_reclamo]:
                #Se escribe el error
                f.write("--- %s ---\n" % error)

            #Se cierra el archivo
            f.close()

            reclamo.save_resultado(filename_erroneos)

            #Agregamos salto de linea por visibilidad
            f = open("./Results/" + filename_erroneos, "a")
            f.write("\n")
            f.close()

        # Creamos el archivo de resultado con los registros duplicados y sus errores
        for reclamo in self.duplicados:
            f = open("./Results/" + filename_duplicados, "a")
            for error in self.errors[reclamo.codigo_reclamo]:
                f.write("--- %s ---\n" % error)

            f.close()

            reclamo.save_resultado(filename_duplicados)

            f = open("./Results/" + filename_duplicados, "a")
            f.write("\n")
            f.close()

        # Creamos el archivo de resultado con los registros en los que fallo en la carga
        for reclamo in self.fallaCarga:
            reclamo.save_resultado(filename_fallaCarga)

        # Creamos el archivo de resultado con los registros cargados correctamente
        for reclamo in self.cargados:
            reclamo.save_resultado(filename_cargados)

        num_cargados = len(self.cargados)
        num_erroneos = len(self.erroneos)
        num_duplicados = len(self.duplicados)
        num_fallaCarga = len(self.fallaCarga)

        total = num_cargados + num_erroneos + num_duplicados + num_fallaCarga

        # Evitando division por 0 :)
        if total:
            porc_cargados = "(" + str(round(100 * (num_cargados + 0.0) / total, 2)) + "%)"
            porc_erroneos = "(" + str(round(100 * (num_erroneos + 0.0) / total, 2)) + "%)"
            porc_duplicados = "(" + str(round(100 * (num_duplicados + 0.0) / total, 2)) + "%)"
            porc_fallaCarga = "(" + str(round(100 * (num_fallaCarga + 0.0) / total, 2)) + "%)"
        else:
            porc_cargados = porc_erroneos = porc_duplicados = porc_fallaCarga = ""

        print "==================================================="
        print "================== Estadisticas ==================="
        print "==================================================="
        print
        print "Total de registros de entrada: %s" % total
        print
        print "==================================================="
        print
        print "Registros cargados correctamente: %s %s" % (num_cargados, porc_cargados)
        print "Archivo de respaldo: %s" % filename_cargados
        print
        print "Registros erroneos: %s %s" % (num_erroneos, porc_erroneos)
        print "Archivo de respaldo: %s" % filename_erroneos
        print
        print "Registros duplicados: %s %s" % (num_duplicados, porc_duplicados)
        print "Archivo de respaldo: %s" % filename_duplicados
        print
        print "Registros con fallas al cargar DB: %s %s" % (num_fallaCarga, porc_fallaCarga)
        print "Archivo de respaldo: %s" % filename_fallaCarga
        print
        print "==================================================="

    #Carga un archivo linea a linea, es agnostico a la clase que se va a ocupar
    def load_file(self, file, className, dictionary):
        f = open(file)
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

    def validate(self):
        #Iteramos sobre todos los reclamos
        for i, reclamo in self.reclamos.items():
            validate = reclamo.validate()
            if not validate['isValid']:
                self.erroneos.append(reclamo)
                self.errors[reclamo.codigo_reclamo] = validate['errors']
                del self.reclamos[reclamo.codigo_reclamo]

    def findDuplicated(self):
        #Iteramos sobre todos los reclamos
        for i, reclamo in self.reclamos.items():
            duplicated = reclamo.isDuplicated(self.cursor)
            if duplicated['isDuplicated']:
                self.duplicados.append(reclamo)
                self.errors[reclamo.codigo_reclamo] = duplicated['errors']
                del self.reclamos[reclamo.codigo_reclamo]

    def loadDB(self):
        #Iteramos sobre todos los reclamos
        for i, reclamo in self.reclamos.items():
            try:
                # Solo por comodidad
                cursor = self.cursor

                # Tanto la DB InnoDB como la biblioteca MySQL soportan transacciones, por lo que haremos uso de ellas
                # Como revisamos que si los primary keys que existen en la db tengan la misma informacion asociada solo agreregamos los registros necesarios
                if not cursor.execute("SELECT * FROM clientes WHERE rut = %s", reclamo.rut):
                    cursor.execute("INSERT INTO clientes (rut, nombre) VALUES (%s, %s)", (reclamo.rut, reclamo.nombre))

                if not cursor.execute("SELECT * FROM codigos WHERE codigo = %s", reclamo.codigo_origen):
                    cursor.execute("INSERT INTO codigos (codigo, descripcion) VALUES (%s, %s)", (reclamo.codigo_origen, reclamo.descripcion_origen))

                if not cursor.execute("SELECT * FROM productos WHERE codigo_producto = %s", reclamo.codigo_producto):
                    cursor.execute("INSERT INTO productos (codigo_producto, tipo_contrato, fecha) VALUES (%s, %s, %s)", (reclamo.codigo_producto, reclamo.tipo_contrato, reclamo.formatDate(reclamo.fecha_sernac)))

                if reclamo.n_cuenta:
                    if not cursor.execute("SELECT * FROM cuentas WHERE numero_cuenta = %s", reclamo.n_cuenta):
                        cursor.execute("INSERT INTO cuentas (numero_cuenta, linea_sobregiro, fecha_creacion, rut) VALUES (%s, %s, %s, %s)", (reclamo.n_cuenta, reclamo.linea_sobregiro, reclamo.formatDate(reclamo.fecha_creacion), reclamo.rut))

                if reclamo.n_tarjeta:
                    if not cursor.execute("SELECT * FROM tarjetas WHERE numero_tarjeta = %s", reclamo.n_tarjeta):
                        cursor.execute("INSERT INTO tarjetas (numero_tarjeta, fecha_creacion, fecha_vencimiento, cupo_nacional, cupo_internacional, rut) VALUES (%s, %s, %s, %s, %s, %s)", (reclamo.n_tarjeta, reclamo.formatDate(reclamo.fecha_creacion), reclamo.formatDate(reclamo.fecha_vencimiento),  reclamo.cupo_nacional, reclamo.cupo_internacional, reclamo.rut))

                # Este registro, por supuesto, siempre debe ser ingresado
                cursor.execute("INSERT INTO reclamos (codigo_reclamo, codigo_origen, codigo_producto, numero_producto, fecha) VALUES (%s, %s, %s, %s, %s)", (reclamo.codigo_reclamo, reclamo.codigo_origen, reclamo.codigo_producto, reclamo.codigo_producto, reclamo.formatDate(reclamo.fecha_reclamo)))

                # Si no se ha lanzado la excepcion commiteamos los cambios :)
                self.con.commit()

                # Y lo agregamos al listado de cargas correctas :)
                self.cargados.append(reclamo)

            except MySQLdb.Error, e:
                # Si salto la excepcion hacemos rollback de los cambios y agregamos el reclamo a la lista de fallidos
                if self.con:
                    self.con.rollback()

                self.fallaCarga.append(reclamo)


# Iniciamos el inyector
Inyector()
