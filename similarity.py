#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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