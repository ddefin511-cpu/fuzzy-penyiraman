# Sistem Rekomendasi Penyiraman Tanaman — Fuzzy Logic (Mamdani & Sugeno)

Project Python tanpa library fuzzy eksternal (hanya NumPy + Matplotlib), sehingga setiap tahap
(fuzzifikasi, inferensi, agregasi, defuzzifikasi) bisa dijelaskan langsung dari kode.

## Studi kasus
| Variabel | Jenis | Rentang | Himpunan fuzzy |
|---|---|---|---|
| Kelembaban tanah | Input | 0–100 % | Kering, Lembab, Basah |
| Suhu udara | Input | 15–45 °C | Dingin, Normal, Panas |
| Durasi penyiraman | Output | 0–30 menit | Singkat, Sedang, Lama |

## Basis aturan (9 aturan)
| Kelembaban \ Suhu | Dingin | Normal | Panas |
|---|---|---|---|
| Kering | Sedang | Lama | Lama |
| Lembab | Singkat | Sedang | Sedang |
| Basah | Singkat | Singkat | Singkat |

## Metode
- **Mamdani**: AND = min, implikasi = min, agregasi = max, defuzzifikasi = centroid.
- **Sugeno orde-nol**: output konstanta (Singkat = 5, Sedang = 15, Lama = 25), z = Σ(αᵢ·zᵢ) / Σαᵢ.

## Struktur file
- `membership.py` — fungsi segitiga & trapesium
- `config.py` — variabel, himpunan fuzzy, aturan (ubah di sini untuk studi kasus lain)
- `fuzzy_engine.py` — fuzzifikasi, Mamdani, Sugeno
- `visualisasi.py` — grafik membership, agregasi, permukaan kontrol
- `main.py` — program utama (demo / CLI / interaktif)
- `test_fuzzy.py` — pengujian dasar

## Menjalankan
```
pip install -r requirements.txt
python main.py                 # demo kasus uji
python main.py -k 25 -s 34     # satu kasus + rincian aturan aktif
python main.py -i              # mode interaktif
python main.py --plot          # simpan grafik ke output/
python test_fuzzy.py           # jalankan pengujian
```
