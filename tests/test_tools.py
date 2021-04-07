from modules.tools import convert_character, convert_eng_character

def test_convert_character():
    """
    Test the function of convert_character
    """
    text = "令和3年１２月"
    output = "令和３年12月"
    assert convert_character(text) == output

def test_convert_eng_character():
    """
    Test the function of convert_eng_character
    """
    text = "ABab1"
    output = "ＡＢａｂ1"
    assert convert_eng_character(text) == output