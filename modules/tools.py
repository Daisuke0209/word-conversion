import re

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
    output = text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

    return output