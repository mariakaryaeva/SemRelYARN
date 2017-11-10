#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pymorphy2

def clear_wikionary_by_freq_list():
    freq_file = open("1grams_nkrya_norm.txt", "r")
    freq_list = []
    freq = freq_file.readlines()

    count = 0
    while(count< 60000):
        line = freq[count]
        freq_list.append(re.split("\t",line)[0])
        count = count + 1


    wictionary_file = open("wikionary_hypernyms.txt", "r")

    out_file = open("wikionary_clear_60k_freq.txt", "w")
    for line in wictionary_file:
        word1 = re.split("#",line)[0].lower()
        word2 = re.sub("\n", "", re.split("#", line)[1].lower())
        if word1 in freq_list and word2 in freq_list:
            out_file.write(line)
    out_file.close()

    out_r_file = open("wikionary_clear_60k_rod_freq.txt", "w")
    for line in wictionary_file:
        word1 = re.split("#",line)[0].lower()
        word2 = re.sub("\n", "", re.split("#", line)[1].lower())
        if word1 in freq_list and word1!="имя":
            out_r_file.write(line)
    out_r_file.close()

# берем словари
# для каждой пары из викшинари находим "вид-род" в определении.
# Выдаем пару и позицию (по словам) рода в определении

def getstr(list):
    if len(list)==1:
        return list[0]
    else:
        return ' '.join(list)




def getsim():
    d1 = open("UF_efremova_v2_40_out.txt", "r")
    out_file = open("wikionary_freq_pairs_pos_in_dict_efremova.txt", "w")
    wictionary_file = open("wikionary_clear_60k_rod_freq.txt", "r")

    morph = pymorphy2.MorphAnalyzer()

    wiki_list = []

    for line in wictionary_file:
        line = re.sub("\n", "", line) # "РОД#ВИД"

        rod = re.split("#",line)[0]
        rod = re.split(" ",rod)
        for idx, item in enumerate(rod):
            item = morph.parse(item)[0]
            rod[idx] = item.normal_form

        vid = re.split("#",line)[1]
        vid = re.split(" ",vid)
        for idx, item in enumerate(vid):
            item = morph.parse(item)[0]
            vid[idx] = item.normal_form


        wiki_list.append([getstr(rod),getstr(vid)])


    for line in d1:


        if re.search(" - ", line)!=None:
            main_word = re.split(" - ",line)[0]
            # main_word = (morph.parse(main_word)[0])
            # main_word = main_word.normal_form
            # print(main_word)

            definition = re.split(" - ", line)[1]
            def_words = re.findall(r'[а-яА-Я]+', definition)

            for idx, word in enumerate(def_words):
                word = morph.parse(word)[0]
                def_words[idx] = word.normal_form


            for pair in wiki_list:

                if pair[0] in def_words and pair[1] == main_word:
                #     print(pair[0] + " *in* " + getstr(def_words))
                #     print(pair[1] + " == " + main_word)
                #     print(pair)
                    position = (def_words.index(pair[0])+1)
                    print(main_word + " = " + definition)
                    out_file.write(position.__str__()+"\t"+pair[1]+","+pair[0]+"\n")

getsim()

# morph = pymorphy2.MorphAnalyzer()
# for idx, item in enumerate(main_word):
#     word = (morph.parse(item)[0])
#     main_word[idx] = word.normal_form
# print(main_word)
# print(' '.join(main_word))
#
# if ' '.join(l) in ' '.join(main_word):
#     print(l)
#
