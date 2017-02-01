from PyPDF2 import PdfFileReader
pdf_file = 'bs1.pdf'
read_pdf = PdfFileReader(pdf_file, 'rb')
page = read_pdf.getPage(1)
print(page.extractText)