#import packages
import os
import io
from PIL import Image 
# import pytesseract
# from wand.image import Image as wi
from os import listdir, mkdir
from os.path import dirname, exists, isdir, realpath, isfile, join
from django.contrib import messages
from fpdf import FPDF

# Path for scanned files
SCANNED_FILES_DIR = "/home/pi/Documents/"

class PDF(FPDF):
    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def create_dir(folder_name):
    content = SCANNED_FILES_DIR + folder_name
    if not os.path.exists(content):
        print('[SUCCESS] Folder created')
        mkdir(content)
        return True
    else:
        print (content)
        print('[ERROR] Folder already exists!')
        return False

def format_list(input):
    lines = []
    while True:
        index = input.find('\n')
        if index is -1:
            lines.append(input)
            break
        lines.append(input[:index])
        input = input[index+1:]
    return lines

def generate_pdf(contents, doc_title):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)

    for content in contents:
        for line in content:
            pdf.multi_cell(0, 5, line, 0,1)

    os.chdir(SCANNED_FILES_DIR + doc_title + '/')
    pdf.output(doc_title + ".pdf", 'F')
    return True