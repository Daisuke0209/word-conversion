import re
import pandas as pd
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

def convert_character(text : str):
    """
    Convert consecutive full-size numbers to half-size numbers.
    Convert a single half-size number into a full-size number.
    Convert half-size English characters to full-size ones.

    Parameters
    ----------
    text : str
        input text
    
    Returns
    ----------
    output : str
        converted text
    """
    list_text = list(text)

    half_nums = re.findall('[0-9]+', text)
    full_nums = re.findall('[０-９]+', text)

    c_half_nums = []
    for half_num in half_nums:
        if len(half_num) == 1:
            c_half_nums.append(half_num)

    c_full_nums = []
    for full_num in full_nums:
        if len(full_num) > 1:
            c_full_nums.append(full_num)

    #half to full
    for c_half_num in c_half_nums:
        index = text.find(c_half_num)
        convert = c_half_num.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
        list_text[index] = convert

    #full to half
    for c_full_num in c_full_nums:
        index = text.find(c_full_num)
        converts = c_full_num.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        for i, convert in enumerate(converts):
            list_text[index + i] = convert

    output = "".join(list_text)

    return output

def convert_eng_character(text : str):
    """
    Convert half-size English characters to full-size ones.

    Parameters
    ----------
    text : str
        input text
    
    Returns
    ----------
    output : str
        converted text
    """
    #Upper English character
    output = text.translate(str.maketrans({chr(0x0041 + i): chr(0xFF21 + i) for i in range(26)}))
    #Lower English character
    output = output.translate(str.maketrans({chr(0x0061 + i): chr(0xFF41 + i) for i in range(26)}))

    return output

def convert_docx(document : Document):
    """
    Convert a word file.

    Parameters
    ----------
    document : Document
        word file
    
    Returns
    ----------
    document : Document
        converted word file
    df : pd.DataFrame
        A dataframe that organizes the conversion points
    """
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

    df = pd.DataFrame([diff_indices, diff_originals, diff_covnerts]).T
    df.columns = ['index', 'original', 'converted']

    return document, df