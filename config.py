"""Definisi variabel, himpunan fuzzy, dan basis aturan.

Studi kasus: rekomendasi durasi penyiraman tanaman
  Input  : kelembaban tanah (%) dan suhu udara (derajat C)
  Output : durasi penyiraman (menit)
"""
from membership import trapmf, trimf

# ---------------- Variabel input ----------------
KELEMBABAN = {
    "range": (0, 100),
    "satuan": "%",
    "himpunan": {
        "Kering": lambda x: trapmf(x, 0, 0, 30, 50),
        "Lembab": lambda x: trimf(x, 30, 50, 70),
        "Basah":  lambda x: trapmf(x, 50, 70, 100, 100),
    },
}

SUHU = {
    "range": (15, 45),
    "satuan": "°C",
    "himpunan": {
        "Dingin": lambda x: trapmf(x, 15, 15, 22, 28),
        "Normal": lambda x: trimf(x, 22, 30, 38),
        "Panas":  lambda x: trapmf(x, 32, 38, 45, 45),
    },
}

# ---------------- Variabel output (Mamdani) ----------------
DURASI = {
    "range": (0, 30),
    "satuan": "menit",
    "himpunan": {
        "Singkat": lambda x: trapmf(x, 0, 0, 5, 12),
        "Sedang":  lambda x: trimf(x, 8, 15, 22),
        "Lama":    lambda x: trapmf(x, 18, 25, 30, 30),
    },
}

# ---------------- Output Sugeno orde-nol (konstanta) ----------------
KONSTANTA_SUGENO = {"Singkat": 5.0, "Sedang": 15.0, "Lama": 25.0}

# ---------------- Basis aturan: (kelembaban, suhu) -> durasi ----------------
ATURAN = [
    ("Kering", "Dingin", "Sedang"),
    ("Kering", "Normal", "Lama"),
    ("Kering", "Panas",  "Lama"),
    ("Lembab", "Dingin", "Singkat"),
    ("Lembab", "Normal", "Sedang"),
    ("Lembab", "Panas",  "Sedang"),
    ("Basah",  "Dingin", "Singkat"),
    ("Basah",  "Normal", "Singkat"),
    ("Basah",  "Panas",  "Singkat"),
]
