#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
from collections import defaultdict


# commands:
# python3 reformat_data.py --input_translations 'translated-diminutives-parents-ces-all.tsv' 'translated-diminutives-parents-all-ces.tsv' --output_file 'diminutives-cs2oth.tsv'
# python3 reformat_data.py --input_translations 'translated-social-gender-parents-ces-all.tsv' 'translated-social-gender-parents-all-ces.tsv' --output_file 'social-gender-cs2oth.tsv'


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_translations', nargs='+')
parser.add_argument('--output_file')
args = parser.parse_args()


# indexes in the data
cs = 0
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


# load panlex original format
def load_panlex(paths):
    czech_input = set()
    panlex_dictionary = defaultdict(lambda: defaultdict(set))
    for path in paths:
        with open(path, mode='r', encoding='U8') as file:
            for line in file:
                line = line.strip().split('\t')
                if line[2] != '<NA>':
                    panlex_dictionary[line[0]][(line[1], line[3])].add(line[2])
                if line[1] == 'ces':
                    czech_input.add(line[0])

    resulting_data = list()
    for word in czech_input:
        data_line = [
            word,
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'eng'), [])),
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'deu'), [])),
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'nld'), [])),
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'rus'), [])),
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'spa'), [])),
            ';'.join(panlex_dictionary.get(word, {}).get(('ces', 'fra'), [])),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('eng', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'eng'), [])]]))),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('deu', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'deu'), [])]]))),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('nld', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'nld'), [])]]))),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('rus', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'rus'), [])]]))),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('spa', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'spa'), [])]]))),
            ';'.join(list(itertools.chain(*[panlex_dictionary.get(w, {}).get(('fra', 'ces'), []) for w in [item for item in panlex_dictionary.get(word, {}).get(('ces', 'fra'), [])]])))
        ]
        resulting_data.append(data_line)

    return resulting_data


# load data
data = load_panlex(args.input_translations)

# reformat data
with open(args.output_file, mode='w', encoding='U8') as output_file:
    # header
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

    # data
    for line in data:
        print(*line, sep='\t' , file=output_file)
