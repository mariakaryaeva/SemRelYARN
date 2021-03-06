#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pymorphy2

# поиск очишенных по частотности пар из Викисловаря
# результат: файл, около 10 тыс слов, "золотой стандарт": wikionary_clear_60k_freq.txt
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

    # "золотой" стандарт: проверяем и род, и вид на соотвествтие в Викшинари
    out_file = open("wikionary_clear_60k_freq.txt", "w")
    for line in wictionary_file:
        word1 = re.split("#",line)[0].lower()
        word2 = re.sub("\n", "", re.split("#", line)[1].lower())
        if word1 in freq_list and word2 in freq_list:
            out_file.write(line)
    out_file.close()

    # расширение: проверяем только род на соотвествтие в Викшинари
    out_r_file = open("wikionary_clear_60k_rod_freq.txt", "w")
    for line in wictionary_file:
        word1 = re.split("#",line)[0].lower()
        word2 = re.sub("\n", "", re.split("#", line)[1].lower())
        if word1 in freq_list and word1!="имя":
            out_r_file.write(line)
    out_r_file.close()



def getstr(list):
    if len(list)==1:
        return list[0]
    else:
        return ' '.join(list)



# берем словари
# для каждой пары из викшинари находим "вид-род" в главном слове и определении.
# Выдаем пару и позицию (по словам) рода в определении
def getWikionaryPairsFromDicts():
    wictionary_file = open("wikionary_clear_60k_freq.txt", "r")  # "золотой" стандарт

    morph = pymorphy2.MorphAnalyzer()

    wiki_list = []

    for line in wictionary_file:
        line = re.sub("\n", "", line)  # "РОД#ВИД"

        rod = re.split("#", line)[0]
        rod = re.split(" ", rod)
        for idx, item in enumerate(rod):
            item = morph.parse(item)[0]
            rod[idx] = item.normal_form

        vid = re.split("#", line)[1]
        vid = re.split(" ", vid)
        for idx, item in enumerate(vid):
            item = morph.parse(item)[0]
            vid[idx] = item.normal_form

        wiki_list.append([getstr(rod), getstr(vid)])


    # indict = ["UF_babenko_v3", "UF_bts_final", "UF_mas_final_latest", "UF_ozhshv_final", "UF_efremova_v2", "UF_ushakov_final"]
    indict = ["UF_babenko_v3", "UF_bts_final_latest", "UF_mas_final_latest", "UF_ozhshv_final_latest", "UF_efremova_v2_latest",
              "UF_ushakov_final_latest"]

    outfpair = ["Wikionary_freq_pairs_pos_in_dict_babenko_v3", "Wikionary_freq_pairs_pos_in_dict_bts_final","Wikionary_freq_pairs_pos_in_dict_mas_final", "Wikionary_freq_pairs_pos_in_dict_ozhshv_final","Wikionary_freq_pairs_pos_in_dict_efremova_v2","Wikionary_freq_pairs_pos_in_dict_ushakov_final"]

    if len(indict)==len(outfpair):
        count = len(indict)


    for idx, val in enumerate(indict):
        d1 = open(val+".txt", "r")
        out_file = open(outfpair[idx]+".txt", "w")
        pair_list = []
        total_pairs = 0

        for line in d1:

            if re.search(" - ", line)!=None:
                main_word = re.split(" - ",line)[0]

                definition = re.split(" - ", line)[1]
                def_words = re.findall(r'[а-яА-Я]+', definition)

                for idx, word in enumerate(def_words):
                    word = morph.parse(word)[0]
                    def_words[idx] = word.normal_form


                for pair in wiki_list:

                    if pair[0] in def_words and pair[1] == main_word:
                        if [pair[1],pair[0]] in pair_list:
                            print("уже в списке: "+ pair[1]+","+pair[0])
                        else:
                            pair_list.append([pair[1],pair[0]])
                            position = (def_words.index(pair[0])+1)
                            out_file.write(position.__str__()+"\t"+pair[1]+","+pair[0]+"\n")
                            total_pairs = total_pairs + 1

        print(val)
        print(total_pairs)

# getWikionaryPairsFromDicts()
# 15.11.2017



# количество определений на один термин по всем словарям
def countDefPerTerms():
    indict = ["UF_babenko_v3", "UF_bts_final_latest", "UF_mas_final_latest",  "UF_efremova_v2_latest", "UF_ushakov_final_latest", "UF_ozhshv_final_latest"]
    # "UF_ozhshv_final",
    outf = open("countDef_ALL_dict.txt", "w")
    ouftdata = open("Def_ALL_dict.txt", "w")

    TDstore = {}

    for dict in indict:
        inf = open(dict+".txt", "r")
        print(dict+".txt")


        for line in inf:
            if re.split(" - ", line)!=None and len(re.split(" - ", line))>1:
                term = re.split(" - ", line)[0]
                term = re.sub(" ", "", term)
               # print(line)
                definition = re.split(" - ", line)[1]

                if re.search("\",\"", term) != None:
                    term_spelling = re.split("\",\"", term)

                    for t in term_spelling:
                        if t in TDstore:
                            def_list = TDstore.get(t)
                            def_list.append(definition)
                            TDstore[t] = def_list
                        else:
                            TDstore[t] = [definition]
                else:
                    if term in TDstore:
                        def_list = TDstore.get(term)
                        def_list.append(definition)
                        TDstore[term] = def_list

                    else:
                        TDstore[term] = [definition]

    for key, value in TDstore.items():
        outf.write(key+"\t"+len(value).__str__()+"\n")
        ouftdata.write(key+"\t"+len(value).__str__()+"\n")
        for defin in value:
            defin = re.sub("\n", "", defin)
            ouftdata.write(key + " - " + defin+ "\n")



