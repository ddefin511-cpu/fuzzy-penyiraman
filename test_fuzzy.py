"""Uji sederhana: python test_fuzzy.py"""
from fuzzy_engine import mamdani, sugeno, fuzzifikasi
from membership import trimf, trapmf


def test_membership():
    assert trimf(50, 30, 50, 70) == 1.0
    assert trimf(30, 30, 50, 70) == 0.0
    assert trapmf(0, 0, 0, 30, 50) == 1.0   # bahu kiri
    assert abs(float(trimf(40, 30, 50, 70)) - 0.5) < 1e-9


def test_fuzzifikasi_jumlah():
    mu_k, _ = fuzzifikasi(40, 30)
    assert abs(mu_k["Kering"] - 0.5) < 1e-9 and abs(mu_k["Lembab"] - 0.5) < 1e-9


def test_monoton():
    # makin kering -> makin lama disiram
    assert mamdani(10, 30) > mamdani(50, 30) > mamdani(90, 30)
    assert sugeno(10, 30) > sugeno(50, 30) > sugeno(90, 30)


def test_rentang():
    for k in range(0, 101, 10):
        for s in range(15, 46, 5):
            assert 0 <= mamdani(k, s) <= 30
            assert 0 <= sugeno(k, s) <= 30


if __name__ == "__main__":
    for nama, fn in list(globals().items()):
        if nama.startswith("test_"):
            fn()
            print("OK  ", nama)
