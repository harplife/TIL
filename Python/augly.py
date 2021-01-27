def to_piglatin(normal_speak:str="") -> str:
    '''
    words that would become unpronounable with common pig latin rules,
    such as is, on, or etc, is only appended 'yay' at the end.
    TODO: add the rule above.
    
    ref: https://lingojam.com/PigLatinTranslator
    '''

    words = normal_speak.split(' ')
    wbag = []
    for _word in words:
        word = list(_word.lower())
        first_letter = word[0]
        second_letter = word[1]
        if first_letter in 'aeiou':
            pig_latin = word + 'ay'
            wbag.append(pig_latin)
        else:
            if second_letter in 'aeiou':
                word.pop(0)
                reword = ''.join(word)
                pig_latin = reword + first_letter + 'ay'
                wbag.append(pig_latin)
            else:
                word.pop(0)
                word.pop(0)
                reword = ''.join(word)
                pig_latin = reword + first_letter + second_letter + 'ay'
                wbag.append(pig_latin)

    return ' '.join(wbag)


def piglatin_to_normal(piglatin_speak:str="") -> str:
    # TODO: piglatin to normal
    
    return piglatin_speak


def to_leet(normal_speak:str="") -> str:

    l33t_mapping = str.maketrans("iseoau", "1530^Ü")
    return normal_speak.translate(l33t_mapping).title().swapcase()


def leet_to_normal(l33t_speak:str="") -> str:

    l33t_reverse_mapping = str.maketrans("1530^Ü", "iseoau")
    return l33t_speak.translate(l33t_reverse_mapping).lower()


def to_japangrish(normal_speak:str="") -> str:
    
    # https://www.kaggle.com/reppic/predicting-english-pronunciations
    
    # TODO: convert word to phoneme
    # TODO: mutate phoneme accordingly to asian accent
    # TODO: mutate consonant accordingly to asian accent
    # EXAMPLE: clever -> ku-reh-va-ru, mcDonalds -> meku-do-naru-du
    
    return