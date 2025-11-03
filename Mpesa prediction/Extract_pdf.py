import io

import pandas as pd
import numpy as np
import PyPDF2
import pikepdf
import warnings
warnings.filterwarnings('ignore')
from tabula.io import read_pdf
from dateutil import parser

input_path = "/Users/briankimanzi/Downloads/Mpesa pdfs/Statement_All_Transactions_20240901_20250301.pdf"
output_path = "/Users/briankimanzi/Downloads/Mpesa pdfs/Tracking.pdf"
password = "102030"

with pikepdf.open(input_path, password=password) as pdf:
    pdf.save(output_path)
path = output_path

def extract_mpesa_data(uploaded_file, password=None):
    try:
        file_byte = uploaded_file.read()

        with pikepdf.open(io.BytesIO(file_byte), password=password) as pdf:
            decrypted_byte = io.BytesIO()
