import streamlit as st
import google.generativeai as genai

# Tambahkan baris ini sebelum memanggil model!
genai.api_version = "v1" 

# Baru setelah itu konfigurasi API Key dan Model
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Konfigurasi Tampilan Website
st.set_page_config(page_title="AI KBLI-KBJI Maluku Utara", page_icon="📊", layout="centered")

# Mengambil API Key secara aman dari sistem Streamlit
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("Waduh, API Key Gemini belum dipasang di Settings Streamlit! Tolong dimasukkan dulu ya.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Desain Header Website
st.title("📊 Asisten KBLI & KBJI Digital")
st.subheader("BPS Kota Tidore Kepulauan")
st.markdown("Aplikasi ini membantu PML menentukan kode KBLI dan KBJI berdasarkan cerita atau rincian tugas responden di lapangan.")
st.markdown("---")

# Form Input untuk PML
with st.form("form_pencarian"):
    cerita = st.text_area(
        "Cerita / Uraian Tugas Responden:",
        placeholder="Contoh: Dia punya perahu sendiri dan sering memancing ikan cakalang di laut Halmahera, lalu hasilnya dijual ke pengepul di pelabuhan.",
        height=150
    )
    submit_button = st.form_submit_button(label="🔍 Analisis Kode Sekarang")

# Proses Analisis AI setelah tombol diklik
if submit_button:
    if not cerita.strip():
        st.warning("Ceritanya diisi dulu ya, jangan dikosongkan.")
    else:
        with st.spinner("Menghitung dan mencocokkan kode dengan standar BPS... Mohon tunggu..."):
            try:
                # Menggunakan model Gemini terbaru yang stabil
                # model = genai.GenerativeModel('gemini-1.5-flash-latest')
                # atau jika ingin pakai versi terbaru:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Instruksi khusus (Prompt Engineering) agar AI paham konteks lokal Malut dan BPS
                prompt = f"""
                Anda adalah seorang pakar metodologi sensus/survei di Badan Pusat Statistik (BPS) Indonesia yang bertugas di Provinsi Maluku Utara.
                Tugas Anda adalah menganalisis cerita/uraian kegiatan berikut dan menentukan Kode KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) tahun terbaru dan Kode KBJI (Klasifikasi Baku Jabatan Indonesia) yang paling tepat beserta deskripsinya.
                Pahami juga istilah lokal Maluku Utara seperti pajeko, jolor, pala, cengkeh, dlsb jika ada.

                Cerita Responden: "{cerita}"

                Berikan jawaban langsung dalam format Markdown yang rapi dan menarik seperti di bawah ini:
                
                ### 🏭 Hasil Analisis KBLI:
                * **Kode KBLI:** [Berikan kode 5 digit yang paling relevan]
                * **Judul KBLI:** [Nama judul KBLI]
                * **Deskripsi Singkat:** [Alasan mengapa kode ini dipilih berdasarkan cerita]

                ### 👔 Hasil Analisis KBJI:
                * **Kode KBJI:** [Berikan kode 4 digit yang paling relevan]
                * **Judul KBJI:** [Nama judul KBJI]
                * **Deskripsi Singkat:** [Alasan mengapa kode ini dipilih berdasarkan cerita]
                
                ---
                *Catatan: Jawaban AI ini bersifat membantu. PML disarankan tetap melakukan verifikasi kembali ke buku pedoman resmi jika menemui keraguan ekstrem.*
                """
                
                response = model.generate_content(prompt)
                
                # Menampilkan Hasil ke Layar
                st.success("Selesai! Berikut adalah rekomendasi kodenya:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Aduh, ada error sistem nih: {e}")
