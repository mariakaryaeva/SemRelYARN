#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Программа извлечения родо-видовых отношений между
# существительными из словарных определений
import sys
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


# блок констант
UTF8 = 'utf-8'
mark_words = ["женск", "ласк",
    "уменьш"]
intro_beg = ["в", "во", "на",
    "по", "у"]
kind_of_words = ["род", "вид",
    "разновидность", "тип",
    "форма", "сорт"]
kind_after_name_words = ["семейство", "подкласс",
    "отряд", "ряд", "класс"]
general_beg = ["то", "что", "кто"]
false_nouns = ["-л", "др"]

class TWord:
    form = ""
    lemma = ""
    def __init__(self, Form = "", Lemma = ""):
        self.form = Form
        self.lemma = Lemma
    def is_empty(self):
        return not self.form
    def to_string(self):
        return (self.lemma + " {" + self.form + "}")

# чистит строку от грамм. информации, добавленной через mystem
def get_plain_text(line):
    res = ""
    in_curly_bracket = False
    for c in line:
        if c == '{':
            in_curly_bracket = True
        elif c == '}':
            in_curly_bracket = False
        elif not in_curly_bracket:
            res = res + c
    return res

# выделяет заголовочное слово и определение
def get_head_word_and_def(line):
    pos = line.find(" - ")
    if pos == -1:
        return ""
    word = get_plain_text(line[:pos])
    definition = line[pos + 3:]
    return word, definition

# частью слова могут быть буквы и дефис
def is_part_of_word(c):
    return c.isalpha() or c == '-'

# получает первое слово из line, следующее за позицией pos
def get_next_word_lower(line, pos):
    while pos < len(line) and (not is_part_of_word(line[pos])):
        pos = pos + 1
    res = ""
    while pos < len(line) and is_part_of_word(line[pos]):
        res = res + line[pos]
        pos = pos + 1
    pos = line.find("}", pos)
    if pos == -1:
        pos = len(line)
    res = res.lower()
    return res, pos

# определено ли слово через синоним
def is_syn_def(definition):
    pos = 0
    w1, pos = get_next_word_lower(definition, pos)
    if w1 == "см":
        return True
    w2, pos = get_next_word_lower(definition, pos)
    if not w2: # одно слово в определении означает, что это синоним
        return True
    w3, pos = get_next_word_lower(definition, pos)
    return w1 == "то" and w2 == "же" \
            and w3 == "что"

# явлется ли определение отсылочным
def is_ref_def(definition):
    pos = 0
    w1, pos = get_next_word_lower(definition, pos)
    w2, pos = get_next_word_lower(definition, pos)
    if (w1 == "действие" \
            or w1 == "свойство" \
            or w1 == "состояние") \
            and w2 == "по":
        return True
    w3, pos = get_next_word_lower(definition, pos)
    if (w1 == "действие" \
            or w1 == "свойство") \
            and w2 == "и" \
            and w3 == "состояние":
        return True
    return False

# содержится ли в определении описание "человека"
def is_person(definition):
    pos = 0
    w1, pos = get_next_word_lower(definition, pos)
    w2, pos = get_next_word_lower(definition, pos)
    return w1 == "тот" and w2 == "кто"

# содержит ли определение вводную часть
def has_intro_part(definition):
    if definition.find(":") == -1:
        return False
    w1, pos = get_next_word_lower(definition, 0)
    return w1 in intro_beg

# является ли лемма словом из списка "род", "вид" и т.п.
def is_kind_of_word(lower_lemma):
    return lower_lemma in kind_of_words

# является ли лемма словом из списка "отряд", "класс" и т.п.
def is_kind_after_name_words(lower_lemma):
    return lower_lemma in kind_after_name_words

# является ли определение очень "общим", из к-ого нельзя извлечь род
def is_general_def(hyponym):
    return hyponym.lemma in general_beg

# начинается ли определение со словарной пометы
def def_has_mark(definition, pos):
    w, pos = get_next_word_lower(definition, pos)
    return w in mark_words

# печатает родо-видовую пару
def print_pair(hypernym, hyponym):
    print('\t{0} - {1}'.format(hypernym, hyponym.to_string()))

# печатает определение, возможно обрезанное
def print_def(origin_line):
    origin_line = get_plain_text(origin_line)
    cut_line = origin_line[0:80]
    sys.stdout.write(cut_line)
    if origin_line != cut_line:
        sys.stdout.write('...')
    sys.stdout.write('\n')

# печатает определение и сформированные пары
def print_def_and_pairs(hypernym, hyponym, hyponym2, origin_line):
    if (not hyponym.is_empty()):
        print_def(origin_line)
        print_pair(hypernym, hyponym)
        if not hyponym2.is_empty():
            print_pair(hypernym, hyponym2)

