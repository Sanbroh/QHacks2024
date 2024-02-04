from tika import parser # pip install tika
import os
import openai
import json
import re
import PyPDF2

def split_pdf(pdf_name):
    pages = []
    pdf_file = pdf_name
    read_pdf = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(read_pdf.pages)
    for page_number in range(number_of_pages):   # use xrange in Py2
        page = read_pdf.pages[page_number].extract_text()  # Extract page wise text then split based on spaces as required by you
        pages.append(page)
    for i in range(0, len(pages)):
        pages[i] = list(create_paragraphs(pages[i]))
        pages[i] = pages[i][1:]
            # try:
            #     item = item.split(". \n")
            # except:
            #     pass
    return pages

def create_paragraphs(file_data_content):
    lines = file_data_content.splitlines(True)
    paragraph = []
    for line in lines:
        if line.isspace():
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph:
        yield ''.join(paragraph)
