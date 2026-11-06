import os
import subprocess
import tempfile
import streamlit as st

st.title("Conversor de Word (.docx) para PDF")

uploaded_file = st.file_uploader("Envie seu arquivo Word", type=["docx"])

if uploaded_file is not None:
  # Salva o arquivo enviado em um diretório temporário
  with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_in:
    tmp_in.write(uploaded_file.getvalue())
    tmp_in_path = tmp_in.name

  output_dir = tempfile.gettempdir()

  # Comando do LibreOffice para converter docx em pdf
  try:
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            tmp_in_path,
            "--outdir",
            output_dir,
        ],
        check=True,
    )

    pdf_filename = (
        os.path.splitext(os.path.basename(uploaded_file.name))[0] + ".pdf"
    )
    pdf_path = os.path.join(output_dir, pdf_filename)

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
