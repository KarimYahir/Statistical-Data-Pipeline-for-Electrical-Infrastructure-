"""
Author: Karim Yahir Vallejo Flores

Description
-----------
Example script showing the preprocessing stage used in the project.

This module receives the raw lines read from a remote CSV file and converts
them into a structured Pandas DataFrame. It also builds a complete time axis
for a full day of measurements and fills missing timestamps with NaN values.

The main objective of this preprocessing step is to preserve the temporal
structure of the electrical measurements before applying statistical analysis.

The workflow is:

1. Read raw CSV lines.
2. Convert each line into a list of values.
3. Build a matrix from the CSV content.
4. Convert the matrix into a Pandas DataFrame.
5. Create a complete timestamp sequence for the selected day.
6. Align the available measurements with the complete time axis.
7. Fill missing records with NaN.

Note
----
This script is an anonymized example based on the original preprocessing
workflow. No institutional data are included.
"""

import datetime
import numpy as np
import pandas as pd


# =============================================================================
# 1. Create matrix from raw CSV lines
# =============================================================================
def CREA_MATRIZ_DATOS(lineas):
    """
    Creates a matrix from the raw lines read from a CSV file.

    The function manually separates each line using commas and stores the
    resulting values inside a nested list. The first line is treated as the
    header and the remaining lines are treated as data records.

    Parameters
    ----------
    lineas : list
        List of raw text lines read from a CSV file.

    Returns
    -------
    matriz : list
        Nested list containing the CSV header and data values.
    """

    n_filas = len(lineas)

    # Matrix that will store the header and all data rows.
    matriz = [[]]

    for l in range(n_filas):
        linea = lineas[l]

        # Positions of commas in the current line.
        pos_c = [0]

        # Values extracted from the current line.
        varis = [0]

        # Counter of commas found in the current line.
        coms = 0

        for c in range(len(linea)):

            # If a comma is found, extract the value before it.
            if linea[c] == ",":
                if coms == 0:
                    pos_c[0] = c
                    vari = linea[0:c]
                    varis[0] = vari
                else:
                    pos_c.append(c)
                    c_o = pos_c[coms - 1] + 1
                    vari = linea[c_o:c]
                    varis.append(vari)

                coms += 1

            # If the end of the line is reached, extract the last value.
            elif linea[c] == "\r" or linea[c] == "\n":
                if coms == 0:
                    vari = linea[0:c]
                    varis[0] = vari
                else:
                    c_o = pos_c[coms - 1] + 1
                    vari = linea[c_o:c]
                    varis.append(vari)
                break

        # First row corresponds to the header.
        if l == 0:
            matriz[l][:] = varis[:]
        else:
            matriz.extend([varis[:]])

    return matriz


# =============================================================================
# 2. Create DataFrame and complete time axis
# =============================================================================
def CREA_DATA_FRAME(M, fecha, ts):
    """
    Creates a Pandas DataFrame from a matrix and aligns it with a complete
    daily time axis.

    The function receives a matrix created from CSV lines, converts it into
    a DataFrame and then builds a complete timestamp sequence from 00:00:00
    to 23:59:59 for the selected date.

    If a timestamp exists in the original CSV, the corresponding measurement
    values are added to the final DataFrame. If a timestamp is missing, the
    function inserts NaN values to preserve the temporal structure.

    Parameters
    ----------
    M : list
        Matrix containing the CSV header and data records.
    fecha : str
        Date of the measurement in the format 'YYYY-MM-DD'.
    ts : int
        Sampling time in seconds.

        Example:
        ts = 5 means one measurement every 5 seconds.

    Returns
    -------
    df_csv : pandas.DataFrame
        DataFrame aligned with the complete daily timestamp sequence.
    t_full : list
        Complete list of expected timestamps for the selected day.
    """

    # Convert matrix into DataFrame.
    # First row contains column names; remaining rows contain data.
    df = pd.DataFrame(M[1:], columns=M[0])

    # Number of rows and columns in the original CSV DataFrame.
    f_csv = df.shape[0]
    c_csv = df.shape[1]

    # Initial datetime of the selected day.
    dt_o = datetime.datetime.strptime(
        fecha + " 00:00:00",
        "%Y-%m-%d %H:%M:%S"
    )

    # Complete timestamp sequence for a full day.
    # Example: if ts = 5, this creates 17,280 timestamps.
    t_full = [
        dt_o + datetime.timedelta(seconds=i)
        for i in range(0, 86400, ts)
    ]

    # This list will store the final aligned data.
    lineas_full = [[]]

    nlin_df = len(df)

    # Index used to move through the original CSV records.
    l = 0

    for t in range(len(t_full)):

        # Start each row with the expected timestamp.
        linea = [t_full[t]]

        # Timestamp from the original CSV.
        t_csv = datetime.datetime.strptime(
            fecha + " " + str(df.iloc[l, 0]),
            "%Y-%m-%d %H:%M:%S"
        )

        # ---------------------------------------------------------------------
        # Case 1: first timestamp
        # ---------------------------------------------------------------------
        if t == 0:
            if t_csv == t_full[t]:
                for c in range(1, c_csv):
                    if l <= nlin_df:
                        linea.extend([df.iloc[l, c]])
                    else:
                        linea.extend([np.NaN])
                l = l + 1

            elif t_csv > t_full[t]:
                for c in range(1, c_csv):
                    linea.extend([np.NaN])

            lineas_full[t][:] = linea[:]

        # ---------------------------------------------------------------------
        # Case 2: timestamp exists in original CSV
        # ---------------------------------------------------------------------
        elif t_csv == t_full[t]:
            for c in range(1, c_csv):
                linea.extend([df.iloc[l, c]])

            lineas_full.extend([linea[:]])
            l = l + 1

        # ---------------------------------------------------------------------
        # Case 3: timestamp is missing in original CSV
        # ---------------------------------------------------------------------
        elif t_csv > t_full[t]:
            for c in range(1, c_csv):
                linea.extend([np.NaN])

            lineas_full.extend([linea[:]])

        # ---------------------------------------------------------------------
        # Case 4: original CSV timestamp is behind expected timestamp
        # ---------------------------------------------------------------------
        elif t_csv < t_full[t]:
            while t_csv < t_full[t]:
                l = l + 1
                t_csv = datetime.datetime.strptime(
                    fecha + " " + str(df.iloc[l, 0]),
                    "%Y-%m-%d %H:%M:%S"
                )

            for c in range(1, c_csv):
                linea.extend([df.iloc[l, c]])

            lineas_full.extend([linea])
            l = l + 1

    # Dictionary indicating the position of each variable in the DataFrame.
    columnas = df.columns
    list_vars = {df.columns[0]: 0}

    for v in range(len(columnas)):
        list_vars.update({str(df.columns[v]): v})

    print("\nLas variables que se pueden graficar son:")
    print(df.columns)

    # Final DataFrame aligned with the complete time axis.
    df_csv = pd.DataFrame(lineas_full, columns=columnas)

    return df_csv, t_full