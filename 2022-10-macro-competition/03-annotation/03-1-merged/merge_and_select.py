#!/usr/bin/env python3
# coding: utf-8

import argparse
from collections import defaultdict, Counter


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--semantic_concept', choices=('diminutives', 'social-gender'))
args = parser.parse_args()


# load data
google_data = defaultdict(lambda: defaultdict())
panlex_data = defaultdict(lambda: defaultdict())
corpora_data = defaultdict(lambda: defaultdict())
treq_data = defaultdict(lambda: defaultdict())
unsup_data = defaultdict(lambda: defaultdict())
for source, s_data in zip(
    ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn'),
    (google_data, panlex_data, corpora_data, treq_data, unsup_data)
):
    with open(f'../{source}/' + args.semantic_concept + '-cs-final.tsv', mode='r', encoding='U8') as cs_file, \
         open(f'../{source}/' + args.semantic_concept + '-en-final.tsv', mode='r', encoding='U8') as en_file, \
         open(f'../{source}/' + args.semantic_concept + '-de-final.tsv', mode='r', encoding='U8') as de_file, \
         open(f'../{source}/' + args.semantic_concept + '-nl-final.tsv', mode='r', encoding='U8') as nl_file, \
         open(f'../{source}/' + args.semantic_concept + '-ru-final.tsv', mode='r', encoding='U8') as ru_file, \
         open(f'../{source}/' + args.semantic_concept + '-fr-final.tsv', mode='r', encoding='U8') as fr_file, \
         open(f'../{source}/' + args.semantic_concept + '-es-final.tsv', mode='r', encoding='U8') as es_file:
        for cs_line in cs_file:
            en_line, de_line = next(en_file), next(de_file)
            nl_line, ru_line = next(nl_file), next(ru_file)
            fr_line, es_line = next(fr_file), next(es_file)

            s_data[cs_line.strip().split('\t')[0]]['xx'] = cs_line.strip().split('\t')[1]
            s_data[cs_line.strip().split('\t')[0]]['en'] = tuple(en_line.strip().split('\t'))
            s_data[cs_line.strip().split('\t')[0]]['de'] = tuple(de_line.strip().split('\t'))
            s_data[cs_line.strip().split('\t')[0]]['nl'] = tuple(nl_line.strip().split('\t'))
            s_data[cs_line.strip().split('\t')[0]]['ru'] = tuple(ru_line.strip().split('\t'))
            s_data[cs_line.strip().split('\t')[0]]['fr'] = tuple(fr_line.strip().split('\t'))
            s_data[cs_line.strip().split('\t')[0]]['es'] = tuple(es_line.strip().split('\t'))


# merge data
resulting_data = [list(), list(), list(), list(), list(), list(), list()]
for czech_word in set(list(google_data.keys()) + list(panlex_data.keys()) + list(corpora_data.keys()) + list(treq_data.keys()) + list(unsup_data.keys())):
    # Czech annotation
    cs_decisions = [
        google_data[czech_word].get('xx', None), panlex_data[czech_word].get('xx', None), corpora_data[czech_word].get('xx', None),
        treq_data[czech_word].get('xx', None), unsup_data[czech_word].get('xx', None)
    ]
    while None in cs_decisions:
        cs_decisions.remove(None)
    resulting_data[0].append((czech_word, cs_decisions[0]))

    # other languages annotations
    for idx, language in zip(range(1, 7), ('en', 'de', 'nl', 'ru', 'fr', 'es')):
        decisions = [
            google_data[czech_word].get(language, None), panlex_data[czech_word].get(language, None), corpora_data[czech_word].get(language, None),
            treq_data[czech_word].get(language, None), unsup_data[czech_word].get(language, None)
        ]
        while None in decisions:
            decisions.remove(None)

        # the most occurences across sources of translations
        dec_words = Counter([w for w, _ in decisions])
        dec_most = dec_words.most_common(1)
        without_most = list(dec_words.values())
        without_most.remove(dec_most[0][1])
        if dec_most[0][1] not in without_most:
            for word, annot in decisions:
                if word == dec_most[0][0]:
                    resulting_data[idx].append((word, annot))
                    break
            continue

        # hierarchy: panlex > treq > corpora > unsup > google
        dec_words = Counter([w for w, _ in decisions])
        max_count = max(dec_words.values())
        words = [w for w, c in dec_words.items() if c == max_count]
        
        found = False
        for source_data in (panlex_data, treq_data, corpora_data, unsup_data, google_data):
            for word in words:
                if source_data[czech_word].get(language, False):
                    resulting_data[idx].append(source_data[czech_word].get(language, False))
                    found = True
                    break
            if found:
                break

        if not found:
            print(czech_word)

# store data
with open(f'merged-data/{args.semantic_concept}-cs-final.tsv', mode='w', encoding='U8') as cs_file, \
     open(f'merged-data/{args.semantic_concept}-en-final.tsv', mode='w', encoding='U8') as en_file, \
     open(f'merged-data/{args.semantic_concept}-de-final.tsv', mode='w', encoding='U8') as de_file, \
     open(f'merged-data/{args.semantic_concept}-nl-final.tsv', mode='w', encoding='U8') as nl_file, \
     open(f'merged-data/{args.semantic_concept}-ru-final.tsv', mode='w', encoding='U8') as ru_file, \
     open(f'merged-data/{args.semantic_concept}-fr-final.tsv', mode='w', encoding='U8') as fr_file, \
     open(f'merged-data/{args.semantic_concept}-es-final.tsv', mode='w', encoding='U8') as es_file:
    for idx in range(len(resulting_data[0])):
        print('\t'.join(resulting_data[0][idx]), file=cs_file)
        print('\t'.join(resulting_data[1][idx]), file=en_file)
        print('\t'.join(resulting_data[2][idx]), file=de_file)
        print('\t'.join(resulting_data[3][idx]), file=nl_file)
        print('\t'.join(resulting_data[4][idx]), file=ru_file)
        print('\t'.join(resulting_data[5][idx]), file=fr_file)
        print('\t'.join(resulting_data[6][idx]), file=es_file)
