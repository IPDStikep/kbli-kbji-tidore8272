import streamlit as st
import pandas as pd
import re

# Pengaturan halaman
st.set_page_config(page_title="Konsultasi KBLI & KBJI Tidore", page_icon="🔮", layout="wide")

st.title("🔮 Konsultasi Pintar KBLI & KBJI Kota Tidore Kepulauan")
st.write("Tuliskan cerita, rencana usaha, atau pengalaman kerja Anda di bawah ini. Sistem akan otomatis mencari kode yang cocok!")

# Fungsi Load Data dengan proteksi error data berantakan
@st.cache_data
def load_data():
    df_kbli = pd.read_csv("data_kbli.csv", on_bad_lines='skip')
    df_ji = pd.read_csv("data_kbji.csv", on_bad_lines='skip')
    return df_kbli, df_ji

try:
    kbli_df, kbji_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat database: {e}")
    st.stop()

# --- BAGIAN INPUT CERITA ---
st.subheader("✍️ Ceritakan Rencana Usaha atau Pekerjaan Anda")
cerita_user = st.text_area(
    "Contoh: 'Saya ingin membuka warung kopi modern yang juga menjual kue, lalu saya mau merekrut seorang barista dan kasir untuk membantu saya.'",
    height=150
)

# Fungsi untuk membersihkan teks dan mengambil kata-kata penting (minimal 3 huruf)
def ambil_kata_kunci(teks):
    teks = teks.lower()
    # Menghapus tanda baca
    teks = re.sub(r'[^\w\s]', ' ', teks)
    kata_list = teks.split()
    # Filter kata-kata umum (stopwards) yang tidak berguna untuk pencarian KBLI/KBJI
    kata_dibuang = {
        'saya', 'ingin', 'membuka', 'yang', 'juga', 'menjual', 'lalu', 'mau', 'merekrut', 
        'seorang', 'dan', 'untuk', 'membantu', 'bisa', 'akan', 'dengan', 'atau', 'di', 'ke'
    }
    kata_kunci = [kata for kata in kata_list if kata not in kata_dibuang and len(kata) > 2]
    return list(set(kata_kunci)) # menghilangkan kata yang duplikat

# --- PROSES DETEKSI OTOMATIS ---
if cerita_user:
    kata_kunci_user = ambil_kata_kunci(cerita_user)
    
    if kata_kunci_user:
        st.info(f"🔎 **Kata kunci yang terdeteksi dari cerita Anda:** {', '.join(kata_kunci_user)}")
        
        # Membuat layout 2 kolom untuk hasil
        kolom1, kolom2 = st.columns(2)
        
        # 1. SCAN KBLI
        with kolom1:
            st.markdown("### 🏢 Rekomendasi KBLI (Usaha)")
            # Mencari baris di CSV yang mengandung salah satu dari kata kunci
            kondisi_kbli = kbli_df.astype(str).apply(lambda x: x.str.contains('|'.join(kata_kunci_user), case=False, na=False)).any(axis=1)
            hasil_kbli = kbli_df[kondisi_kbli]
            
            if not hasil_kbli.empty:
                st.success(f"Ditemukan {len(hasil_kbli)} KBLI yang relevan:")
                st.dataframe(hasil_kbli, use_container_width=True)
            else:
                st.warning("Tidak ditemukan kode KBLI yang cocok dengan kata kunci cerita Anda.")
                
        # 2. SCAN KBJI
        with kolom2:
            st.markdown("### 💼 Rekomendasi KBJI (Jabatan/Pekerjaan)")
            # Mencari baris di CSV yang mengandung salah satu dari kata kunci
            kondisi_kbji = kbji_df.astype(str).apply(lambda x: x.str.contains('|'.join(kata_kunci_user), case=False, na=False)).any(axis=1)
            hasil_kbji = kbji_df[kondisi_kbji]
            
            if not hasil_kbji.empty:
                st.success(f"Ditemukan {len(hasil_kbji)} KBJI yang relevan:")
                st.dataframe(hasil_kbji, use_container_width=True)
            else:
                st.warning("Tidak ditemukan kode KBJI yang cocok dengan kata kunci cerita Anda.")
    else:
        st.warning("Cerita terlalu pendek atau belum mengandung kata kunci yang spesifik.")
