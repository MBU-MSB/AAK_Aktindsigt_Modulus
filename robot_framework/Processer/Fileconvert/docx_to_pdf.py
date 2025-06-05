"""Converts docx to PDF"""
from docx2pdf import convert


def docx_to_pdf(doc_path):
    """Converts docx to PDF"""
    output_path = str(doc_path).replace(".docx", ".pdf")

    # Convert the Word document to PDF
    convert(doc_path, output_path)

    print(f"Document converted to PDF and saved as {output_path}")
