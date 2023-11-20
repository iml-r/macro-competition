#!/usr/bin/env python3
# coding: utf-8

import string
import argparse

# commands:
# python3 filter_out_symbols.py --input_file 'google/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'google/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'cognet/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'cognet/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'panlex/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'panlex/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'universalwordnet/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'universalwordnet/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'treq/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'treq/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'yes'
# python3 filter_out_symbols.py --input_file 'unsup-nn/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'no'
# python3 filter_out_symbols.py --input_file 'unsup-nn/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'no'
# python3 filter_out_symbols.py --input_file 'parallel-corpora/diminutives-cs2oth-filtred-with-pos.tsv' --has_header 'no'
# python3 filter_out_symbols.py --input_file 'parallel-corpora/social-gender-cs2oth-filtred-with-pos.tsv' --has_header 'no'


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_file')
parser.add_argument('--has_header', choices=('yes', 'no'))
args = parser.parse_args()

special_symbols = string.punctuation.replace('|', '').replace('-', '').replace('–', '').replace('.', ''). replace(',', '').replace(';', '')


# process the input file
filtred_data = list()
with open(args.input_file, mode='r', encoding='U8') as input_file:
    
    # skip header if necessary
    if args.has_header == 'yes':
        header1 = next(input_file)
        header1 = header1.rstrip('\n').split('\t')
        filtred_data.append(header1)

        header2 = next(input_file)
        header2 = header2.rstrip('\n').split('\t')
        filtred_data.append(header2)

    # process data
    for line in input_file:
        # store processed data in output_line
        # [
        #   cs, cs2en, cs2de, cs2nl, cs2ru, cs2es, cs2fr, en2cs,
        #   de2cs, nl2cs, ru2cs, es2cs, fr2cs
        # ]
        output_line = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        # load original data
        line = line.rstrip('\n').split('\t')
        line = [item.split(';') for item in line]

        # exclude items with special symbols and remove symbols in the respective list
        for idx, language_data in enumerate(line):
            for entry in language_data:
                # skip entries with special chararters
                if any(char in entry for char in special_symbols):
                    continue
                # remove individual symbols
                entry = entry.replace(',', '').replace('.', '')
                # store
                output_line[idx].append(entry)
            output_line[idx] = ';'.join(output_line[idx])

        # store
        filtred_data.append(output_line)


# store resulting data
with open(args.input_file, mode='w', encoding='U8') as output_file:
    # create header
    if args.has_header == 'no':
        print(
                'source',
                'forward', 'forward', 'forward', 'forward', 'forward', 'forward',
                'backward', 'backward', 'backward', 'backward', 'backward', 'backward',
                sep='\t' , file=output_file
            )
        print(
                'Czech',
                'English', 'Deutch', 'Dutch', 'Russian', 'Spanish', 'French',
                'English', 'Deutch', 'Dutch', 'Russian', 'Spanish', 'French',
                sep='\t' , file=output_file
            )
        
    # store data
    for line in filtred_data:
        print(*line, sep='\t' , file=output_file)
