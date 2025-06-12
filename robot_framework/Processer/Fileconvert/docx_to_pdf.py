"""Converts docx to PDF"""
import os
from docx2pdf import convert


def docx_to_pdf(doc_path):
    """Converts docx to PDF"""

    # Extract the filename from the doc_path and construct the output path
    output_folder = r'\\srvsql46\INDBAKKE\AAK_Aktindsigt\Test_resultater'
    doc_filename = os.path.basename(doc_path)
    pdf_filename = str(doc_filename).replace(".docx", ".pdf")
    output_path = os.path.join(output_folder, pdf_filename)

    # Convert the Word document to PDF
    convert(doc_path, output_path)

    print(f"Document converted to PDF and saved as {output_path}")
