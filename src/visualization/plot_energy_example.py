"""
Author: Karim Yahir Vallejo Flores

Description

Example script used to query hourly electrical energy data from a SQL
database and visualize active, reactive and apparent energy over a selected
date range.

The function retrieves:

- kWh  : active energy
- kvarh: reactive energy
- kVAh : apparent energy

It also separates reactive energy into inductive and capacitive behavior
using the sign of kvarh.

Note

Real database credentials and institutional table names were removed for
confidentiality reasons.
"""

import datetime
import numpy as np
import matplotlib.pyplot as plt
import MySQLdb

import lista_SubsDer


# --------------------------------------------------------------------------
def PlotEnergys1(fecha_o, fecha_f, tabla, BD_host, BD_user, BD_passwd, BD_port, BD_):
# --------------------------------------------------------------------------
    """
    Queries hourly energy data from a SQL table and generates an energy plot.

    Parameters
    ----------
    fecha_o : str
        Initial date in the format 'YYYY-MM-DD'.

    fecha_f : str
        Final date in the format 'YYYY-MM-DD'.

    tabla : str
        Name of the SQL table containing hourly energy data.

    BD_host : str
        Database host.

    BD_user : str
        Database username.

    BD_passwd : str
        Database password.

    BD_port : int
        Database port.

    BD_ : str
        Database name.

    Returns
    -------
    dbdata : tuple
        Records retrieved from the SQL query.

    X : list
        Complete hourly datetime axis.

    Y1 : list
        Active energy values (kWh).

    Y2 : list
        Positive reactive energy values.

    Y3 : list
        Reactive energy values.

    Y4 : list
        Apparent energy values (kVAh).
    """

    # ----------------------------------------------------------------------
    # 1. Search metadata associated with the selected table
    # ----------------------------------------------------------------------
    infoSubs = lista_SubsDer.nombres()

    Sub = ""
    KVATr = ""
    nombre = ""

    for n in range(len(infoSubs)):
        if infoSubs[n][0] == tabla[:-6]:
            Sub = infoSubs[n][1]
            KVATr = infoSubs[n][3]
            nombre = infoSubs[n][-1]
            print(nombre)
            break

    # ----------------------------------------------------------------------
    # 2. Define initial and final datetime strings
    # ----------------------------------------------------------------------
    dho = fecha_o + " 00:00:00"
    dhf = fecha_f + " 23:00:00"

    ano_o = fecha_o[0:4]
    mes_o = fecha_o[5:7]
    dia_o = fecha_o[8:10]

    ano_f = fecha_f[0:4]
    mes_f = fecha_f[5:7]
    dia_f = fecha_f[8:10]

    # ----------------------------------------------------------------------
    # 3. Create complete hourly datetime axis
    # ----------------------------------------------------------------------
    DHo = datetime.datetime.strptime(
        fecha_o + " 00:00:00",
        "%Y-%m-%d %H:%M:%S"
    )

    DHf = datetime.datetime.strptime(
        fecha_f + " 23:00:00",
        "%Y-%m-%d %H:%M:%S"
    )

    dias_t = int((DHf - DHo).days)

    # Complete hourly axis for the selected date range.
    DH_full = [
        DHo + datetime.timedelta(hours=i)
        for i in range(24 * int(dias_t + 1))
    ]

    # ----------------------------------------------------------------------
    # 4. SQL queries
    # ----------------------------------------------------------------------
    query_0 = "SELECT * FROM " + tabla + " WHERE TIMESTAMP(dh)>='" + dho + "'"
    query_0 += " AND TIMESTAMP(dh)<='" + dhf + "' ORDER BY dh ASC"

    query_1 = "SELECT SUM(kWh) FROM " + tabla
    query_1 += " WHERE TIMESTAMP(dh)>='" + dho + "' AND TIMESTAMP(dh)<='" + dhf + "'"

    query_2 = "SELECT SUM(kvarh) FROM " + tabla
    query_2 += " WHERE TIMESTAMP(dh)>='" + dho + "' AND TIMESTAMP(dh)<='" + dhf + "' AND kvarh>=0"

    query_3 = "SELECT SUM(kvarh) FROM " + tabla
    query_3 += " WHERE TIMESTAMP(dh)>='" + dho + "' AND TIMESTAMP(dh)<='" + dhf + "' AND kvarh<0"

    query_4 = "SELECT SUM(kVAh) FROM " + tabla
    query_4 += " WHERE TIMESTAMP(dh)>='" + dho + "' AND TIMESTAMP(dh)<='" + dhf + "'"

    # ----------------------------------------------------------------------
    # 5. Connect to SQL database and execute queries
    # ----------------------------------------------------------------------
    db = None

    try:
        db = MySQLdb.connect(
            user=BD_user,
            password=BD_passwd,
            host=BD_host,
            port=BD_port,
            database=BD_
        )

        curs = db.cursor()

        print(query_0)
        curs.execute(query_0)
        dbdata = curs.fetchall()

        print(query_1)
        curs.execute(query_1)
        kWh = curs.fetchall()
        kWh = kWh[0][0]

        print(query_2)
        curs.execute(query_2)
        kvarh_i = curs.fetchall()
        kvarh_i = kvarh_i[0][0]

        print(query_3)
        curs.execute(query_3)
        kvarh_c = curs.fetchall()
        kvarh_c = kvarh_c[0][0]

        print(query_4)
        curs.execute(query_4)
        kVAh = curs.fetchall()
        kVAh = kVAh[0][0]

    except MySQLdb.Error as ex:
        print(f"Hubo un error: {ex}")
        return None, [], [], [], [], []

    finally:
        if db is not None:
            db.close()

    # ----------------------------------------------------------------------
    # 6. Align SQL data with complete hourly axis
    # ----------------------------------------------------------------------
    X = [0]
    Y1 = [0]  # kWh
    Y2 = [0]  # positive kvarh
    Y3 = [0]  # kvarh
    Y4 = [0]  # kVAh

    j = 0

    for i in range(len(DH_full)):

        if j < len(dbdata):

            if DH_full[i] == dbdata[j][0]:

                if i == 0:
                    X[0] = DH_full[i]
                    Y1[0] = dbdata[j][1]
                    Y4[0] = dbdata[j][3]

                    if dbdata[j][2] >= 0:
                        Y2[0] = dbdata[j][2]
                        Y3[0] = dbdata[j][2]
                    else:
                        Y2[0] = np.NaN
                        Y3[0] = dbdata[j][2]

                else:
                    X.append(DH_full[i])
                    Y1.append(dbdata[j][1])
                    Y4.append(dbdata[j][3])

                    if dbdata[j][2] >= 0:
                        Y2.append(dbdata[j][2])
                        Y3.append(dbdata[j][2])
                    else:
                        Y2.append(np.NaN)
                        Y3.append(dbdata[j][2])

                j += 1

            else:
                if i == 0:
                    X[0] = DH_full[i]
                    Y1[0] = np.NaN
                    Y2[0] = np.NaN
                    Y3[0] = np.NaN
                    Y4[0] = np.NaN
                else:
                    X.append(DH_full[i])
                    Y1.append(np.NaN)
                    Y2.append(np.NaN)
                    Y3.append(np.NaN)
                    Y4.append(np.NaN)

        else:
            X.append(DH_full[i])
            Y1.append(np.NaN)
            Y2.append(np.NaN)
            Y3.append(np.NaN)
            Y4.append(np.NaN)

    # ----------------------------------------------------------------------
    # 7. Compute power factor approximation
    # ----------------------------------------------------------------------
    if kvarh_i:
        FP = np.cos(np.arctan(float(kvarh_i) / float(kWh)))
        print("Fp = " + str(FP))
    else:
        FP = np.cos(np.arctan(float(kvarh_c) / float(kWh))) * (-1)
        print("Fp = " + str(FP))

    # ----------------------------------------------------------------------
    # 8. Add visual indicators for days and missing data
    # ----------------------------------------------------------------------
    for h in range(len(X)):

        # Vertical lines at the start of each day.
        if X[h].hour == 0:
            if X[h].isoweekday() == 1:
                plt.axvline(x=X[h], color="y", linestyle="-", linewidth=2)
            else:
                plt.axvline(x=X[h], color="y", linestyle="--", linewidth=0.7)

        # Highlight missing data intervals.
        if np.isnan(Y1[h]):
            if (h + 1) < len(X):
                plt.axvspan(X[h], X[h + 1], facecolor="m", alpha=0.3)

    # ----------------------------------------------------------------------
    # 9. Plot energy variables
    # ----------------------------------------------------------------------
    plt.plot(X, Y4, "b", drawstyle="steps-post", label="kVAh = " + str(kVAh))
    plt.plot(X, Y1, "c", drawstyle="steps-post", label="kWh = " + str(kWh))
    plt.plot(X, Y3, "pink", drawstyle="steps-post", label="kvarh_c = " + str(kvarh_c))
    plt.plot(X, Y2, "r", drawstyle="steps-post", label="kvarh_i = " + str(kvarh_i))

    plt.fill_between(X, Y1, Y4, color="b", step="post", alpha=0.4)
    plt.fill_between(X, Y1, color="c", step="post", alpha=0.4)
    plt.fill_between(X, Y3, color="pink", step="post", alpha=0.4)
    plt.fill_between(X, Y2, color="r", step="post", alpha=0.4)

    plt.xlabel("Tiempo")
    plt.xticks(rotation=45)
    plt.ylabel("[kWh - kvarh - kVAh]")

    if min(Y3) >= 0:
        lim = max(Y4) * (-0.03)
        plt.ylim(bottom=lim)

    plt.legend(bbox_to_anchor=(1, 1.11), ncol=2)

    plt.title(
        tabla[0:-6] + ". "
        + Sub + ". "
        + nombre + ". Tr: "
        + str(KVATr) + "KVA. "
        + dia_o + "/" + mes_o + "/" + ano_o
        + " - "
        + dia_f + "/" + mes_f + "/" + ano_f,
        loc="left"
    )

    plt.grid(True)
    plt.show()

    return dbdata, X, Y1, Y2, Y3