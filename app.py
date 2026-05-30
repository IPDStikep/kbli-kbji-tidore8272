import streamlit as st
import google.generativeai as genai
import os

# 1. Pengaturan Halaman Tab Browser
st.set_page_config(page_title="KBLI & KBJI", page_icon="🔮", layout="wide")

st.title("🔮 Konsultasi Pintar KBLI & KBJI (BPS Kota Tidore Kepulauan)")
# st.write("Deskripsi/Ceritakan Pekerjaan.")

# 2. Paksa library menggunakan API v1 agar tidak error 404
genai.api_version = "v1"

# 3. Mengambil API Key dengan aman dari Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Waduh, API Key Gemini belum terpasang dengan benar di Streamlit Secrets!")
    st.stop()

# 4. Bagian Input Cerita Pengguna
st.subheader("✍️ Tuliskan Cerita Anda")
cerita_user = st.text_area(
    "Contoh: 'Dia bekerja sebagai Pemilik Toko Sembako, Menjual Sembako'",
    height=100
)

# Tombol untuk memicu AI berpikir (wajib ada untuk menghemat kuota gratisan)
if st.button("Minta Rekomendasi AI"):
    if cerita_user:
        with st.spinner("AI sedang menganalisis cerita Anda, mohon tunggu..."):
            try:
                # Membuat Prompt (perintah) yang jelas untuk AI
                prompt_instruksi = f"""
                Anda adalah seorang ahli klasifikasi bisnis dan ketenagakerjaan di Indonesia.
                Berdasarkan cerita berikut: "{cerita_user}"
                
                Tolong berikan rekomendasi:
                1. Kode KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) yang paling cocok beserta penjelasan singkat fungsinya.
                2. Kode KBJI (Klasifikasi Baku Jabatan Indonesia) untuk profesi/pekerjaan yang disebutkan atau relevan beserta penjelasannya.
                
                Format jawaban harus rapi menggunakan poin-poin atau tabel Markdown agar mudah dibaca oleh pengguna.
                """
                
                # Memanggil Gemini AI
                response = model.generate_content(prompt_instruksi)
                
                # Menampilkan Hasil dari AI
                st.success("✨ Hasil Analisis AI:")
                st.markdown(response.text)
                
            except Exception as e:
                # Menangkap error jika kuota habis (Error 429) atau error lainnya
                st.error(f"Gagal mendapatkan respon dari AI. Error: {e}")
    else:
        st.warning("Silakan tulis ceritanya terlebih dahulu sebelum menekan tombol!")
