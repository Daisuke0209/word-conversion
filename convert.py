import os
import argparse
from docx import Document
from modules.tools import convert_docx

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file', type = str, required = True)
  args = parser.parse_args( )
  if not os.path.isfile(args.file):
    raise ValueError("The file does not exist.")

  folder = os.path.dirname(args.file) + "/"
  filename = os.path.basename(args.file)
  output_filename = filename.split('.')[0] + "-converted.docx"
  diff_filename = filename.split('.')[0] + "-diff.csv"

  document = Document(folder + filename)
  document, df = convert_docx(document)

  document.save(folder + output_filename)
  df.to_csv(folder + diff_filename, index = False)


