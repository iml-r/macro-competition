#!/usr/bin/env python3
# coding: utf-8

import argparse
from collections import defaultdict


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--Derinet', default='derinet-2-1.tsv')
parser.add_argument('--SemanticLabel')
parser.add_argument('--OutputData')
args = parser.parse_args()


# load input data
lexemes = defaultdict()
with open(args.Derinet, mode='r', encoding='U8') as file:
    for line in file:
        line = line.rstrip('\n').split('\t')
        
        if line == ['']:
            continue

        lexemes[line[0]] = (line[2], line[3], line[6], line[7])


# extract desired pairs: apellative nouns of the selected semantic concept
with open(args.OutputData, mode='w', encoding='U8') as file:
    for id, item in lexemes.items():
        if 'SemanticLabel={}'.format(args.SemanticLabel) in item[3]:
            if 'NOUN' in item[1]:
                parent = lexemes.get(item[2], 'x')[0]
                if not item[0][0].isupper() and not parent[0].isupper():
                    print(item[0], '<', parent, sep='\t', file=file)
