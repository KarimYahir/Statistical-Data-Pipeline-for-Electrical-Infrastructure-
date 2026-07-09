"""
Author: Karim Yahir Vallejo Flores

Description}:

This module automatically generates the SQL statements required to create
the database schema used throughout the project.

Using the metadata catalog, the script creates one hourly table for each
monitored electrical measurement point. Every table stores the following
energy variables:

- Active Energy (kWh)
- Reactive Energy (kvarh)
- Apparent Energy (kVAh)

Each record is indexed by a timestamp ("dh"), allowing hourly electrical
measurements to be stored and queried efficiently.

The script also provides an example of how to establish a connection to a
MariaDB/MySQL database and execute the generated SQL statements.

Note
---
The original database credentials and institutional infrastructure have
been removed for confidentiality purposes. Placeholder values are used
instead.
"""

from datetime import datetime
import datetime
import time
import MySQLdb

import lista_SubsDer

"""
The following function generates the SQL CREATE TABLE statements for all monitored
electrical measurement points.

Returns
----
list
List containing one CREATE TABLE query per monitored location.
"""
def Querys_CREATE_TABLES_EnHor():
###############################################################################
    campos_EnHor = ['kWh','kvarh','kVAh']
    
    infoSubs = lista_SubsDer.nombres()

    listaQuerys = [[]]
    for x in range(len(infoSubs)):

        tabla = infoSubs[x][0]
        if tabla[-1] != '*':
            query = "CREATE TABLE " + tabla +"_EnHor (dh DATETIME NULL DEFAULT '0000-00-00 00:00:00',"
            query += " kWh FLOAT(9,3), kvarh FLOAT(9,3), kVAh FLOAT(9,3))"
            
            if x == 0: listaQuerys[0] = query
            else: listaQuerys.append(query)

    return listaQuerys


"""
The following function connects to a MariaDB/MySQL database and executes the SQL statements
required to create the project tables.

Parameters
-----
BD_host : str
    Database host.
BD_user : str
    Database username.
BD_passwd : str
    Database password.
BaseDatos : str
    Database name.
listaQuerys : list
    List of SQL CREATE TABLE statements.
"""

###############################################################################
def CREATE_TABLES_BD(BD_host, BD_user, BD_passwd, BaseDatos, listaQuerys): 
###############################################################################

    for q in range(len(listaQuerys)):
        try:
            db = MySQLdb.connect(host=BD_host, user=BD_user, passwd=BD_passwd, port= "Your port", db="Name of you database here")
            curs =db.cursor()
            curs.execute(listaQuerys[q])
            db.commit()
            #print(listaQuerys[q])
            print("Se creo la tabla: " + listaQuerys[q][13:25])        
        except MySQLdb.Error as ex:print(f"Hubo un error: {ex}")
        finally:db.close()





###############################################################################
def LLENA_TABLA_EnDia():
###############################################################################
    for x in range(len(listaQuerys)):
        cad_campos += "," + campos[x]
        cad_datos += "," + str("{0:.3f}".format(datos[x]))
  
    query_1 = "INSERT INTO " + tabla + " (dia" + cad_campos + ") VALUES ('" + fecha +"'"+ cad_datos + ")"
    #print(query_1)
    
    try:
        db = MySQLdb.connect(user=BD_user,password=BD_passwd,host=BD_host, port= "Your port", db="Name of you database here")
        curs =db.cursor()
        #query = "DESCRIBE " + tabla
        curs.execute(query_1)
        db.commit()
        #dbdata = curs.fetchall()
        print("Se guardaron bien los valores en la base de datos")        
    except MySQLdb.Error as ex:print(f"Hubo un error: {ex}")
    finally:db.close()



###############################################################################
BD_host = "Your host"
BD_user = "Your user"
BD_passwd = "Your password"
BD_ ="Name of you database here"

listaQuerys = Querys_CREATE_TABLES_EnHor()
#print(listaQuerys)
CREATE_TABLES_BD(BD_host, BD_user, BD_passwd, BD_, listaQuerys)

