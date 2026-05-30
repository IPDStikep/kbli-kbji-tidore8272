import streamlit as st
from google import genai
from google.genai import types

# 1. Konfigurasi API Key (Ganti dengan API Key Anda atau gunakan environment variable)
# Disarankan menggunakan st.secrets untuk keamanan jika dideploy
API_KEY = "PASTE_API_KEY_GOOGLE_AI_STUDIO_ANDA_DISINI"

# Inisialisasi Client Gemini
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Gagal inisialisasi API Key: {e}")

# Setup halaman Streamlit
st.set_page_config(page_title="AI KBLI-KBJI Malut", page_icon="🌋", layout="centered")

st.title("Asisten KBLI & KBJI AI 🌋")
st.subheader("BPS Kota Tidore Kepulauan")
st.write("Sistem otomatis pencarian kode KBLI dan KBJI berdasarkan cerita kasus petugas di lapangan.")

st.markdown("---")

# 2. Input Kasus dari PML
kasus_lapangan = st.text_area(
    "Cerita Kasus dari Lapangan (PML):", 
    placeholder="Contoh: Responden adalah seorang ibu di Tidore yang menerima pesanan pembuatan sarung tenun khas daerah di rumahnya, kadang dibantu anak perempuan tanpa digaji...",
    height=150
)

# Tombol Proses
if st.button("Analisis Kode KBLI & KBJI ✨", type="primary"):
    if not kasus_lapangan:
        st.warning("Silakan masukkan cerita kasus lapangan terlebih dahulu!")
    elif API_KEY == "PASTE_API_KEY_GOOGLE_AI_STUDIO_ANDA_DISINI":
        st.error("API Key belum diisi! Silakan masukkan API Key Google AI Studio Anda di dalam kode.")
    else:
        with st.spinner("AI sedang menganalisis kasus dan mencocokkan kode..."):
            
            # 3. Definisi Aturan & Istilah Lokal (System Instruction)
            instruksi_sistem = """
            Anda adalah seorang pakar metodologi statistik dari BPS (Badan Pusat Statistik) Provinsi Maluku Utara. 
            Tugas Anda adalah menganalisis cerita kasus ketenagakerjaan dari petugas lapangan (PML) dan menentukan 
            rekomendasi kode KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) dan KBJI (Klasifikasi Baku Jabatan Indonesia) yang paling tepat.

            PENTING: Anda harus memahami istilah lokal Maluku Utara berikut jika muncul dalam cerita:
            - "Papalele" atau "Jaga Papalele": Merujuk pada pedagang eceran (biasanya ikan, sayur, atau hasil bumi) di pasar atau keliling.
            - "Dibo-dibo": Merujuk pada pedagang pengumpul / perantara / tengkulak hasil pertanian atau perikanan.
            - "Ketinting": Perahu motor kecil yang digunakan nelayan untuk menangkap ikan.
            - "Bia": Kerang/kerang-kerangan.
            - "Dulang Emas": Penambangan emas rakyat secara tradisional.

            Format Output harus rapi menggunakan Markdown dengan struktur:
            ### 📌 Rekomendasi KBLI (Pilih 1-2 kode yang paling relevan)
            - **Kode KBLI**: [Nomor Kode] - [Nama KBLI]
              *Penjelasan*: [Alasan kenapa kode ini dipilih berdasarkan cerita]

            ### 👔 Rekomendasi KBJI (Pilih 1-2 kode yang paling relevan)
            - **Kode KBJI**: [Nomor Kode] - [Nama Jabatan]
              *Penjelasan*: [Alasan kenapa kode ini dipilih berdasarkan cerita]

            ### 📊 Analisis Tambahan (Opsional)
            - Status Pekerjaan Utama yang disarankan (misal: Berusaha Sendiri, Buruh/Karyawan, Pekerja Keluarga/Tidak Dibayar).
            """

            try:
                # 4. Memanggil API Gemini (Menggunakan model gemini-2.5-flash yang cepat dan hemat)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=kasus_lapangan,
                    config=types.GenerateContentConfig(
                        system_instruction=instruksi_sistem,
                        temperature=0.3, # Nilai rendah agar jawaban lebih konsisten/tidak halusinasi
                    )
                )
                
                # Tampilkan Hasil
                st.success("Analisis Selesai!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi Gemini API: {e}")

st.markdown("---")
st.caption("© 2026 BPS Kota Tidore Kepulauan")
