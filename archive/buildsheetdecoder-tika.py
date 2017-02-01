# https://content.pivotal.io/blog/how-to-scalably-extract-insight-from-large-natural-language-documents
"""
Conversion using Apache Tika can be performed in a few different ways. You can run it locally and convert individual
documents or run a batch job specifying an input folder and an output folder. To do so, download the JAR (binary)
file and use one of the two commands.

https://tika.apache.org/download.html

Convert individual document:
   java -jar /path/to/jar/tika-app-1.11.jar --html MyDocument.doc > MyDocument.html

Batch convert folder:
   java -jar /path/to/jar/tika-app-1.11.jar --html –i input_folder -o output_folder
"""


from tika import parser
import re


parsedPDF = parser.from_file("bs1.pdf")
pdf = parsedPDF["content"]

#Replace double newlines with single newlines
pdf = pdf.replace('\n\n', '\n')

#pdf = pdf.replace('.> ','')
#pdf = pdf.replace('.>','')
pdf = pdf.replace('\ninst',' inst')
print(pdf)



def parseFile():
    print('test')