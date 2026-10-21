"""Mesin inferensi fuzzy: Mamdani dan Sugeno orde-nol."""
import numpy as np
from config import (KELEMBABAN, SUHU, DURASI, KONSTANTA_SUGENO, ATURAN)


def fuzzifikasi(kelembaban, suhu):
    """Hitung derajat keanggotaan input pada tiap himpunan fuzzy."""
    mu_k = {n: float(f(kelembaban)) for n, f in KELEMBABAN["himpunan"].items()}
    mu_s = {n: float(f(suhu)) for n, f in SUHU["himpunan"].items()}
    return mu_k, mu_s


def kekuatan_aturan(mu_k, mu_s):
    """Firing strength tiap aturan (operator AND = min)."""
    return [(k, s, out, min(mu_k[k], mu_s[s])) for k, s, out in ATURAN]


def mamdani(kelembaban, suhu, resolusi=1001, detail=False):
    """Mamdani: implikasi MIN, agregasi MAX, defuzzifikasi centroid."""
    mu_k, mu_s = fuzzifikasi(kelembaban, suhu)
    aturan = kekuatan_aturan(mu_k, mu_s)

    lo, hi = DURASI["range"]
    x = np.linspace(lo, hi, resolusi)
    agregat = np.zeros_like(x)
    for _, _, out, alpha in aturan:
        potongan = np.minimum(alpha, DURASI["himpunan"][out](x))
        agregat = np.maximum(agregat, potongan)

    luas = agregat.sum()
    hasil = float((x * agregat).sum() / luas) if luas > 0 else 0.0
    if detail:
        return hasil, {"mu_k": mu_k, "mu_s": mu_s, "aturan": aturan,
                       "x": x, "agregat": agregat}
    return hasil


def sugeno(kelembaban, suhu, detail=False):
    """Sugeno orde-nol: rata-rata terbobot  z = sum(a_i * z_i) / sum(a_i)."""
    mu_k, mu_s = fuzzifikasi(kelembaban, suhu)
    aturan = kekuatan_aturan(mu_k, mu_s)

    pembilang = sum(a * KONSTANTA_SUGENO[out] for _, _, out, a in aturan)
    penyebut = sum(a for _, _, _, a in aturan)
    hasil = pembilang / penyebut if penyebut > 0 else 0.0
    if detail:
        return hasil, {"mu_k": mu_k, "mu_s": mu_s, "aturan": aturan}
    return hasil


def status(durasi):
    """Ubah durasi (menit) menjadi status rekomendasi."""
    if durasi < 3:
        return "Tidak perlu disiram"
    if durasi < 10:
        return "Siram singkat"
    if durasi < 20:
        return "Siram sedang"
    return "Siram lama"