# получает лемму из грамм. информации
def get_lemma(grammar_info):
    if not grammar_info:
        return ""
    w = grammar_info[0]
    pos = w.find("=")
    if pos == -1:
        return ""
    res = w[0:pos]
    while res and res.endswith('?'):
        res = res[:-1]
    return res

# получает грамм. информацию о слове после fn
def get_grammar(definition, fn):
    st = fn + 1
    while fn < len(definition) and definition[fn] != '}':
        fn = fn + 1
    return definition[st:fn].split("|"), fn

# относится ли грамм. информация к существительному
def is_noun(gr):
    return gr.find("=S") != -1

# относится ли грамм. информация к им. падежу
def is_nomin_case(gr):
    return gr.find("им") != -1

# получает часть речи и падеж (для существительного)
def get_noun_and_case(grammar_info, lower_form, lower_lemma):
    noun = False
    nomin_case = False
    for gi in grammar_info:
        if (is_noun(gi)):
            noun = True
            nomin_case = is_nomin_case(gi)
    nomin_case = nomin_case or (noun and lower_form == lower_lemma)
    return noun, nomin_case

# проверяет явлется ли лемма "ложным" существительным
def is_false_noun(lower_form):
    return lower_form in false_nouns

# основная функция программы
if __name__ == "__main__":
    add = ""
    inf = open("dict-mystem.txt", "r")
    outf = open(add+"total_1_word.txt","w")
    outf_err = open(add+"no_relation.txt","w")
    multi_outf = open("multi_word_mixed_.txt", "w")
    #multi_outf_err = open(add+"multi_res_err.txt", "w")
    multi_outf_attr_err = open(add+"multi_res_attr_err.txt", "w")
    for line in inf:
        if line !="":
            origin_line = line[0:-1] # удаляем перенос строки
            origin_line = origin_line
            #print(origin_line)
           # print(line)
            hypernym, definition = get_head_word_and_def(origin_line)
            if not hypernym: # неизвестное форматирование словарной статьи
                continue
            if is_syn_def(definition): # проблемный случай № 1 - опред. ч-з син.
                continue
            if is_ref_def(definition): # проблемный случай № 3 - отсыл. опред.
                continue
            if is_person(definition):
                print_def_and_pairs(hypernym, TWord("человек",
                        "человек"), TWord(), origin_line)
                continue

            st = fn = 0
            if has_intro_part(definition): # проблемный случай № 5
                fn = st = definition.find(":") + 1
            # проблемный случай № 2 - опред. с пометой
            if def_has_mark(definition, st):
                continue

            hyponym = hyponym2 = TWord()
            name = False
            while fn < len(definition):
                if is_part_of_word(definition[fn]):
                    fn = fn + 1
                elif definition[fn] == '{':
                    form = definition[st:fn]
                    lower_form = form.lower()

                    # проблемный случай № 4 - "меронимическое" определение
                    if (not hyponym.lemma) and \
                            lower_form == "часть":
                        break

                    grammar_info, fn = get_grammar(definition, fn)
                    lemma = get_lemma(grammar_info)
                    fn = fn + 1
                    st = fn

                    lower_lemma = lemma.lower()
                    # проблемный случай № 6 - род/вид чего-л.
                    if is_kind_of_word(lower_lemma):
                        continue
                    # проблемный случай № 7 - название чего-л.
                    if lower_form == "название":
                        name = True
                        continue
                    else:
                        if name and is_kind_after_name_words(lower_lemma):
                            continue

                    # пропускаем фрагменты, к-ые могут восприниматься как…
                    # … существительные в mystem
                    if len(lower_form) < 2 or is_false_noun(lower_form):
                        continue

                    noun, nomin_case = get_noun_and_case(grammar_info,
                            lower_form, lower_lemma)
                    if noun:
                        if hyponym.is_empty():
                            hyponym = TWord(form, lemma) # 1-ый кандидат
                            if nomin_case: # кандидат в им. падеже
                                break
                        elif nomin_case:
                            hyponym2 = TWord(form, lemma) # 2-ой кандидат
                    # из подобного определения род не извлечь
                    if is_general_def(hyponym):
                        #outf_err.write(hypernym+"\n")
                        hyponym = hyponym2 = TWord() # очищаем результат
                        break
                    # может выступать в роли сущ., но точно не является родом
                    if is_general_def(hyponym2):
                        hyponym2 = TWord()
                        continue
                    if not (hyponym.is_empty() or hyponym2.is_empty()):
                        break # найдены оба кандидата
                else:
                    fn = fn + 1
                    st = fn
        #print_def_and_pairs(hypernym, hyponym, hyponym2, origin_line)

        def_lst = re.split(" ", definition)
        # print(def_lst)
        count = 0
        first_a = second_a = ""

        for word in def_lst:
            if re.search(hyponym.form, word) != None and hyponym.form!="":
                s = ""
                # сущ предлог сущ = Прибор для вычисления
                if (count + 2)<len(def_lst):
                    f_w = def_lst[count + 1]
                    s_w = def_lst[count + 2]
                    # сущ <предлог сущ> = Прибор для вычисления
                    if re.search("=PR=", f_w) != None and re.search("род", s_w) != None and re.search("S", s_w) != None:
                        f_w = re.split("\{", def_lst[count + 1])[0]
                        s_w = re.split("\{", def_lst[count + 2])[0]
                        multi_outf.write(hypernym + " - " + hyponym.form + " " + f_w + " " + s_w +" {" + hyponym.form + "} \t type:NPN\n")

                    # сущ <прил сущ> = Атака неприятельского судна
                    if re.search("=A=род,", f_w) != None and re.search("род", s_w) != None and re.search("S", s_w) != None:
                        f_w = re.split("\{", def_lst[count + 1])[0]
                        s_w = re.split("\{", def_lst[count + 2])[0]
                        multi_outf.write(hypernym + " - " + hyponym.form + " " + f_w + " " + s_w +" {" + hyponym.form + "} \t type:NAN\n")


                    # сущ <сущ прил> = растение семейства лилейных
                    if re.search("род", f_w) != None and re.search("S", f_w) != None and re.search("=A=род,", s_w) != None:
                        f_w = re.split("\{", def_lst[count + 1])[0]
                        s_w = re.split("\{", def_lst[count + 2])[0]
                        if (count + 3)<len(def_lst):
                            #добавлем еще одно существительное NNAN:
                            th_w = re.split("\{", def_lst[count + 3])[0]
                            if re.search("S", def_lst[count + 3]) != None and re.search("род,", def_lst[count + 3]) != None:
                                multi_outf.write(
                                    hypernym + " - " + hyponym.form + " " + f_w + " " + s_w + " " + th_w + " {" + hyponym.form + "} \t type:NNAN \n")
                            else:
                                multi_outf.write(hypernym + " - " + hyponym.form + " " + f_w + " " + s_w +" {" + hyponym.form + "} \t type:NNA \n")
                        else:
                            multi_outf.write(
                                hypernym + " - " + hyponym.form + " " + f_w + " " + s_w + " {" + hyponym.form + "} \t type:NNA \n")

                if (count -2) > 0:
                    p_w = def_lst[count - 1]
                    pp_w = def_lst[count - 2]

                    # <прил прил> сущ = Острое заразное заболевание
                    if re.search("=A=", p_w) != None and re.search("=A=", pp_w) != None:
                        pp_w = re.split("\{", def_lst[count - 2])[0]
                        p_w = re.split("\{", def_lst[count - 1])[0]
                        multi_outf.write(hypernym + " - " + pp_w + " " + p_w + " " + hyponym.form + " {" + hyponym.form + "} \t type:AAN \n")
                        # print(hypernym + " - " + p_w + " " + pp_w + " " + hyponym.form + " {" + hyponym.form + "} \t type:AAN \n")




                if (count - 1) > 0 and (count + 1)<len(def_lst):
                    # <прил> сущ <сущ> = Горизонтальный отрезок линии
                    p_w = def_lst[count - 1]
                    f_w = def_lst[count + 1]
                    if re.search("=A=", p_w) != None and re.search("род", f_w) != None and re.search("S", f_w) != None:
                        f_w = re.split("\{", def_lst[count + 1])[0]
                        p_w = re.split("\{", def_lst[count - 1])[0]
                        multi_outf.write(hypernym + " - " + p_w + " " + hyponym.form + " " + f_w + " {" + hyponym.form + "} \t type:ANN \n")
                        print(hypernym + " - " + p_w + " " + hyponym.form + " " + f_w + " {" + hyponym.form + "} \t type:ANN \n")
                break




            count = count + 1


        if first_a != "" and hyponym.form != "":
            hyponym_gr = morph.parse(hyponym.form)[0]
            first_a_tmp = morph.parse(first_a)[0]
            # print(first_a_tmp)
            first_a_gr = morph.parse(first_a_tmp.normal_form)[0]

            multi_outf.write(hypernym + " - " + hyponym.form + " " + first_a + " {" + hyponym.form +"}\n")
            print(hypernym + " - " + first_a  + " " + hyponym.to_string() )

