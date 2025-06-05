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


def msg_to_pdf(msg_path, pdf_path):
    """Extracts a given msg file to PDF"""
    # Extract content from MSG file
    msg = Message(msg_path)

    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add text content to PDF
    pdf.cell(200, 10, txt="Subject: " + msg.subject, ln=1)
    pdf.cell(200, 10, txt="From: " + msg.sender, ln=1)
    pdf.cell(200, 10, txt="To: " + ", ".join(msg.to), ln=1)
    pdf.cell(200, 10, txt="Date: " + str(msg.date), ln=1)
    pdf.multi_cell(0, 10, txt="Body: " + msg.body)

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

    # Save the PDF
    pdf.output(pdf_path)


# Example usage
msg_to_pdf(r'C:\repos-py\031_01_Boris_Sletning_Go\robot_framework\dokumenter\Klara.msg', r'C:\repos-py\031_01_Boris_Sletning_Go\robot_framework\dokumenter_done\Klara.pdf')
