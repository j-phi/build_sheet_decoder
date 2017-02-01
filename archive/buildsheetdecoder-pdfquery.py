import pdfquery

pdf1 = pdfquery.PDFQuery('bs1.pdf')
pdf1.load()

#pdf = pdf.tree.tostring()

print(pdf1.tree.write(filename, pretty_print=True))