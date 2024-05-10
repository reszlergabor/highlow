from PIL import Image
import os

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

desktop_path = os.path.expanduser("~/Desktop")
input_path = os.path.join(desktop_path, "highlow/input/")
output_path = os.path.join(desktop_path, "highlow/output/")
high_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/high/")
low_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/low/")
jpg_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/jpg/")

# Levágási méret
#margin_to_cut = 5  # mm-ben

# Konvertálás pontonként pixelre (1 inch = 25.4 mm)
#margin_to_cut_pixel = margin_to_cut / 25.4 * 72

def folderMaker():
    # Ellenőrizzük, hogy a kimeneti mappa létezik-e
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #tobbi mappat letrehozzuk
    if not os.path.exists(high_path):
        os.makedirs(high_path)
    if not os.path.exists(low_path):
        os.makedirs(low_path)
    if not os.path.exists(jpg_path):
        os.makedirs(jpg_path)



def pdfCropper():
    # PDF-ek levágása
    for filename in os.listdir(input_path):
        if filename.endswith(".pdf"):
            input_file_path = os.path.join(input_path, filename)
            high_output_file_path = os.path.join(high_path, filename)
            low_output_file_path = os.path.join(low_path, filename)

            pdf_reader = PdfReader(input_file_path)
            pdf_writer_high = PdfWriter()
            pdf_writer_low = PdfWriter()

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Oldal méretének módosítása
                #page.trimbox.lower_left = (25, 25)
                #page.trimbox.upper_right = (225, 225)
                page.cropbox.lower_left = (32, 32)
                page.cropbox.upper_right = (874, 969)
                pdf_writer_high.add_page(page)

            with open(high_output_file_path, "wb") as output_file:
                pdf_writer_high.write(output_file)

            page.compress_content_streams()  # This is CPU intensive!
            pdf_writer_low.add_page(page)

            with open(low_output_file_path, "wb") as output_file:
                pdf_writer_low.write(output_file)

#print("Levágás kész.")

folderMaker()
pdfCropper()