import os
import argparse
import pandas as pd
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from modules.tools import convert_character, convert_eng_character

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

  diff_originals, diff_covnerts, diff_indices = [], [], []
  for i, paragraph in enumerate(document.paragraphs):
    original_text = paragraph.text
    paragraph.text = convert_character(paragraph.text)
    paragraph.text = convert_eng_character(paragraph.text)
    if original_text != paragraph.text:
      paragraph.runs[0].font.highlight_color = WD_COLOR_INDEX.YELLOW
      diff_originals.append(original_text)
      diff_covnerts.append(paragraph.text)
      diff_indices.append(i)

  document.save(folder + output_filename)
  df = pd.DataFrame([diff_indices, diff_originals, diff_covnerts]).T
  df.columns = ['index', 'original', 'converted']
  df.to_csv(folder + diff_filename, index = False)


