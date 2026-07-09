"""
plot_outlier_methods_example.py

Descripción:
Este script grafica la distribución de cada corriente eléctrica y muestra
los límites calculados por tres métodos de detección de outliers:

1. IQR
2. MAD
3. Percentiles

Sirve para comparar visualmente qué método se ajusta mejor al comportamiento
estadístico de los datos.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import median_abs_deviation


# Leer los datos
# Ruta original eliminada por confidencialidad.
datos = pd.read_csv("examples/sample_measurements.csv")

datos_select = datos.iloc[:17280].dropna().drop_duplicates()
datos_select["t"] = pd.to_datetime(datos_select["t"])

columnas_corriente = [col for col in datos_select.columns if col.startswith("I")]


for column in columnas_corriente:

    print(f"\n=== Analizando la corriente: {column} ===")

    corriente = datos_select[column].dropna()

    # -------------------------------------------------------------------------
    # Cálculo de límites por IQR
    # -------------------------------------------------------------------------
    q1 = corriente.quantile(0.25)
    q3 = corriente.quantile(0.75)
    iqr = q3 - q1

    iqr_lower = q1 - 1.5 * iqr
    iqr_upper = q3 + 1.5 * iqr

    # -------------------------------------------------------------------------
    # Cálculo de límites por MAD
    # -------------------------------------------------------------------------
    mad = median_abs_deviation(corriente)

    mad_lower = corriente.median() - 1.5 * mad
    mad_upper = corriente.median() + 1.5 * mad

    # -------------------------------------------------------------------------
    # Cálculo de límites por percentiles
    # -------------------------------------------------------------------------
    percentile_5 = corriente.quantile(0.001)
    percentile_95 = corriente.quantile(0.999)

    # -------------------------------------------------------------------------
    # Detección de outliers
    # -------------------------------------------------------------------------
    outliers_iqr = (corriente < iqr_lower) | (corriente > iqr_upper)
    outliers_mad = (corriente < mad_lower) | (corriente > mad_upper)
    outliers_percentile = (corriente < percentile_5) | (corriente > percentile_95)

    total = len(corriente)

    dentro_iqr = 100 * (~outliers_iqr).sum() / total
    dentro_mad = 100 * (~outliers_mad).sum() / total
    dentro_percentil = 100 * (~outliers_percentile).sum() / total

    print("\n--- Porcentaje de datos dentro de cada método ---")
    print(f"IQR: {dentro_iqr:.1f}%")
    print(f"MAD: {dentro_mad:.1f}%")
    print(f"Percentil 0.1%-99.9%: {dentro_percentil:.1f}%")

    # -------------------------------------------------------------------------
    # Gráfico comparativo
    # -------------------------------------------------------------------------
    plt.figure(figsize=(12, 6))

    sns.histplot(
        corriente,
        bins=30,
        kde=True,
        color="skyblue",
        stat="density"
    )

    plt.axvline(iqr_lower, color="orange", linestyle="--", label="IQR lower")
    plt.axvline(iqr_upper, color="orange", linestyle="--", label="IQR upper")

    plt.axvline(mad_lower, color="green", linestyle="--", label="MAD lower")
    plt.axvline(mad_upper, color="green", linestyle="--", label="MAD upper")

    plt.axvline(percentile_5, color="red", linestyle="--", label="Percentile lower")
    plt.axvline(percentile_95, color="red", linestyle="--", label="Percentile upper")

    plt.legend()
    plt.title(f"Distribución de la corriente: {column}")
    plt.xlabel("Corriente")
    plt.ylabel("Densidad")

    # -------------------------------------------------------------------------
    # Eje superior con percentiles acumulados
    # -------------------------------------------------------------------------
    ax = plt.gca()

    percentiles = np.linspace(0, 1, 11)
    valores_percentiles = np.quantile(corriente, percentiles)

    secax = ax.secondary_xaxis("top")
    secax.set_xticks(valores_percentiles)
    secax.set_xticklabels([f"{int(p * 100)}%" for p in percentiles])
    secax.set_xlabel("Percentil acumulado")

    # -------------------------------------------------------------------------
    # Caja de texto con resumen de porcentajes
    # -------------------------------------------------------------------------
    textstr = "\n".join((
        f"IQR: {dentro_iqr:.1f}%",
        f"MAD: {dentro_mad:.1f}%",
        f"Percentil: {dentro_percentil:.1f}%"
    ))

    props = dict(boxstyle="round", facecolor="white", alpha=0.8)

    plt.text(
        0.99,
        0.95,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=props
    )

    plt.tight_layout()
    plt.show()