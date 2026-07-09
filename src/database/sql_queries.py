"""
Author: Karim Yahir Vallejo Flores

Description

Example script showing how Python was used to connect to a MariaDB/MySQL
database and execute SQL queries over hourly electrical energy tables.

This script illustrates basic database operations used during the project:

1. Connect to a SQL database.
2. Create a cursor object.
3. Retrieve timestamp records.
4. Filter records using a condition.
5. Read a limited number of records using LIMIT and OFFSET.

Note

Real credentials, database names and table names were replaced with
placeholder values for confidentiality reasons.
"""

import mysql.connector


# ------------------------------------------------------------------------------
# 1. Database connection
# ------------------------------------------------------------------------------
def ConexionBaseDeDatos():
    """
    Creates a connection to the SQL database.

    Returns

    conexion : mysql.connector.connection.MySQLConnection
        Connection object used to interact with the database.
    """

    try:
        conexion = mysql.connector.connect(
            user="YOUR_USER",
            password="YOUR_PASSWORD",
            host="YOUR_HOST",
            port="YOUR_PORT",
            database="YOUR_DATABASE"
        )

        print("Conexión correcta")
        return conexion

    except mysql.connector.Error as error:
        print("Error al conectarse a la base de datos {}".format(error))
        return None


# -----------------------------------------------------------------------------
# 2. Connect to database and create cursor
# -----------------------------------------------------------------------------
mydb = ConexionBaseDeDatos()

if mydb is not None:
    # The cursor object allows Python to execute SQL queries.
    mycursor = mydb.cursor()

    # -------------------------------------------------------------------------
    # 3. Example 1: Retrieve timestamp column
    # ------------------------------------------------------------------------
    # This query selects only the datetime column from an hourly energy table.
    #
    # Original project example:
    # SELECT dh FROM a1t1_enhor
    #
    # Public/anonymized example:
    mycursor.execute("SELECT dh FROM measured_point_EnHor")

    # fetchall() retrieves all records returned by the executed query.
    myresult = mycursor.fetchall()

    print("\nTimestamps retrieved from the table:")

    for row in myresult:
        print(row)
    else:
        print("Datos no disponibles")

    # --------------------------------------------------------------------------
    # 4. Example 2: Filter records using a condition
    # -------------------------------------------------------------------------
    # This query retrieves all records where active energy is greater than
    # a selected threshold.
    #
    # Original project example:
    # SELECT * FROM a1t1_enhor WHERE kWh > 60
    #
    # Public/anonymized example:
    sql = "SELECT * FROM measured_point_EnHor WHERE kWh > 60"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    print("\nRecords where kWh > 60:")

    for result in myresult:
        print(result)
    else:
        print("No hay datos para mostrar")

    # ------------------------------------------------------------------
    # 5. Example 3: Read records using LIMIT and OFFSET
    # ------------------------------------------------------------------
    # LIMIT controls how many records are returned.
    # OFFSET controls the starting position of the query.
    #
    # Original project example:
    # SELECT * FROM a1t1_enhor LIMIT 5 OFFSET 366
    #
    # Public/anonymized example:
    mycursor.execute("SELECT * FROM measured_point_EnHor LIMIT 5 OFFSET 366")

    myresult = mycursor.fetchall()

    print("\nRecords retrieved using LIMIT and OFFSET:")

    for result in myresult:
        print(result)
    else:
        print("No hay datos para mostrar")

    # --------------------------------------------------------------------------
    # 6. Close connection
    # --------------------------------------------------------------------------
    mycursor.close()
    mydb.close()
    print("\nConexión cerrada")