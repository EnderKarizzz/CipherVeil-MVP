import streamlit as st
# Impor fungsi backend yang dibuat Almer & Dapa
# from core.workflows import embed_pdf 

st.title("Embed PDF ke Gambar")
st.write("Enkripsi PDF Anda dan sisipkan ke dalam gambar sampul.")

# 1. Upload File
pdf_file = st.file_uploader("1. Pilih dokumen PDF", type=["pdf"])
cover_image = st.file_uploader("2. Pilih gambar sampul", type=["png", "jpg", "jpeg", "bmp"])

# 2. Pilih Mode Penempatan Bit (Ditambahkan sesuai spesifikasi Paket 2)
mode_options = {
    1: "Mode 1: Sekuensial (Baseline)",
    2: "Mode 2: Acak Berbasis Kunci (AES-CTR)",
    3: "Mode 3: Adaptif Tepi (Sobel)"
}
selected_mode_key = st.selectbox(
    "3. Pilih Mode Penempatan Bit", 
    options=[1, 2, 3], 
    format_func=lambda x: mode_options[x]
)

# 3. Input Password
password = st.text_input("4. Masukkan Password Enkripsi", type="password")

if st.button("Encrypt & Embed"):
    if pdf_file and cover_image and password:
        with st.spinner("Memproses enkripsi dan steganografi..."):
            try:
                from core.workflows import embed_pdf
                pdf_bytes = pdf_file.read()
                image_bytes = cover_image.read()
                
                stego_png_bytes = embed_pdf(pdf_bytes, image_bytes, password, mode=selected_mode_key)
                
                st.success("Berhasil! Gambar stego siap diunduh.")
                st.download_button(
                    label="Unduh Gambar Stego (PNG)",
                    data=stego_png_bytes,
                    file_name="cipherveil_stego.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Harap lengkapi semua unggahan dan password!")