import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kontrol Kualitas - X̄ Chart", layout="wide")
st.title("Kontrol Kualitas Berat Botol - X̄ Chart")

st.markdown("""
Sebuah pabrik memproduksi botol air mineral. Untuk mengontrol kualitas berat botol, dilakukan pengambilan sampel 5 botol tiap 4 jam.
Aplikasi ini menghitung rata-rata, rentang, serta batas kendali berdasarkan data berat botol yang Anda input.
""")

# Input jumlah sampel
num_samples = st.number_input("Jumlah sampel (kelompok):", min_value=1, max_value=50, value=6)

st.markdown("### Masukkan Berat Botol (gram) per Sampel (5 data per baris):")
data = []
valid_input = True
for i in range(num_samples):
    row = st.text_input(f"Sampel {i+1} (pisahkan dengan koma):", value="500, 502, 498, 497, 501", key=f"input_{i}")
    try:
        values = list(map(float, row.split(",")))
        if len(values) != 5:
            st.error(f"Sampel {i+1} harus terdiri dari 5 nilai.")
            valid_input = False
        else:
            data.append(values)
    except:
        st.error(f"Format salah pada sampel {i+1}.")
        valid_input = False

if valid_input and len(data) == num_samples:
    df = pd.DataFrame(data, columns=[f'Botol-{i+1}' for i in range(5)])
    df["Rata-rata"] = df.mean(axis=1)
    df["Rentang"] = df.max(axis=1) - df.min(axis=1)

    X_bar_bar = df["Rata-rata"].mean()
    R_bar = df["Rentang"].mean()
    A2 = 0.577  # untuk ukuran sampel n = 5

    UCL = X_bar_bar + A2 * R_bar
    LCL = X_bar_bar - A2 * R_bar

    st.markdown("### Hasil Perhitungan:")
    st.dataframe(df.style.format("{:.2f}"))

    st.markdown(f"""
    **X̄̄ (Rata-rata dari rata-rata):** {X_bar_bar:.2f}  
    **R̄ (Rata-rata rentang):** {R_bar:.2f}  
    **UCL (Batas atas):** {UCL:.2f}  
    **LCL (Batas bawah):** {LCL:.2f}
    """)

    # Visualisasi chart
    st.markdown("### Diagram Kontrol X̄:")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Rata-rata"], marker='o', linestyle='-', label="Rata-rata Sampel")
    ax.axhline(UCL, color='red', linestyle='--', label="UCL")
    ax.axhline(LCL, color='red', linestyle='--', label="LCL")
    ax.axhline(X_bar_bar, color='green', linestyle='-', label="X̄̄")
    ax.set_xlabel("Sampel ke-")
    ax.set_ylabel("Berat Rata-rata (gram)")
    ax.set_title("X̄ Chart Kontrol Kualitas Berat Botol")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Evaluasi kontrol statistik
    out_of_control = df[(df["Rata-rata"] > UCL) | (df["Rata-rata"] < LCL)]
    if not out_of_control.empty:
        st.warning("\U0001F6A8 Terdapat rata-rata sampel di luar batas kendali. Proses tidak dalam kendali statistik.")
    else:
        st.success("\u2705 Semua sampel berada dalam batas kendali. Proses dalam kendali statistik.")
