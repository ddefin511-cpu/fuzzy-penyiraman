"""Sistem Rekomendasi Penyiraman Tanaman — Fuzzy Logic Mamdani & Sugeno.

Cara pakai:
    python main.py                  # demo beberapa kasus uji
    python main.py -k 25 -s 34      # hitung satu kasus (kelembaban 25%, suhu 34 C)
    python main.py -i               # mode interaktif
    python main.py --plot           # simpan grafik ke folder output/
"""
import argparse
from fuzzy_engine import mamdani, sugeno, status

KASUS_UJI = [(15, 35), (25, 34), (45, 28), (50, 30), (60, 24), (80, 20), (90, 40)]


def cetak_detail(kel, suhu):
    dm, info = mamdani(kel, suhu, detail=True)
    ds = sugeno(kel, suhu)
    print(f"\nInput: kelembaban = {kel}%, suhu = {suhu}°C")
    print("Fuzzifikasi kelembaban:", {k: round(v, 3) for k, v in info["mu_k"].items()})
    print("Fuzzifikasi suhu      :", {k: round(v, 3) for k, v in info["mu_s"].items()})
    print("Aturan aktif (alpha > 0):")
    for k, s, out, a in info["aturan"]:
        if a > 0:
            print(f"  JIKA kelembaban {k} DAN suhu {s} MAKA durasi {out}  (alpha = {a:.3f})")
    print(f"Mamdani (centroid) : {dm:.2f} menit -> {status(dm)}")
    print(f"Sugeno (wtd. avg)  : {ds:.2f} menit -> {status(ds)}")


def demo():
    print(f"{'Kelembaban':>10} {'Suhu':>6} | {'Mamdani':>8} {'Sugeno':>8} | Rekomendasi (Mamdani)")
    print("-" * 66)
    for kel, suhu in KASUS_UJI:
        dm, ds = mamdani(kel, suhu), sugeno(kel, suhu)
        print(f"{kel:>9}% {suhu:>5}° | {dm:>8.2f} {ds:>8.2f} | {status(dm)}")
    cetak_detail(*KASUS_UJI[1])


def interaktif():
    print("Ketik 'q' untuk keluar.")
    while True:
        try:
            a = input("\nKelembaban tanah (0-100 %): ").strip()
            if a.lower() == "q":
                break
            b = input("Suhu udara (15-45 °C): ").strip()
            if b.lower() == "q":
                break
            cetak_detail(float(a), float(b))
        except ValueError:
            print("Masukkan angka yang valid.")
        except (EOFError, KeyboardInterrupt):
            break


def main():
    p = argparse.ArgumentParser(description="Fuzzy Mamdani & Sugeno - penyiraman tanaman")
    p.add_argument("-k", "--kelembaban", type=float)
    p.add_argument("-s", "--suhu", type=float)
    p.add_argument("-i", "--interaktif", action="store_true")
    p.add_argument("--plot", action="store_true", help="simpan grafik ke output/")
    args = p.parse_args()

    if args.plot:
        import visualisasi as v
        kel = args.kelembaban if args.kelembaban is not None else 25
        suhu = args.suhu if args.suhu is not None else 34
        for path in (v.plot_membership(), v.plot_mamdani(kel, suhu), v.plot_permukaan()):
            print("Tersimpan:", path)
    elif args.interaktif:
        interaktif()
    elif args.kelembaban is not None and args.suhu is not None:
        cetak_detail(args.kelembaban, args.suhu)
    else:
        demo()


if __name__ == "__main__":
    main()
