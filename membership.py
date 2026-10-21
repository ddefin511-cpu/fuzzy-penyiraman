"""Fungsi keanggotaan (membership function) fuzzy."""
import numpy as np


def trapmf(x, a, b, c, d):
    """Trapesium: naik a->b, datar b->c, turun c->d.
    Bahu kiri: a == b, bahu kanan: c == d."""
    x = np.asarray(x, dtype=float)
    kiri = (x - a) / (b - a) if b > a else (x >= a).astype(float)
    kanan = (d - x) / (d - c) if d > c else (x <= d).astype(float)
    return np.clip(np.minimum(kiri, kanan), 0.0, 1.0)


def trimf(x, a, b, c):
    """Segitiga dengan puncak di b."""
    return trapmf(x, a, b, b, c)
