import os
import subprocess
import tempfile
import streamlit as st

st.title("Conversor de Word (.docx) para PDF")

uploaded_file = st.file_uploader("Envie seu arquivo Word", type=["docx"])

if uploaded_file is not None:
  # Salva o arquivo enviado em um diretório temporário
  
  # Comando do LibreOffice para converter docx em pdf
  try:
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            uploaded_file.getvalue(),
            "--outdir",
            output_dir,
        ],
        check=True,
    )
    
    with open(pdf_path, "rb") as f:
      st.download_button(
          label="Baixar PDF",
          data=f,
          file_name=pdf_filename,
          mime="application/pdf",
      )

    st.success("Conversão realizada com sucesso!")

  except Exception as e:
    st.error(f"Erro na conversão: {e}")

