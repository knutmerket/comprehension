"""
Simple program meant to illustrate what reading comprehension at x% really looks like.

Currently a crude implementation, here are some of the shortcomings:
* Not taking word frequency into account at all (should perhaps be weighted so that very common words are less likely to be omitted from the final output)
* Not able to recognize proper nouns (one could argue that these should be excluded from the "blanked out word" candidates)
"""

import pandas as pd
import jieba
import random
import re


def program(text, comprehension_as_ratio, language="NO"):
    unaltered_text = text # Copy kept to use in the final reinsertion of "non-chracters" (to avoid including white spaces for Chinese, which are added for convenience to text in the if statement below)
    if language == "CN": #If Chinese, we need to use a segmenter to get the individual words (due to the lack of a word separator)
        segmented_text = jieba.lcut(text, cut_all=False)
        text = (" ".join(segmented_text)) # Convert segmented list to string, adding white spaces.
    test_string_split = re.findall(r'(?:(?![\d_])\w)+', text.lower())
    word_list = list(dict.fromkeys(test_string_split)) # Remove duplicate list items by converting to dict (which cannot have duplicate keys) and creating a list from this
    word_dict = dict(zip(word_list, word_list)) # Make dictionary with unique words as keys, and same unique words as values. Will be used later to keep track of which words were blanked out.

    denominator = len(word_dict)
    num_words_to_blank_out = round((1-comprehension_as_ratio)*denominator) # decide number of unique words that should be blanked out
    words_to_blank_out = [] # Empty list to be populated
    for i in range(num_words_to_blank_out):
        random_word = random.choice(word_list)
        words_to_blank_out.append(random_word)
    #blanked_word_dict = {k:("|*****|" if v in words_to_blank_out else v) for k, v in word_dict.items()}
    blanked_word_dict = {k:("*"*len(v) if v in words_to_blank_out else v) for k, v in word_dict.items()} # for blanked words, replace values (but keep key) in dict with one * per length of the word.

    # Performing split of test_string to replace blanked words, then joining to recreate string.
    test_string_split_original_case = re.findall(r'(?:(?![\d_])\w)+', text)
    res = []
    for word in test_string_split_original_case:
        if word.isupper(): # If whole word is capitalized then retain this in output
            res.append(blanked_word_dict.get(word.lower(), word).upper())
        elif word[0].isupper(): # If only first letter of word is capitalized then retain this in output
            res.append(blanked_word_dict.get(word.lower(), word).capitalize())
        else:
            res.append(blanked_word_dict.get(word, word))
    final_result = "".join(res)
    print("\n", 'Here is the "comprehension adjusted" output:', "\n", final_result)


    # Then we extract any "non-chracters" (e.g. punctuation, numbers, white spaces etc.) from the original text string, and add them back into the result
    non_character_dict = {}
    i = 0
    for element in unaltered_text:
        if re.search(r'(?:(?![\d_])\w)+', element.lower()) is None:
            non_character_dict[i] = element # Add element to dictionary with index as the key
        i += 1
    for k,v in non_character_dict.items():
        final_result = final_result[:k] + v + final_result[k:]
    print("HER KOMMER OPPRINELIG TEKST \n", unaltered_text)
    print("HER KOMMER DICT \n", non_character_dict)
    print("HER KOMMER final_result \n", final_result)


# TODO: Fetches freqlist from get_freq_list_table function
def get_language_frequency_list(language):
    pass

# TODO: Function (should be moved to a separate file later) for fetching frequency lists for different languages. Consider whether or not it is worth it, compared to just storing those lists 
# (which are unlikely) to change much) as individual csv files instead.
def get_freq_list_table(language):
    pass
    # url = "https://www.korrekturavdelingen.no/ord-uttrykk-frekvensordliste-500-vanligste-norsk.htm"
    # df = pd.read_html(url)
    # df = df[0].drop(columns=0)
    # print(df)


#test_string = "Det ble dramatisk på Miljøpartiet De Grønnes digitale landsmøte lørdag. Ny partileder skulle velges. Une Bastholm meldte overraskende sin avgang som partileder i august. Det sto mellom nestleder Arild Hermstad og utfordrer Kristoffer Robin Haug. Hermstad var den suverent beste kandidaten», sa valgkomiteens leder Trude Thy. Thy talte på vegne av en samlet valgkomité. Men store deler av den digitale landsmøtesalen var ikke enig. Hermstad maktet å overbevise nøyaktig halvparten av de stemmegivende. Med 102 mot 101 stemmer ble Hermstad valgt. Én blank stemme ble utslagsgivende. Hadde den gått til Haug, kunne valget blitt avgjort ved loddtrekning. Haugs popularitet må sees på som et uttrykk for misnøye med «sentralmakten» i MDG. Valgresultatet i 2021 var et hardt slag internt i partiet, ikke minst fordi store deler av valgkampen handlet om klima. Forslagsstiller for Haug, Brynjar Arnfinnson, mente Haug var bedre til å gi folk håp – velgere så vel som medlemmer. Støttetaler Kriss Rokkan Iversen trakk også frem at han var både «by og land». Konfliktlinjen sentrum-periferi preger også MDG. Selv om Haug er fra Oslo, blir han ansett som en slags distriktenes mann i partiet, i motsetning til Hermstad. Mindre synlighet, mer introspeksjon. Haug selv snakket om en «ny kurs». Men det er ikke noen stor politisk forskjell mellom Hermstad og Haug. Begge vil bredde ut partiet slik at det oppfattes som mer enn rent miljøparti. Haug har derimot betonet behovet for å bygge organisasjon og skue innover, om nødvendig på bekostning av synlighet i mediene. Mens Hermstad har vært krystallklar på at MDG skal søke regjeringsmakt ved neste anledning, har Haug vært mer skeptisk."
test_string = "高马二溪自然环境优越，所产茶叶，自古享有“天生好原料”的美誉。明·洪武24年（1391年），被定为贡茶。清嘉庆年间，第一支千两茶采用高马二溪原料于边江村踩制。清道光四年（1824年），高马二溪立“奉上严禁”碑，钦定为皇家茶园。1953年，毛主席亲点湖南省委筹备两百担高马二溪优质安化黑茶作为国礼赠送前苏联友人。高马二溪是具有代表性的高品质安化黑茶品牌，是高端优质黑茶的代名词"


program(test_string, 0.8, "CN")
#get_freq_list_table("NO")
