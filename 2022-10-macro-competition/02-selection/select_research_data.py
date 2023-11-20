#!/usr/bin/env python3
# coding: utf-8

import regex as re
import argparse
from collections import defaultdict

# commands:
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv'  --input_translations '../01-translation/parallel-corpora/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'parallel-corpora/social-gender-cs.tsv' 'parallel-corpora/social-gender-en.tsv' 'parallel-corpora/social-gender-de.tsv' 'parallel-corpora/social-gender-nl.tsv' 'parallel-corpora/social-gender-ru.tsv' 'parallel-corpora/social-gender-es.tsv' 'parallel-corpora/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/parallel-corpora/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'parallel-corpora/diminutives-cs.tsv' 'parallel-corpora/diminutives-en.tsv' 'parallel-corpora/diminutives-de.tsv' 'parallel-corpora/diminutives-nl.tsv' 'parallel-corpora/diminutives-ru.tsv' 'parallel-corpora/diminutives-es.tsv' 'parallel-corpora/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/unsup-nn/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'unsup-nn/social-gender-cs.tsv' 'unsup-nn/social-gender-en.tsv' 'unsup-nn/social-gender-de.tsv' 'unsup-nn/social-gender-nl.tsv' 'unsup-nn/social-gender-ru.tsv' 'unsup-nn/social-gender-es.tsv' 'unsup-nn/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/unsup-nn/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'unsup-nn/diminutives-cs.tsv' 'unsup-nn/diminutives-en.tsv' 'unsup-nn/diminutives-de.tsv' 'unsup-nn/diminutives-nl.tsv' 'unsup-nn/diminutives-ru.tsv' 'unsup-nn/diminutives-es.tsv' 'unsup-nn/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/universalwordnet/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'universalwordnet/social-gender-cs.tsv' 'universalwordnet/social-gender-en.tsv' 'universalwordnet/social-gender-de.tsv' 'universalwordnet/social-gender-nl.tsv' 'universalwordnet/social-gender-ru.tsv' 'universalwordnet/social-gender-es.tsv' 'universalwordnet/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/universalwordnet/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'universalwordnet/diminutives-cs.tsv' 'universalwordnet/diminutives-en.tsv' 'universalwordnet/diminutives-de.tsv' 'universalwordnet/diminutives-nl.tsv' 'universalwordnet/diminutives-ru.tsv' 'universalwordnet/diminutives-es.tsv' 'universalwordnet/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/cognet/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'cognet/social-gender-cs.tsv' 'cognet/social-gender-en.tsv' 'cognet/social-gender-de.tsv' 'cognet/social-gender-nl.tsv' 'cognet/social-gender-ru.tsv' 'cognet/social-gender-es.tsv' 'cognet/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/cognet/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'cognet/diminutives-cs.tsv' 'cognet/diminutives-en.tsv' 'cognet/diminutives-de.tsv' 'cognet/diminutives-nl.tsv' 'cognet/diminutives-ru.tsv' 'cognet/diminutives-es.tsv' 'cognet/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/google/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'google/social-gender-cs.tsv' 'google/social-gender-en.tsv' 'google/social-gender-de.tsv' 'google/social-gender-nl.tsv' 'google/social-gender-ru.tsv' 'google/social-gender-es.tsv' 'google/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/google/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'google/diminutives-cs.tsv' 'google/diminutives-en.tsv' 'google/diminutives-de.tsv' 'google/diminutives-nl.tsv' 'google/diminutives-ru.tsv' 'google/diminutives-es.tsv' 'google/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/treq/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'treq/social-gender-cs.tsv' 'treq/social-gender-en.tsv' 'treq/social-gender-de.tsv' 'treq/social-gender-nl.tsv' 'treq/social-gender-ru.tsv' 'treq/social-gender-es.tsv' 'treq/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/treq/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'treq/diminutives-cs.tsv' 'treq/diminutives-en.tsv' 'treq/diminutives-de.tsv' 'treq/diminutives-nl.tsv' 'treq/diminutives-ru.tsv' 'treq/diminutives-es.tsv' 'treq/diminutives-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --input_translations '../01-translation/panlex/social-gender-cs2oth-filtred-with-pos.tsv' --output_files 'panlex/social-gender-cs.tsv' 'panlex/social-gender-en.tsv' 'panlex/social-gender-de.tsv' 'panlex/social-gender-nl.tsv' 'panlex/social-gender-ru.tsv' 'panlex/social-gender-es.tsv' 'panlex/social-gender-fr.tsv'
# python3 select_research_data.py --has_header 'yes' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --input_translations '../01-translation/panlex/diminutives-cs2oth-filtred-with-pos.tsv' --output_files 'panlex/diminutives-cs.tsv' 'panlex/diminutives-en.tsv' 'panlex/diminutives-de.tsv' 'panlex/diminutives-nl.tsv' 'panlex/diminutives-ru.tsv' 'panlex/diminutives-es.tsv' 'panlex/diminutives-fr.tsv'


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_translations')
parser.add_argument('--has_header', choices=('yes', 'no'))
parser.add_argument('--input_sources')
parser.add_argument('--output_files', nargs='+')
args = parser.parse_args()


