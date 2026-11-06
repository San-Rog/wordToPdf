import os
import subprocess
import tempfile
import streamlit as st

st.title("Conversor de Word (.docx) para PDF")

uploaded_file = st.file_uploader("Envie seu arquivo Word (.docx)", type=["docx"])

if uploaded_file is not None:
  if st.button("Converter para PDF"):
    # 1. Salvar os bytes do arquivo enviado em um arquivo temporário de entrada
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
      tmp_docx.write(uploaded_file.getvalue())
      tmp_docx_path = tmp_docx.name

    # 2. Definir o diretório de saída temporário
    output_dir = tempfile.mkdtemp()

    try:
      # 3. Rodar o LibreOffice em modo headless para converter .docx em .pdf
      subprocess.run(
          [
              "libreoffice",
              "--headless",
              "--convert-to",
              "pdf",
              tmp_docx_path,
              "--outdir",
              output_dir,
          ],
          check=True,
      )

      # 4. Obter o caminho do arquivo PDF gerado
      base_name = os.path.splitext(os.path.basename(tmp_docx_path))[0]
      pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

      # 5. Ler os bytes do PDF gerado
      with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

      st.success("Conversão realizada com sucesso!")

      # 6. Botão de download para o usuário
      st.download_button(
          label="Baixar PDF",
          data=pdf_bytes,
          file_name=f"{base_name}.pdf",
          mime="application/pdf",
      )

    except Exception as e:
      st.error(f"Erro na conversão: {e}")

    finally:
      # Limpar arquivos temporários
      if os.path.exists(tmp_docx_path):
        os.remove(tmp_docx_path)


