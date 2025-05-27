from fpdf import FPDF
import os


def add_testfiles(folderpath: str):
    # Ensure the folder exists
    os.makedirs(folderpath, exist_ok=True)

    # Create 3 PDF files
    for i in range(3):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Set title with lorem ipsum
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Lorem Ipsum Title {i+1}", ln=1, align="C")

        # Add text
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, txt="Hello", align="L")

        # Save the PDF file
        pdf.output(f"{folderpath}/test_file_{i+1}.pdf")


add_testfiles(r'\\srvsql46\INDBAKKE\AAK_Aktindsigt\10_0509820000\Modulus')