# indexes in the data
cs1 = 0
en1 = 1
de1 = 2
nl1 = 3
ru1 = 4
es1 = 5
fr1 = 6
en2 = 7
de2 = 8
nl2 = 9
ru2 = 10
es2 = 11
fr2 = 12


# load parents
parents = defaultdict()
with open(args.input_sources, mode='r', encoding='U8') as file:
    for line in file:
        line = line.rstrip('\n').split('\t')
        parents[line[0]] = line[-1]


# load and select research data
with open(args.input_translations, mode='r', encoding='U8') as input_file, \
     open(args.output_files[0], mode='w', encoding='U8') as cs_file, \
     open(args.output_files[1], mode='w', encoding='U8') as en_file, \
     open(args.output_files[2], mode='w', encoding='U8') as de_file, \
     open(args.output_files[3], mode='w', encoding='U8') as nl_file, \
     open(args.output_files[4], mode='w', encoding='U8') as ru_file, \
     open(args.output_files[5], mode='w', encoding='U8') as es_file, \
     open(args.output_files[6], mode='w', encoding='U8') as fr_file:

    # skip header if necessary
    if args.has_header == 'yes':
        next(input_file)
        next(input_file)

    # go through input data
    for line in input_file:
        line = line.rstrip('\n')
        line = re.sub(r'\|[A-Z]+', '', line)
        line = [item for item in line.split('\t')]

        # skip incomplete translations equivalents
        if not all(item != '' for item in line):
            continue

        # skip incorrect translations
        exact_in = True
        if line[cs1] not in line[en2] or line[cs1] not in line[de2] or line[cs1] not in line[nl2] or \
           line[cs1] not in line[ru2] or line[cs1] not in line[es2] or line[cs1] not in line[fr2]:  # check exact translation
            exact_in = False
        
        neutral_in = True
        if parents.get(line[cs1], '') not in line[en2] or parents.get(line[cs1], '') not in line[de2] or \
           parents.get(line[cs1], '') not in line[nl2] or parents.get(line[cs1], '') not in line[ru2] or \
           parents.get(line[cs1], '') not in line[es2] or parents.get(line[cs1], '') not in line[fr2]:  # check neutral translation
            neutral_in = False

        if exact_in == False and neutral_in == False:  # decide on correctness of translation
            continue

        # select the best translation equivalent for individua languages
        print(line[cs1].split(';')[0], file=cs_file)
        print(line[en1].split(';')[0], file=en_file)
        print(line[de1].split(';')[0], file=de_file)
        print(line[nl1].split(';')[0], file=nl_file)
        print(line[ru1].split(';')[0], file=ru_file)
        print(line[es1].split(';')[0], file=es_file)
        print(line[fr1].split(';')[0], file=fr_file)
