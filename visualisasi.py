"""Grafik fungsi keanggotaan, hasil agregasi, dan permukaan kontrol."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import KELEMBABAN, SUHU, DURASI
from fuzzy_engine import mamdani, sugeno

OUT_DIR = "output"


def _simpan(nama):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, nama)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_membership():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (judul, var) in zip(axes, [("Kelembaban Tanah", KELEMBABAN),
                                       ("Suhu Udara", SUHU),
                                       ("Durasi Penyiraman", DURASI)]):
        lo, hi = var["range"]
        x = np.linspace(lo, hi, 500)
        for nama, f in var["himpunan"].items():
            ax.plot(x, f(x), label=nama, linewidth=2)
        ax.set_title(judul)
        ax.set_xlabel(var["satuan"])
        ax.set_ylabel("Derajat keanggotaan")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(alpha=0.3)
        ax.legend()
    return _simpan("fungsi_keanggotaan.png")


def plot_mamdani(kelembaban, suhu):
    hasil, d = mamdani(kelembaban, suhu, detail=True)
    x = d["x"]
    fig, ax = plt.subplots(figsize=(8, 4))
    for nama, f in DURASI["himpunan"].items():
        ax.plot(x, f(x), "--", alpha=0.5, label=nama)
    ax.fill_between(x, d["agregat"], alpha=0.4, color="tab:green", label="Agregasi")
    ax.axvline(hasil, color="red", label=f"Centroid = {hasil:.2f} menit")
    ax.set_title(f"Mamdani: kelembaban {kelembaban}%, suhu {suhu}°C")
    ax.set_xlabel("Durasi (menit)")
    ax.legend()
    ax.grid(alpha=0.3)
    return _simpan("agregasi_mamdani.png")


def plot_permukaan(n=25):
    k = np.linspace(*KELEMBABAN["range"], n)
    s = np.linspace(*SUHU["range"], n)
    K, S = np.meshgrid(k, s)
    zm = np.array([[mamdani(a, b, resolusi=301) for a in k] for b in s])
    zs = np.array([[sugeno(a, b) for a in k] for b in s])

    fig = plt.figure(figsize=(13, 5))
    for i, (z, judul) in enumerate([(zm, "Mamdani"), (zs, "Sugeno")], 1):
        ax = fig.add_subplot(1, 2, i, projection="3d")
        ax.plot_surface(K, S, z, cmap="viridis")
        ax.set_title(f"Permukaan kontrol {judul}")
        ax.set_xlabel("Kelembaban (%)")
        ax.set_ylabel("Suhu (°C)")
        ax.set_zlabel("Durasi (menit)")
    return _simpan("permukaan_kontrol.png")
