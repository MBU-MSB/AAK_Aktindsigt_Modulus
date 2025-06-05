"""Converts docx to PDF"""
from docx2pdf import convert


def docx_to_pdf(doc_path, pdf_path):
    """Converts docx to PDF"""

    # Convert the Word document to PDF
    convert(doc_path, pdf_path)

    print(f"Document converted to PDF and saved as {pdf_path}")


docx_to_pdf(r'C:\repos-py\031_01_Boris_Sletning_Go\robot_framework\dokumenter\Funktionsbeskrivelse-Klara%20-%20f%C3%A6rdig.docx', r'C:\repos-py\031_01_Boris_Sletning_Go\robot_framework\dokumenter_done\Klara.pdf')