countDefPerTerms()

# в ожегове определения смыслов одного слова перечислены в одном определении.
# экстаз - 1. Исступленно-восторженное состояние  Прийти в э. Говорить что-н. в экстазе. 2. Вид аффективного психического расстройства  П прил. экстатический,  Экстатическая музыка.
def divideDefinitionInDict():
    inf = open("UF_ozhshv_final.txt", "r")
    outf = open("UF_ozhshv_final_latest.txt", "w")

    for line in inf:
        search = re.search('[А-Яа-я]*( )-', line)
        if search != None and search.span()[0] == 0:
            line = re.sub("\n", "", line)
            term = re.sub(" -", "", search.group())
            definition = line[search.span()[1]:]

            def_list = re.split('\d[.]', definition)
            for defin in def_list:
                if defin == "" or defin == " " or (re.search(" ",defin)!=None and len(defin)<3):
                    print(defin)
                else:
                    outf.write(term + " - " + defin + "\n")

        else:
            outf.write(line)


# divideDefinitionInDict()



def divideDefinitionInDictMAS():
    inf = open("UF_mas_final.txt", "r")
    outf = open("UF_mas_final_latest.txt", "w")


    for line in inf:
        line = re.sub("\n", "", line)
        term = re.split(" - ", line)[0]
        common_def = re.split(" - ", line)[1]

        if re.search("\",\"", term)!=None:
            terms_list = re.split("\",\"", term)
            for t in terms_list:
                if re.search("\.\",\"", common_def)!=None:
                    def_list  = re.split("\.\",\"", common_def)
                    for definition in def_list:
                        outf.write(t + " - " + definition+"\n")
                else:
                    outf.write(t + " - "+ common_def + "\n")
        else:
            if re.search("\.\",\"", common_def) != None:
                def_list = re.split("\.\",\"", common_def)
                for definition in def_list:
                    outf.write(term + " - " + definition + "\n")
            else:
                outf.write(line + "\n")



# divideDefinitionInDictMAS()


def divideDefinitionInDictUSH():
    inf = open("UF_ushakov_final.txt", "r")
    outf = open("UF_ushakov_final_latest.txt", "w")


    for line in inf:
        line = re.sub("\n", "", line)
        term = re.split(" - ", line)[0]
        common_def = re.split(" - ", line)[1]

        if re.search("\",\"", term)!=None:
            terms_list = re.split("\",\"", term)
            for t in terms_list:
                if re.search("\.\",\"", common_def)!=None:
                    def_list  = re.split("\.\",\"", common_def)
                    for definition in def_list:
                        outf.write(t + " - " + definition+"\n")
                else:
                    outf.write(t + " - "+ common_def + "\n")
        else:
            if re.search("\.\",\"", common_def) != None:
                def_list = re.split("\.\",\"", common_def)
                for definition in def_list:
                    outf.write(term + " - " + definition + "\n")
            else:
                outf.write(line + "\n")

# divideDefinitionInDictUSH()






def divideDefinitionInDictEFR():
    inf = open("UF_efremova_v2.txt", "r")
    outf = open("UF_efremova_v2_latest.txt", "w")


    for line in inf:
        line = re.sub("\n", "", line)
        term = re.split(" - ", line)[0]
        common_def = re.split(" - ", line)[1]

        if re.search("\",\"", term)!=None:
            terms_list = re.split("\",\"", term)
            for t in terms_list:
                if re.search("\.\",\"", common_def)!=None:
                    def_list  = re.split("\.\",\"", common_def)
                    for definition in def_list:
                        outf.write(t + " - " + definition+"\n")
                else:
                    outf.write(t + " - "+ common_def + "\n")
        else:
            if re.search("\.\",\"", common_def) != None:
                def_list = re.split("\.\",\"", common_def)
                for definition in def_list:
                    outf.write(term + " - " + definition + "\n")
            else:
                outf.write(line + "\n")


# divideDefinitionInDictEFR()






def divideDefinitionInDictBTS():
    inf = open("UF_bts_final.txt", "r")
    outf = open("UF_bts_final_latest.txt", "w")


    for line in inf:
        line = re.sub("\n", "", line)
        term = re.split(" - ", line)[0]
        common_def = re.split(" - ", line)[1]

        if re.search("\",\"", term)!=None:
            terms_list = re.split("\",\"", term)
            for t in terms_list:
                if re.search("\.\",\"", common_def)!=None:
                    def_list  = re.split("\.\",\"", common_def)
                    for definition in def_list:
                        outf.write(t + " - " + definition+"\n")
                else:
                    outf.write(t + " - "+ common_def + "\n")
        else:
            if re.search("\.\",\"", common_def) != None:
                def_list = re.split("\.\",\"", common_def)
                for definition in def_list:
                    outf.write(term + " - " + definition + "\n")
            else:
                outf.write(line + "\n")


# divideDefinitionInDictBTS()