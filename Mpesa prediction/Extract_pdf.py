import io
import tempfile
import pandas as pd
import numpy as np
import PyPDF2
import pdfplumber
import pikepdf
import warnings
warnings.filterwarnings('ignore')
from tabula.io import read_pdf
from dateutil import parser


def extract_mpesa_data(uploaded_file, password=""):
    try:
        if password is None:
            password = ""

        file_bytes = uploaded_file.read()

        decrypted_bytes = io.BytesIO()
        with pikepdf.open(io.BytesIO(file_bytes), password=password) as pdf:
            pdf.save(decrypted_bytes)
        decrypted_bytes.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(decrypted_bytes.read())
            tmp_path = tmp_pdf.name

        with open(tmp_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

        def get_data():
            return_df = pd.DataFrame()
            for page_number in range(1, num_pages + 1):
                df_list = read_pdf(tmp_path, pages=page_number, multiple_tables=True)
                if not df_list:
                    continue

                data = df_list[-1] if page_number == 1 and len(df_list) > 1 else df_list[0]
                return_df = pd.concat([return_df, data], ignore_index=True)
            return return_df

        working_data = get_data()

        working_data = working_data.dropna(how='all')
        working_data.reset_index(drop=True, inplace=True)

        return working_data

    except Exception as e:
        print(f" Error while processing PDF: {e}")
        return None
