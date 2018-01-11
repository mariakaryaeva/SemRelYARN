#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
# проверка: сколько существительных в 60 тыс частотных слов (из рейтинга НКРЯ)
# результат: 33 022 существительных из золотого стандарта (60 тыс)

# inf = open("1grams_nkrya_norm.txt", "r")
# outf = open("1grams_nkrya_norm_60k_nouns.txt", "w")
# count = 0
# for line in inf:
#     if count <=60000:
#         count = count + 1
#         word = re.split("\t", line)[0]
#         p = morph.parse(word)[0]
#         if p.tag.POS  == "NOUN":
#             outf.write(line)


# сколько уникальных терминов (только существительных) во всех словарях в качестве термина
# результат: 62 915 - термины существительные

# inf = open("/Users/maria/PycharmProjects/SemRelYARN/countDef_ALL_dict.txt", "r")
# outf = open("countDef_ALL_dict_nouns.txt", "w")
#
# for line in inf:
#     word = re.split("\t", line)[0]
#     p = morph.parse(word)[0]
#     if p.tag.POS  == "NOUN":
#         outf.write(line)


# пересекаем уникальные термины из всех словарей с золотым стандартом по частотности (60 тыс).
# результат: 22 356 уникальных терминов

# inf = open("/Users/maria/PycharmProjects/SemRelYARN/countDef_ALL_dict.txt", "r")
# inf_gs = open("1grams_nkrya_norm_standart_60k.txt", "r")
# outf = open("countDef_ALL_dict_standart_60k.txt", "w")
# outf_lack = open("countDef_ALL_dict_no_in_st_60k.txt", "w")
#
# gs_list = []
# for line in inf_gs:
#     word_gs = re.split("\t", line)[0]
#     gs_list.append(word_gs)
#
# for line in inf:
#     word = re.split("\t", line)[0]
#     if word in gs_list:
#         outf.write(line)
#     else:
#         outf_lack.write(line)



# составляем файл с ОПРЕДЕЛЕНИЯМИ для 22 356 уникальных терминов (см. пред. этап)

# inf_gs = open("countDef_ALL_dict_standart_60k.txt", "r")
# inf = open("/Users/maria/PycharmProjects/SemRelYARN/Def_ALL_dict.txt", "r")
# outf = open("Def_ALL_dict_standart_60k.txt", "w")
#
# gs_list = []
# for line in inf_gs:
#     word_gs = re.split("\t", line)[0]
#     gs_list.append(word_gs)
#
# inf_rd = inf.readlines()
#
# for idx, line in enumerate(inf_rd):
#
#     if re.search(" - ", line) == None:
#         word = re.split("\t", line)[0]
#         count_next_lines = int(re.sub("\n","",re.split("\t", line)[1]))
#
#         if word in gs_list:
#             i_line = 0
#             while i_line <= count_next_lines:
#                 outf.write(inf_rd[idx+i_line])
#                 i_line = i_line + 1






# удаляем повторящиющиеся опредления
#
# inf = open("Def_ALL_dict_standart_60k.txt", "r")
# outf = open("Def_ALL_dict_standart_60k_no_dubl_clean.txt", "w")
#
# #  файл как есть со знаками препинания и заглавными буквами:  Def_ALL_dict_standart_60k_no_dubl
# #  файл очищенный, слова приведены к нижнему регистру: Def_ALL_dict_standart_60k_no_dubl_clean
#
# inf_rd = inf.readlines()
#
# for idx, line in enumerate(inf_rd):
#
#     if re.search(" - ", line) == None:
#         word = re.split("\t", line)[0]
#         count_next_lines = int(re.sub("\n","",re.split("\t", line)[1]))
#
#         i_line = 1
#         def_list = [] # собираем определения для каждого термина
#         while i_line <= count_next_lines:
#             candidate = (re.sub("ё","е", inf_rd[idx+i_line])).lower()
#             definition = re.split(" - ", candidate)[1]
#             def_words = re.findall(r'[а-я]+', definition)
#
#             def_list.append(" ".join(def_words))
#             i_line = i_line + 1
#
#         def_list = list(set(def_list)) # удалили дубликаты
#
#         outf.write(word + "\t"+len(def_list).__str__()+"\n")
#         for definition in def_list:
#             outf.write(word + " - "+ definition+"\n")



# # подготовка файла с термин - опредлениями для извлечения рода методом Юры
# # убираем строки "термин и его количество"
# inf = open("Def_ALL_dict_standart_60k_no_dubl_clean.txt", "r")
# outf = open("Def_ALL_dict_standart_60k_no_dubl_clean_for_mystem.txt", "w")
# count = 0
# for line in inf:
#     if re.search(" - ", line)!=None:
#         outf.write(line)
#     if re.search("\t", line)!=None:
#         count = count+1
#
# print(count)


# # в файле расставляем нумерацию строк, пропуская строки где "термин - количество ниже строк с определениями этого термина"
# inf = open("Def_ALL_dict_standart_60k_no_dubl_clean.txt", "r")
# outf = open("Def_ALL_dict_standart_60k_no_dubl_clean_num.txt", "w")
#
# count_t = 0
# for idx, line in enumerate(inf):
#     if re.search(" - ", line) != None:
#         outf.write((idx+1-count_t).__str__()+"\t"+line)
#     else:
#         count_t = count_t + 1
#         outf.write(line)



# совместить файл для построения графов и шаблоны
inf = open("Def_ALL_dict_standart_60k_no_dubl_clean_num.txt", "r")
outf = open("Def_ALL_dict_standart_60k_no_dubl_clean_num_up.txt", "w")
inf_1 = open("total_1_word.txt", "r")
inf_2 = open("multi_words_AN.txt","r")
inf_3 = open("multi_words_NN.txt","r")
inf_4 = open("multi_word_mixed_.txt","r")
file_lst = [inf_1,inf_2,inf_3,inf_4]

dict = {}
for f in file_lst:
    for line in f:
        num = re.split("\t",line)[0]
        other = re.split(" - ", re.sub("\n", "", re.split("\t",line)[1]))[1]
        # оппортунизм - политика приспособления {политика}

        lst = []

        if num in dict:
            lst = dict[num]
            lst.append(other)
        else:
            lst.append(other)
            dict[num] = lst


for line in inf:
    if re.search(" - ", line)!=None:
        c_num = re.split("\t", line)[0]

        if c_num in dict:
            new_str_num = c_num + "\t" + "|".join(dict[c_num]) + " = "
            line = re.sub(c_num, new_str_num, line)
    outf.write(line)





