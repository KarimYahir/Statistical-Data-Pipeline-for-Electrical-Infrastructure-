"""
Descripción:
Este script compara tres métodos para detectar outliers en corrientes
eléctricas: IQR, MAD y percentiles.

El objetivo es analizar qué porcentaje de datos queda dentro de los límites
definidos por cada método para cada corriente eléctrica.
"""

import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation


# Leer los datos
# Ruta original eliminada por confidencialidad.
datos = pd.read_csv("examples/sample_measurements.csv")

# Seleccionamos un día completo de mediciones:
# 17280 datos = 24 horas * 720 muestras por hora
datos_select = datos.iloc[:17280].dropna().drop_duplicates()

# Convertimos la columna de tiempo a formato datetime
datos_select["t"] = pd.to_datetime(datos_select["t"])

# Seleccionamos automáticamente las columnas de corriente
columnas_corriente = [col for col in datos_select.columns if col.startswith("I")]


for column in columnas_corriente:

    print(f"\n=== Analizando la corriente: {column} ===")

    # Tomamos la corriente actual y eliminamos posibles valores NaN
    corriente = datos_select[column].dropna()

    # -------------------------------------------------------------------------
    # Método 1: IQR
    # -------------------------------------------------------------------------
    # El rango intercuartílico usa Q1 y Q3 para definir límites.
    q1 = corriente.quantile(0.25)
    q3 = corriente.quantile(0.75)
    iqr = q3 - q1

    iqr_lower = q1 - 1.5 * iqr
    iqr_upper = q3 + 1.5 * iqr

    # -------------------------------------------------------------------------
    # Método 2: MAD
    # -------------------------------------------------------------------------
    # MAD mide desviaciones absolutas respecto a la mediana.
    mad = median_abs_deviation(corriente)

    mad_lower = corriente.median() - 1.5 * mad
    mad_upper = corriente.median() + 1.5 * mad

    # -------------------------------------------------------------------------
    # Método 3: Percentiles
    # -------------------------------------------------------------------------
    # Se usan percentiles extremos porque los datos reales no necesariamente
    # siguen una distribución normal.
    percentile_5 = corriente.quantile(0.001)
    percentile_95 = corriente.quantile(0.999)

    # -------------------------------------------------------------------------
    # Detección de outliers por cada método
    # -------------------------------------------------------------------------
    outliers_iqr = (corriente < iqr_lower) | (corriente > iqr_upper)
    outliers_mad = (corriente < mad_lower) | (corriente > mad_upper)
    outliers_percentile = (corriente < percentile_5) | (corriente > percentile_95)

    total = len(corriente)

    # Porcentaje de datos que quedan dentro de los límites de cada método
    dentro_iqr = 100 * (~outliers_iqr).sum() / total
    dentro_mad = 100 * (~outliers_mad).sum() / total
    dentro_percentil = 100 * (~outliers_percentile).sum() / total

    print("\n--- Porcentaje de datos dentro de cada método ---")
    print(f"IQR: {dentro_iqr:.1f}%")
    print(f"MAD: {dentro_mad:.1f}%")
    print(f"Percentil 0.1%-99.9%: {dentro_percentil:.1f}%")