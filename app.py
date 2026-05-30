import streamlit as st
import pandas as pd

# Atur judul halaman di tab browser
st.set_page_config(page_title="Pencarian KBLI & KBJI Tidore", page_icon="🏢", layout="wide")

st.title("🏢 Sistem Pencarian KBLI (2025) & KBJI (2014) Tidore")
st.write("Aplikasi ini berjalan 100% lokal tanpa menggunakan API Key (Gratis & Unlimited).")

# Fungsi untuk membaca data dengan Fitur Cache agar aplikasi super cepat
@st.cache_data
def load_data():
    # Ditambahkan on_bad_lines='skip' agar baris yang kelebihan kolom otomatis dilewati
    df_kbli = pd.read_csv("data_kbli.csv", on_bad_lines='skip')
    df_ji = pd.read_csv("data_kbji.csv", on_bad_lines='skip')
    return df_kbli, df_ji
    
# Load data ke aplikasi
try:
    kbli_df, kbji_df = load_data()
except Exception as e:
    st.error(f"Gagal membaca file CSV. Pastikan nama file sesuai. Error: {e}")
    st.stop()

# Membuat Menu Tab di Streamlit
tab1, tab2 = st.tabs(["🔍 Cari KBLI (Usaha)", "💼 Cari KBJI (Jabatan/Pekerjaan)"])

# === TAB 1: PENCARIAN KBLI ===
with tab1:
    st.header("Pencarian Kode KBLI 2025")
    keyword_kbli = st.text_input("Masukkan kata kunci usaha (Contoh: kopi, warung, komputer):", key="kbli_input")
    
    if keyword_kbli:
        # Mencari kata kunci di semua kolom (mengabaikan huruf besar/kecil)
        # SESEUKAN 'nama_kbli' dengan nama kolom judul di CSV-mu
        hasil_kbli = kbli_df[kbli_df.astype(str).apply(lambda x: x.str.contains(keyword_kbli, case=False)).any(axis=1)]
        
        st.write(f"Ditemukan {len(hasil_kbli)} data yang cocok:")
        st.dataframe(hasil_kbli, use_container_width=True)

# === TAB 2: PENCARIAN KBJI ===
with tab2:
    st.header("Pencarian Kode KBJI 2014")
    keyword_kbji = st.text_input("Masukkan kata kunci jabatan (Contoh: manajer, programmer, guru):", key="kbji_input")
    
    if keyword_kbji:
        # Mencari kata kunci di semua kolom
        hasil_kbji = kbji_df[kbji_df.astype(str).apply(lambda x: x.str.contains(keyword_kbji, case=False)).any(axis=1)]
        
        st.write(f"Ditemukan {len(hasil_kbji)} data yang cocok:")
        st.dataframe(hasil_kbji, use_container_width=True)
