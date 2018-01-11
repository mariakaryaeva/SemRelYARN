
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import collections

# работаем со следующей конструкцией:
# ========================================
# -- 	чугунка
# 0.0	49673	печка {печка}|чугунная печка {печка} = чугунная печка
# 0.3	49677	печка {печка}|чугунная печка {печка} = чугунная печка разг раскалить чугунку
# 0.5	49679	печка {печка}|чугунная печка {печка} = чугунная печка разг
#
# 1.4	49678	дорога {дорога}|железная дорога {дорога} = железная дорога с рельсами из чугуна
# 1.6	49680	дорога {дорога}|железная дорога {дорога}|дорога простореч {дорога} = железная дорога простореч устар
# 1.7	49681	дорога {дорога}|железная дорога {дорога} = железная дорога устар прост ехать по чугунке
#
# *	49674	горшок {горшок}|чугунный горшок {горшок} = чугунный горшок то же что чугун во знач простореч
# *	49676	дорога {дороги}|чжелезная дорога {дороги} = название чжелезной дороги
# ========================================

# список терминов, у которых вообще не нашлось пары из словарей
def list_no_pairs_terms():
    inf = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/simMeas_Def_dicts_gs_60k_clean_up.txt", "r")
    outf = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/simMeas_Def_dicts_gs_60k_clean_up_pairs.txt", "w")
    outf_no_pair = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/simMeas_Def_dicts_gs_60k_clean_up_no_pairs.txt", "w")

    total_list = {}
    term = ""
    list_meanings = {}
    for idx, line in enumerate(inf):
        if re.search("-- ", line)!=None:
            if term!="":
                if len(list_meanings)>=1:
                    total_list[term] = list_meanings
                else:
                    outf_no_pair.write(term+"\n")


            term = re.sub("\n", "", re.split(" ", line)[1])
            list_meanings = {}
            sense = 0
        if re.search(" = ",line)!=None:
            defin = re.sub("\n","", re.split(" = ",line)[1])
            if len(re.split("\t",re.split(" = ",line)[0]))==3: # rod in definition
                rod = re.split("\t", re.split(" = ", line)[0])[2] # ['1.2', '118160', 'чихание {чихание}']
                # if re.search("\|", rod)!=None:
                #     rod_list = re.split("\|", rod)
                # else:
                #     rod_list = [rod]

                lst = []
                if sense in list_meanings:
                    lst = list_meanings[sense]
                    lst.append(rod)
                else:
                    lst.append(rod)
                    list_meanings[sense] = lst


        if line =="\n":
            sense=sense+1


    for term, value in total_list.items():
        for sense, rod_list in value.items():
            outf.write(term+" : "+';'.join(rod_list)+"\n")
        



# для каждого рода подбираем виды (для проверки, что у рода должно быть много видов)
def kind_of_vids():
    inf = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/simMeas_Def_dicts_gs_60k_clean_up_pairs.txt", "r")
    outf_1 = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/kind_of_specie_1.txt", "w")
    outf_2 = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/kind_of_species_2.txt", "w")
    outf_3 = open("/Users/maria/PycharmProjects/SemRelYARN/60_freq/kind_of_species_more_than_2.txt", "w")

    dict = {}
    for line in inf:
        term = re.split(" : ", line)[0]
        other = re.split(" : ", line)[1]
        list_rods = re.split("\|", other)
        for item in list_rods:
            rod = re.split(" {", item)[0]
            lst = []
            if rod in dict:
                lst = dict[rod]
            lst.append(term)
            dict[rod] = lst

    for rod, value in dict.items():
        value = list(set(value))
        if len(value)==1:
            outf_1.write(rod+" : "+";".join(value)+"\n")
        if len(value) == 2:
            outf_2.write(rod + " : " + ";".join(value)+"\n")
        if len(value) > 2:
            outf_3.write(rod + " : " + ";".join(value)+"\n")


# отранжируем пары по частоте НКРЯ
def range_spicie_NRKYA():
    outf = open("kind_of_species_nkrya_range.txt", "w")
    outf_no = open("kind_of_species_nkrya_range_no.txt", "w")

    nkrya = open("1grams_nkrya_norm.txt", "r")
    nkrya_dict = {}
    for line in nkrya:
        term = re.split("\t",line)[0]
        num = re.sub("\n", "", re.split("\t",line)[1])
        nkrya_dict[term] = num


    f_l = ["kind_of_specie_1", "kind_of_species_2", "kind_of_species_more_than_2"]

    dict = {}
    for f in f_l:
        inf = open(f+".txt", "r")

        for line in inf:
            rod = re.split(" : ", line)[0]
            if rod in nkrya_dict:
                num = nkrya_dict[rod]
                lst = {}
                if num in dict:
                    dict[num] = lst
                    tmp_key = 0
                    for key in lst:
                        if key > tmp_key:
                            tmp_key = key
                    tmp_key = tmp_key+1
                else:
                    tmp_key = 0


                lst[tmp_key] = line
                dict[num] = lst
            else:
                outf_no.write(line)

    od = collections.OrderedDict(sorted(dict.items()))
    for num, value in od.items():
        for key, line in value.items():
            outf.write(num+"\t"+line)

range_spicie_NRKYA()