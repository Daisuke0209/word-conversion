from docx import Document
from modules.tools import convert_character, convert_eng_character

folder = "data/"
filename = "test.docx"
output_filename = filename.split('.')[0] + "-converted.docx"

document = Document(folder + filename)

for i in document.paragraphs:
  i.text = convert_character(i.text)
  i.text = convert_eng_character(i.text)

document.save(folder + output_filename)

