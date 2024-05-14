from PIL import Image, ImageDraw, ImageFont
import os
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path


desktop_path = os.path.expanduser("~/Desktop")
input_path = os.path.join(desktop_path, "highlow/input/")
output_path = os.path.join(desktop_path, "highlow/output/")
high_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/high/")
low_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/low/")
jpg_path = os.path.join(desktop_path, "highlow/output/_JPG_PDF/jpg/")
low_pdf_quality = 5


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
    for filename in os.listdir(input_path):
        if filename.endswith(".pdf"):

            # Eredeti fájlnév utolsó 8 karakterének eltávolítása
            base_filename = os.path.splitext(filename)[0]
            shortened_filename = base_filename[:-8]+".pdf"


            input_file_path = os.path.join(input_path, filename)
            high_output_file_path = os.path.join(high_path, shortened_filename)
            #low_output_file_path = os.path.join(low_path, filename)




            pdf_reader = PdfReader(input_file_path)
            pdf_writer_high = PdfWriter()
            #pdf_writer_low = PdfWriter()


            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Oldal méretének módosítása
                # page.trimbox.lower_left = (25, 25)
                # page.trimbox.upper_right = (225, 225)
                page.cropbox.lower_left = (32, 32)
                page.cropbox.upper_right = (874, 969)
                pdf_writer_high.add_page(page)

            with open(high_output_file_path, "wb") as output_file:
                pdf_writer_high.write(output_file)

            

            

        


            


def compress_pdf():
    for filename in os.listdir(high_path):
        if filename.endswith(".pdf"):
            high_output_file_path = os.path.join(high_path, filename)
            low_output_file_path = os.path.join(low_path, filename)

            input_file_path = os.path.join(high_output_file_path)
            pdf_reader = PdfReader(input_file_path)
            pdf_writer_low = PdfWriter()

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                for page in pdf_reader.pages:
                    pdf_writer_low.add_page(page)

                for page in pdf_writer_low.pages:
                    for img in page.images:
                        img.replace(img.image, quality=low_pdf_quality)
                
            with open(low_output_file_path, "wb") as output_file:
                pdf_writer_low.write(output_file)



def convert_to_jpg():

    for filename in os.listdir(low_path):
        if filename.endswith(".pdf"):
            high_output_file_path = os.path.join(high_path, filename)
            pages = convert_from_path(high_output_file_path)
             
            for count, page in enumerate(pages):
                jpg_output_file_path = os.path.join(jpg_path, f"{os.path.splitext(filename)[0]}.jpg")
                page.save(jpg_output_file_path, 'JPEG')


def crop_jpgs():
    for filename in os.listdir(jpg_path):
        if filename.endswith(".jpg"):
            temp_file_path = os.path.join(jpg_path, filename)
            img = Image.open(temp_file_path)
            cropped_img = img.crop((88,53,2425,2700))

            cropped_img.save(jpg_path + filename)





folderMaker()
pdfCropper()
compress_pdf()
convert_to_jpg()
crop_jpgs()
