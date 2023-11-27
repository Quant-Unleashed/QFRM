#Read PDF

import PyPDF2

pdfFileObj = open('2.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print(pdfReader.getPage(8).extractText())





