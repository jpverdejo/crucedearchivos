#Cruce de archivos
######Estructura de archivos - USACH 

###Premisas:
 - Existen los archivos de datos:
 	- /Data/Codigos_genericos.txt
 	- /Data/Cuentas_CtaCte.txt
 	- /Data/Cuentas_Ctas_Vistas.txt
 	- /Data/Origen_reclamo.txt
 	- /Data/Sernac.txt
 	- /Data/Tarjetas.txt

 - Existen los FDL:
 	- /FDL/Codigos_genericos.fdl
 	- /FDL/Cuentas_CtaCte.fdl
 	- /FDL/Cuentas_Ctas_Vistas.fdl
 	- /FDL/Origen_reclamo.fdl
 	- /FDL/resultado.fdl
 	- /FDL/Sernac.fdl
 	- /FDL/Tarjetas.fdl

 - El software tiene permisos de escritura en el directorio /Results

 - El FDL tiene formato: ```nombre_variable_1#nombre_variable_2#nombre_variable_3```

 - El archivo de datos tiene formato: ```valor_1#valor_2#valor_3```

###Ejecución:
 - Para la ejecución el comando es:
 	```python Cruce.py```
 - Los resultados se guardan en los archivos ```/Results/<nombre_del_banco>.txt```
   - Si el cruce no tiene informacion del banco se guarda en ```/Results/otros.txt```
