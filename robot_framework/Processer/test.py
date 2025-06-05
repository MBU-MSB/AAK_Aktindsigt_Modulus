"""Test enkelte funktioner og simple metoder"""
from docx import Document

def save_without_macros(input_path, output_path):
    doc = Document(input_path)
    doc.save(output_path)

# Example usage
input_path = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt\17_0909108999\Modulus\BL%20%C2%A7%2087%20Tabt%20arbejdsfortjeneste%20-%20Afg%C3%B8relse%20-%20tilbagebetaling.docx"
output_path = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt\17_0909108999\Modulus\BL%20%C2%A7%2087%20Tabt%20arbejdsfortjeneste%20-%20Afg%C3%B8relse%20-%20tilbagebetaling2.docx"
save_without_macros(input_path, output_path)