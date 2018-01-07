#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Для определения близости определений

import sys
import re
from py_stringmatching import simfunctions, tokenizers
#
# y = "Короткая трубчатая кость пальцев кисти и стопы."
# y_list = re.findall("([а-яА-Я]+)", y)
#
# x = "У древних греков: сомкнутый строй пехоты."
# x_list = re.findall("([а-яА-Я]+)", x)
# # f = simfunctions.cosine(tokenizers.whitespace(x), tokenizers.whitespace(y))
#
# f = simfunctions.monge_elkan( y_list, x_list, sim_func=simfunctions.levenshtein)
# print(f)


inf = open("/Users/maria/PycharmProjects/SemRelYARN/Def_ALL_dict.txt", "r")
outf = open("/Users/maria/PycharmProjects/SemRelYARN/cosine_sim_defs.txt", "w")
dict = {}
for line in inf:
    if re.search("\t", line)==None:
        term = re.split(" - ",line)[0]
        defin = re.split(" - ",line)[1]
        lst = []

        if term in dict:
            lst = dict[term]
            lst.append(defin)
        else:
            lst.append(defin)
            dict[term] = lst

for key, value in dict.items():
    if key =="фаланга":
        outf.write("---------------\n")
        for idx, defX in enumerate(value):
            for idy, defY in enumerate(value):
                if idy>idx:
                    x_clean_def = re.findall("([а-яА-Я]+)", defX)
                    defX_clean =' '.join(x_clean_def)
                    y_clean_def = re.findall("([а-яА-Я]+)", defY)
                    defY_clean = ' '.join(y_clean_def)
                    f = simfunctions.cosine(tokenizers.whitespace(defX_clean), tokenizers.whitespace(defY_clean))
                    outf.write(round(f, 2).__str__() + "\t" + defX_clean +"\t" + defY_clean + "\n")



