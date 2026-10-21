
import streamlit as st

st.set_page_config(
    page_title="Fuzzy Penyiraman Tanaman",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Dashboard Fuzzy Penyiraman Tanaman")
st.write("Sistem pendukung keputusan penyiraman tanaman")

st.subheader("Input Kondisi Tanaman")

kelembaban = st.slider(
    "Kelembapan tanah (%)",
    min_value=0,
    max_value=100,
    value=25
)

suhu = st.slider(
    "Suhu udara (°C)",
    min_value=0,
    max_value=50,
    value=34
)

if st.button("Proses Penyiraman"):
    st.write("### Data input")
    st.metric("Kelembapan tanah", f"{kelembaban}%")
    st.metric("Suhu udara", f"{suhu} °C")
    st.info(
        "Tampilan dashboard berhasil dijalankan. "
        "Berikutnya, mesin fuzzy Mamdani dan Sugeno "
        "perlu dihubungkan untuk menghitung keputusan sebenarnya."
    )
