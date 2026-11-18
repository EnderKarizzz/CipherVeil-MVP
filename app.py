import streamlit as st

st.set_page_config(
    page_title="CipherVeil MVP",
    page_icon="🔐",
    layout="centered"
)

st.title("CipherVeil")
st.caption("Secure document concealment using cryptography and steganography.")

st.markdown("""
### Selamat Datang di CipherVeil
Aplikasi ini memungkinkan Anda untuk mengenkripsi dokumen PDF rahasia dan menyembunyikannya di dalam gambar menggunakan metode steganografi.
* **Embed PDF:** Untuk menyisipkan file.
* **Extract PDF:** Untuk memulihkan file dari gambar.

Silakan gunakan menu navigasi di sebelah kiri untuk memulai.
""")