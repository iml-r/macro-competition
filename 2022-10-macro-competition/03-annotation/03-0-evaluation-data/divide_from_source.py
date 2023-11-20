#!/usr/bin/env python3
# coding: utf-8


with open('original-source.txt', mode='r', encoding='U8') as input_file, \
     open('annotated-by-tool/eval-by-tool-cs.tsv', mode='w', encoding='U8') as cs_file, \
     open('annotated-by-tool/eval-by-tool-en.tsv', mode='w', encoding='U8') as en_file, \
     open('annotated-by-tool/eval-by-tool-de.tsv', mode='w', encoding='U8') as de_file, \
     open('annotated-by-tool/eval-by-tool-nl.tsv', mode='w', encoding='U8') as nl_file, \
     open('annotated-by-tool/eval-by-tool-ru.tsv', mode='w', encoding='U8') as ru_file, \
     open('annotated-by-tool/eval-by-tool-fr.tsv', mode='w', encoding='U8') as fr_file, \
     open('annotated-by-tool/eval-by-tool-es.tsv', mode='w', encoding='U8') as es_file, \
     open('eval-data-cs.tsv', mode='w', encoding='U8') as cs_eval_file, \
     open('eval-data-en.tsv', mode='w', encoding='U8') as en_eval_file, \
     open('eval-data-de.tsv', mode='w', encoding='U8') as de_eval_file, \
     open('eval-data-nl.tsv', mode='w', encoding='U8') as nl_eval_file, \
     open('eval-data-ru.tsv', mode='w', encoding='U8') as ru_eval_file, \
     open('eval-data-fr.tsv', mode='w', encoding='U8') as fr_eval_file, \
     open('eval-data-es.tsv', mode='w', encoding='U8') as es_eval_file:
    next(input_file)  # skip header
    for line in input_file:
        _, lexeme, parents, language, word_type, block, PaReNT_opinion = line.strip().split(',')
        if language == 'cs':
            print(lexeme, PaReNT_opinion, sep='\t', file=cs_file)
            print(lexeme, word_type, sep='\t', file=cs_eval_file)
        elif language == 'en':
            print(lexeme, PaReNT_opinion, sep='\t', file=en_file)
            print(lexeme, word_type, sep='\t', file=en_eval_file)
        elif language == 'de':
            print(lexeme, PaReNT_opinion, sep='\t', file=de_file)
            print(lexeme, word_type, sep='\t', file=de_eval_file)
        elif language == 'nl':
            print(lexeme, PaReNT_opinion, sep='\t', file=nl_file)
            print(lexeme, word_type, sep='\t', file=nl_eval_file)
        elif language == 'ru':
            print(lexeme, PaReNT_opinion, sep='\t', file=ru_file)
            print(lexeme, word_type, sep='\t', file=ru_eval_file)
        elif language == 'es':
            print(lexeme, PaReNT_opinion, sep='\t', file=es_file)
            print(lexeme, word_type, sep='\t', file=es_eval_file)
        elif language == 'fr':
            print(lexeme, PaReNT_opinion, sep='\t', file=fr_file)
            print(lexeme, word_type, sep='\t', file=fr_eval_file)
