"""

Descripción:
Este script construye histogramas para distintas variables eléctricas.

Los histogramas se usaron para estudiar la forma de la distribución de los
datos y comparar visualmente el comportamiento de voltajes, corrientes,
potencias, factor de potencia y distorsión armónica.

También se ajusta una curva normal como referencia visual.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity


# Leer los datos
# Ruta original eliminada por confidencialidad.
df = pd.read_csv("examples/sample_measurements.csv")


# =============================================================================
# Histogramas de voltajes: Van, Vbn, Vcn
# =============================================================================

df = df.dropna(subset=["Van", "Vbn", "Vcn"], axis="index")

fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Histograma de Van
ax1 = axs[0]
ax1 = df["Van"].hist(density=True, alpha=0.5, color="blue", edgecolor="black", ax=ax1)

mu_van, std_van = norm.fit(df["Van"])
xmin_van, xmax_van = ax1.get_xlim()
x_van = np.linspace(xmin_van, xmax_van, 100)
p_van = norm.pdf(x_van, mu_van, std_van)

ax1.plot(x_van, p_van, "k", linewidth=2)
ax1.set_xlabel("Van")
ax1.set_ylabel("Densidad de probabilidad")
ax1.set_title("Histograma Van")

# Histograma de Vbn
ax2 = axs[1]
ax2 = df["Vbn"].hist(density=True, alpha=0.5, color="orange", edgecolor="black", ax=ax2)

mu_vbn, std_vbn = norm.fit(df["Vbn"])
xmin_vbn, xmax_vbn = ax2.get_xlim()
x_vbn = np.linspace(xmin_vbn, xmax_vbn, 100)
p_vbn = norm.pdf(x_vbn, mu_vbn, std_vbn)

ax2.plot(x_vbn, p_vbn, "k", linewidth=2)
ax2.set_xlabel("Vbn")
ax2.set_ylabel("Densidad de probabilidad")
ax2.set_title("Histograma Vbn")

# Histograma de Vcn
ax3 = axs[2]
ax3 = df["Vcn"].hist(density=True, alpha=0.5, color="green", edgecolor="black", ax=ax3)

mu_vcn, std_vcn = norm.fit(df["Vcn"])
xmin_vcn, xmax_vcn = ax3.get_xlim()
x_vcn = np.linspace(xmin_vcn, xmax_vcn, 100)
p_vcn = norm.pdf(x_vcn, mu_vcn, std_vcn)

ax3.plot(x_vcn, p_vcn, "k", linewidth=2)
ax3.set_xlabel("Vcn")
ax3.set_ylabel("Densidad de probabilidad")
ax3.set_title("Histograma Vcn")

plt.tight_layout()
plt.show()


# =============================================================================
# Histogramas de corrientes: Ia, Ib, Ic, In
# =============================================================================

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Histograma de Ia
ax1 = axs[0, 0]
ax1 = df["Ia"].hist(density=True, alpha=0.5, color="blue", edgecolor="black", ax=ax1)

mu_ia, std_ia = norm.fit(df["Ia"])
xmin_ia, xmax_ia = ax1.get_xlim()
x_ia = np.linspace(xmin_ia, xmax_ia, 100)
p_ia = norm.pdf(x_ia, mu_ia, std_ia)

ax1.plot(x_ia, p_ia, "k", linewidth=2)
ax1.set_xlabel("Ia")
ax1.set_ylabel("Densidad de probabilidad")
ax1.set_title("Histograma Ia")

# Histograma de Ib
ax2 = axs[0, 1]
ax2 = df["Ib"].hist(density=True, alpha=0.5, color="orange", edgecolor="black", ax=ax2)

mu_ib, std_ib = norm.fit(df["Ib"])
xmin_ib, xmax_ib = ax2.get_xlim()
x_ib = np.linspace(xmin_ib, xmax_ib, 100)
p_ib = norm.pdf(x_ib, mu_ib, std_ib)

ax2.plot(x_ib, p_ib, "k", linewidth=2)
ax2.set_xlabel("Ib")
ax2.set_ylabel("Densidad de probabilidad")
ax2.set_title("Histograma Ib")

# Histograma de Ic
ax3 = axs[1, 0]
ax3 = df["Ic"].hist(density=True, alpha=0.5, color="green", edgecolor="black", ax=ax3)

mu_ic, std_ic = norm.fit(df["Ic"])
xmin_ic, xmax_ic = ax3.get_xlim()
x_ic = np.linspace(xmin_ic, xmax_ic, 100)
p_ic = norm.pdf(x_ic, mu_ic, std_ic)

ax3.plot(x_ic, p_ic, "k", linewidth=2)
ax3.set_xlabel("Ic")
ax3.set_ylabel("Densidad de probabilidad")
ax3.set_title("Histograma Ic")

# Histograma de In
ax4 = axs[1, 1]
ax4 = df["In"].hist(density=True, alpha=0.5, color="red", edgecolor="black", ax=ax4)

mu_in, std_in = norm.fit(df["In"])
xmin_in, xmax_in = ax4.get_xlim()
x_in = np.linspace(xmin_in, xmax_in, 100)
p_in = norm.pdf(x_in, mu_in, std_in)

ax4.plot(x_in, p_in, "k", linewidth=2)
ax4.set_xlabel("In")
ax4.set_ylabel("Densidad de probabilidad")
ax4.set_title("Histograma In")

plt.tight_layout()
plt.show()


# =============================================================================
# Histogramas de Qtot y Ptot
# =============================================================================

fig, axs = plt.subplots(1, 2, figsize=(18, 6))

# Histograma de Qtot
ax1 = axs[0]
ax1 = df["Qtot"].hist(density=True, alpha=0.5, color="blue", edgecolor="black", ax=ax1)

mu_qtot, std_qtot = norm.fit(df["Qtot"])
xmin_qtot, xmax_qtot = ax1.get_xlim()
x_qtot = np.linspace(xmin_qtot, xmax_qtot, 100)
p_qtot = norm.pdf(x_qtot, mu_qtot, std_qtot)

ax1.plot(x_qtot, p_qtot, "k", linewidth=2)
ax1.set_xlabel("Qtot")
ax1.set_ylabel("Densidad de probabilidad")
ax1.set_title("Histograma Qtot")

# Histograma de Ptot
ax2 = axs[1]
ax2 = df["Ptot"].hist(density=True, alpha=0.5, color="orange", edgecolor="black", ax=ax2)

mu_ptot, std_ptot = norm.fit(df["Ptot"])
xmin_ptot, xmax_ptot = ax2.get_xlim()
x_ptot = np.linspace(xmin_ptot, xmax_ptot, 100)
p_ptot = norm.pdf(x_ptot, mu_ptot, std_ptot)

ax2.plot(x_ptot, p_ptot, "k", linewidth=2)
ax2.set_xlabel("Ptot")
ax2.set_ylabel("Densidad de probabilidad")
ax2.set_title("Histograma Ptot")

plt.tight_layout()
plt.show()


# =============================================================================
# Histogramas de FPtot, THDIa, THDIb, THDIc
# =============================================================================

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Histograma de FPtot
ax1 = axs[0, 0]
ax1 = df["FPtot"].hist(density=True, alpha=0.5, color="blue", edgecolor="black", ax=ax1)

mu_fptot, std_fptot = norm.fit(df["FPtot"])
xmin_fptot, xmax_fptot = ax1.get_xlim()
x_fptot = np.linspace(xmin_fptot, xmax_fptot, 100)
p_fptot = norm.pdf(x_fptot, mu_fptot, std_fptot)

ax1.plot(x_fptot, p_fptot, "k", linewidth=2)
ax1.set_xlabel("FPtot")
ax1.set_ylabel("Densidad de probabilidad")
ax1.set_title("Histograma FPtot")

# Histograma de THDIa
ax2 = axs[0, 1]
ax2 = df["THDIa"].hist(density=True, alpha=0.5, color="orange", edgecolor="black", ax=ax2)

mu_thdia, std_thdia = norm.fit(df["THDIa"])
xmin_thdia, xmax_thdia = ax2.get_xlim()
x_thdia = np.linspace(xmin_thdia, xmax_thdia, 100)
p_thdia = norm.pdf(x_thdia, mu_thdia, std_thdia)

ax2.plot(x_thdia, p_thdia, "k", linewidth=2)
ax2.set_xlabel("THDIa")
ax2.set_ylabel("Densidad de probabilidad")
ax2.set_title("Histograma THDIa")

# Histograma de THDIb
ax3 = axs[1, 0]
ax3 = df["THDIb"].hist(density=True, alpha=0.5, color="green", edgecolor="black", ax=ax3)

mu_thdib, std_thdib = norm.fit(df["THDIb"])
xmin_thdib, xmax_thdib = ax3.get_xlim()
x_thdib = np.linspace(xmin_thdib, xmax_thdib, 100)
p_thdib = norm.pdf(x_thdib, mu_thdib, std_thdib)

ax3.plot(x_thdib, p_thdib, "k", linewidth=2)
ax3.set_xlabel("THDIb")
ax3.set_ylabel("Densidad de probabilidad")
ax3.set_title("Histograma THDIb")

# Histograma de THDIc
ax4 = axs[1, 1]
ax4 = df["THDIc"].hist(density=True, alpha=0.5, color="red", edgecolor="black", ax=ax4)

mu_thdic, std_thdic = norm.fit(df["THDIc"])
xmin_thdic, xmax_thdic = ax4.get_xlim()
x_thdic = np.linspace(xmin_thdic, xmax_thdic, 100)
p_thdic = norm.pdf(x_thdic, mu_thdic, std_thdic)

ax4.plot(x_thdic, p_thdic, "k", linewidth=2)
ax4.set_xlabel("THDIc")
ax4.set_ylabel("Densidad de probabilidad")
ax4.set_title("Histograma THDIc")

plt.tight_layout()
plt.show()