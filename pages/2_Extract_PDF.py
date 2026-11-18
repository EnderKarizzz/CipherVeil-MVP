import streamlit as st
# Impor fungsi backend yang dibuat Almer & Dapa
# from core.workflows import extract_pdf 

st.title("Extract PDF dari Gambar")
st.write("Pulihkan dokumen PDF Anda dari gambar CipherVeil.")

stego_image = st.file_uploader("1. Pilih gambar stego (Wajib PNG)", type=["png"])
password = st.text_input("2. Masukkan Password Dekripsi", type="password")

if st.button("Extract PDF"):
    if stego_image and password:
        with st.spinner("Memproses ekstraksi dan dekripsi..."):
            try:
                from core.workflows import extract_pdf
                image_bytes = stego_image.read()
                
                recovered_pdf_bytes = extract_pdf(image_bytes, password)
                
                st.success("Autentikasi berhasil! Dokumen PDF berhasil dipulihkan.")
                st.download_button(
                    label="Unduh PDF",
                    data=recovered_pdf_bytes,
                    file_name="recovered_document.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error("Ekstraksi gagal. Password salah, format tidak didukung, atau gambar telah dimodifikasi.")
    else:
        st.warning("Harap unggah gambar dan masukkan password!")