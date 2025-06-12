"""Extracts a given msg file to PDF"""
import os
from extract_msg import Message
from PIL import Image
from fpdf import FPDF


def _add_image_to_pdf(pdf, image_path, max_width=180):
    """Adjust image properties"""
    # Open the image to get its dimensions
    with Image.open(image_path) as img:
        width, height = img.size

    # Calculate the aspect ratio
    aspect_ratio = height / width

    # Set the width and calculate the height to maintain the aspect ratio
    width = min(width, max_width)
    height = width * aspect_ratio

    # Add the image to the PDF
    pdf.image(image_path, x=10, y=None, w=width)


def msg_to_pdf(msg_path):
    """Extracts a given msg file to PDF"""

    output_folder = r'\\srvsql46\INDBAKKE\AAK_Aktindsigt\Test_resultater'
    # Extract content from MSG file
    msg = Message(msg_path)

    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()

    # Use a Unicode font
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)

    # No need to sanitize text - fpdf2 handles Unicode
    pdf.cell(200, 10, text="Subject: " + (msg.subject or ""), ln=1)
    pdf.cell(200, 10, text="From: " + (msg.sender or ""), ln=1)
    pdf.cell(200, 10, text="To: " + ", ".join(msg.to or []), ln=1)
    pdf.cell(200, 10, text="Date: " + str(msg.date or ""), ln=1)
    pdf.multi_cell(0, 10, text="Body: " + (msg.body or ""))

    # Extract and add images to PDF
    for attachment in msg.attachments:
        if hasattr(attachment, 'data') and attachment.longFilename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Save the image temporarily
            image_path = os.path.join('temp_images', attachment.longFilename)
            os.makedirs('temp_images', exist_ok=True)
            with open(image_path, 'wb') as image_file:
                image_file.write(attachment.data)

            # Add the image to the PDF
            _add_image_to_pdf(pdf, image_path)

    # Generate the PDF filename based on the MSG filename
    msg_filename = os.path.basename(msg_path)
    pdf_filename = os.path.splitext(msg_filename)[0] + '.pdf'
    pdf_path = os.path.join(output_folder, pdf_filename)

    # Save the PDF
    pdf.output(pdf_path)
