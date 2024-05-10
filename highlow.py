from PIL import Image
import os
from PyPDF2 import PdfWriter, PdfReader

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

desktop_path = os.path.expanduser("~/Desktop")
input_path = os.path.join(desktop_path, "highlow/input/")
output_path = os.path.join(desktop_path, "highlow/output/")
high_path = os.path.join(desktop_path, "highlow/high/")
low_path = os.path.join(desktop_path, "highlow/high/")

# Levágási méret
#margin_to_cut = 5  # mm-ben

# Konvertálás pontonként pixelre (1 inch = 25.4 mm)
#margin_to_cut_pixel = margin_to_cut / 25.4 * 72


# Ellenőrizzük, hogy a kimeneti mappa létezik-e
if not os.path.exists(output_path):
    os.makedirs(output_path)

#tobbi mappat letrehozzuk


# PDF-ek levágása
for filename in os.listdir(input_path):
    if filename.endswith(".pdf"):
        input_file_path = os.path.join(input_path, filename)
        output_file_path = os.path.join(output_path, filename)

        pdf_reader = PdfReader(input_file_path)
        pdf_writer = PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            # Oldal méretének módosítása
            #page.trimbox.lower_left = (25, 25)
            #page.trimbox.upper_right = (225, 225)
            page.cropbox.lower_left = (32, 32)
            page.cropbox.upper_right = (874, 969)
            pdf_writer.add_page(page)

        with open(output_file_path, "wb") as output_file:
            pdf_writer.write(output_file)

print("Levágás kész.")
