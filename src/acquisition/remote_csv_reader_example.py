"""
Author: Karim Yahir Vallejo Flores

Description
Example script showing how remote CSV files were accessed from an SFTP
server during the project.

The original workflow connected to an institutional remote storage system,
located CSV files according to substation, transformer, device type and
date, and then read the contents of the selected file for later processing
in Python.

This script keeps the original logic of the project while replacing all
real credentials, hosts and institutional paths with placeholder values.

Note
The original SFTP credentials, hostnames, ports and institutional routes
were removed for confidentiality reasons.
"""

import paramiko
import lista_SubsDer


# =============================================================================
# 1. SFTP configuration
# =============================================================================
# Replace these values with your own credentials if you want to adapt this
# example to another SFTP server.
host = "YOUR_SFTP_HOST"
port = "YOUR_SFTP_PORT"
usuario = "YOUR_SFTP_USER"
contrasena = "YOUR_SFTP_PASSWORD"
sftp_main = "YOUR_REMOTE_MAIN_DIRECTORY"


# =============================================================================
# 2. Connect to SFTP server
# =============================================================================
def CONECTA_SFTP(host, usuario, contrasena, carpeta_sftp):
    """
    Connects to the SFTP server where the CSV measurement files are stored.

    Parameters
    ----------
    host : str
        SFTP server hostname.
    usuario : str
        SFTP username.
    contrasena : str
        SFTP password.
    carpeta_sftp : str
        Main remote directory where the measurement files are stored.

    Returns
    -------
    sftp : paramiko.SFTPClient or int
        Active SFTP client if the connection is successful.
        Returns 0 if the connection fails.
    ssh_client : paramiko.SSHClient or int
        Active SSH client if the connection is successful.
        Returns 0 if the connection fails.
    """

    # Dictionary containing the connection parameters.
    datos = dict(
        hostname=host,
        port=port,
        username=usuario,
        password=contrasena
    )

    # Create SSH client.
    ssh_client = paramiko.SSHClient()

    # Automatically add unknown host keys.
    # This was useful during development, but in production environments
    # a stricter host-key policy is recommended.
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Establish SSH connection.
        ssh_client.connect(**datos)

        # Open SFTP session.
        sftp = ssh_client.open_sftp()

        print("\nConectado con servidor SFTP: %s" % host)

    except:
        print("No se pudo conectar. Intentar de nuevo en unos segundos...")
        sftp = 0
        ssh_client = 0

    return sftp, ssh_client


# =============================================================================
# 3. Read remote CSV file from SCADA/NAS structure
# =============================================================================
def LEE_CSV_SCADA(device, nombre_BD, fecha):
    """
    Reads a remote CSV file from the SFTP server.

    The function builds the remote path using the device type, the database
    identifier of the monitored point and the date of the measurement.

    Parameters
    ----------
    device : int
        Type of measurement device.

        Device convention used in the original workflow:
        0 -> MED-T
        1 -> T2_L
        2 -> C-T2_T
        3 -> C-T2_E
        4 -> PARM-T
        5 -> Custom route

    nombre_BD : str or list
        Database identifier of the monitored point.

        If device < 5, this value is searched inside the metadata catalog.
        If device == 5, this value should contain a custom route and filename.

    fecha : str
        Date of the file to be read, using the format 'YYYY-MM-DD'.

    Returns
    -------
    lineas : list
        Lines read from the remote CSV file.
    """

    # -------------------------------------------------------------------------
    # 3.1 Select device folder name
    # -------------------------------------------------------------------------
    if device == 0:
        dev = "MED"
    elif device == 1:
        dev = "T2_L"
    elif device == 2:
        dev = "C-T2_T"
    elif device == 3:
        dev = "C-T2_E"
    elif device == 4:
        dev = "PARM-T"

    # -------------------------------------------------------------------------
    # 3.2 Extract date components
    # -------------------------------------------------------------------------
    ano = fecha[0:4]
    mes = fecha[5:7]
    dia = fecha[8:10]

    # -------------------------------------------------------------------------
    # 3.3 Build remote path using metadata catalog
    # -------------------------------------------------------------------------
    global subes, trafo, capac, entidad

    if device < 5:
        # Load metadata catalog.
        infoSubs = lista_SubsDer.nombres()

        # Match the database identifier with its physical metadata.
        for x in range(len(infoSubs)):
            if nombre_BD == infoSubs[x][0]:
                subes = infoSubs[x][1]
                trafo = infoSubs[x][2]
                capac = infoSubs[x][3]
                entidad = infoSubs[x][-1]

        # Main SFTP directory.
        # Original institutional path was removed.
        raiz_SFTP = "YOUR_REMOTE_MAIN_DIRECTORY/"

        # Build the folder path:
        # main_directory / substation / device-transformer /
        ruta_SFTP = raiz_SFTP + subes + "/" + dev + "-" + trafo + "/"

        # Build CSV filename using the original naming convention:
        # substation_device-transformer_YYYYMMDD.csv
        CSV = subes + "_" + dev + "-" + trafo + "_" + ano + mes + dia + ".csv"

    else:
        # Custom route option.
        # This allows manually specifying the remote folder and file name.
        ruta_SFTP = nombre_BD[0]
        CSV = nombre_BD[1]

    # -------------------------------------------------------------------------
    # 3.4 Connect to SFTP server
    # -------------------------------------------------------------------------
    sftp, ssh_client = CONECTA_SFTP(host, usuario, contrasena, sftp_main)

    # -------------------------------------------------------------------------
    # 3.5 Read remote CSV file
    # -------------------------------------------------------------------------
    if sftp != 0 and ssh_client != 0:
        try:
            # Move to the desired remote folder.
            sftp.chdir(ruta_SFTP)

            try:
                # Full remote CSV path.
                CSV_remoto = ruta_SFTP + CSV

                print("Leyendo: %s ......" % CSV_remoto)

                # Open remote CSV file in read mode.
                datos_CSV = sftp.file(CSV_remoto, mode="r")

                # Read all lines from the file.
                lineas = datos_CSV.readlines()

                print("%s leído correctamente." % CSV_remoto)

                # Close file.
                datos_CSV.close()

            except:
                print("Fallo al leer %s" % CSV_remoto)
                lineas = []

        except:
            print("No existe la ruta deseada.")
            lineas = []

        # Close connections.
        sftp.close()
        ssh_client.close()

    else:
        print("Falló la conexión SFTP con el servidor.")
        lineas = []

    return lineas