#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Для определения близости определений

import sys
import re
import networkx as nx
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


# pos=nx.spring_layout(G) # positions for all nodes


# inf = open("/Users/maria/PycharmProjects/SemRelYARN/Def_ALL_dict.txt", "r")
# outf = open("/Users/maria/PycharmProjects/SemRelYARN/cosine_sim_defs.txt", "w")
inf = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/Def_ALL_dict_standart_60k_no_dubl_clean.txt", "r")
outf = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/simMeas_Def_dicts_gs_60k_clean.txt", "w")

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

lab = {}
for key, value in dict.items():
    G = nx.Graph()
    if key!="":
        for idx, defX in enumerate(value):
            lab[idx] = defX
            G.add_node(idx)
            for idy, defY in enumerate(value):
                if idy != idx:
                    x_clean_def = re.findall("([а-яА-Я]+)", defX)
                    defX_clean =' '.join(x_clean_def)
                    y_clean_def = re.findall("([а-яА-Я]+)", defY)
                    defY_clean = ' '.join(y_clean_def)
                    f = simfunctions.cosine(tokenizers.whitespace(defX_clean), tokenizers.whitespace(defY_clean))

                    if f >= 0.25 and f != 1.0:
                        # outf(round(f, 2).__str__() + "\t" + defX_clean +"\t" + defY_clean + "\n")
                        G.add_edge(idx, idy, weight=round(f, 2))



    nx.set_node_attributes(G, lab, 'labels')
    # nx.draw(G, labels = lab,font_size=9)

    #  [{15, 2, 19, 20, 7}, {10, 3, 12, 13}, {8, 17, 4, 22}, {0, 16, 1}, {9, 6, 14}, {18, 11, 21}, {5}, {23}]
    components = sorted(nx.connected_components(G), key = len, reverse=True)
    outf.write("-- "+key+"\n")
    for id, comp in enumerate(components):

        if len(comp)!=1:
            for num in comp:
                outf.write(id.__str__()+"."+num.__str__()+"\t"+G.node[num]['labels'])

            outf.write("\n")
        else:
            for num in comp:
                outf.write("*\t"+G.node[num]['labels'])



#  рисовалка графа
# plt.axis('off')
# plt.savefig("labels_and_colors.png") # save as png
# plt.show() # display


