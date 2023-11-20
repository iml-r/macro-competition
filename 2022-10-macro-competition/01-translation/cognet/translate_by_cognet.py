#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
from collections import defaultdict

# commands:
# python3 translate_by_cognet.py --source_path cognet.tsv --input_data ../../00-input-data/pairs-of-diminutives.tsv --output_data diminutives-cs2oth.tsv
# python3 translate_by_cognet.py --source_path cognet.tsv --input_data ../../00-input-data/pairs-of-social-gender.tsv --output_data social-gender-cs2oth.tsv


class TranslationCogNetAndUniWordNet:
    def __init__(self, source_language, target_languages, path_cognet=None, path_uniwordnet=None):
        if path_cognet and source_language and target_languages:
            self.cognet = self._load_resource(path_cognet, source_language, target_languages)
        if path_uniwordnet and source_language and target_languages:
            self.uniwordnet = self._load_resource(path_uniwordnet, source_language, target_languages)

    def _load_resource(self, path, source, languages):
        dictionary = defaultdict(lambda: defaultdict(set))
        with open(path, mode='r', encoding='U8') as file:
            for line in file:
                _, entries = line.rstrip('\n').split('\t')
                entries = entries.split(';')

                if any(entry.split('/')[0] == source for entry in entries):  # if there is a pivot language identified
                    # find all words from a pivot language
                    pivot_words = list()
                    for entry in entries:
                        lang, word = entry[:3], entry[4:]
                        if lang == source:
                            pivot_words.append(word)

                    # store all relevant translations for all pivot words above
                    for entry in entries:
                        lang, word = entry[:3], entry[4:]
                        if lang in languages:
                            for w in pivot_words:
                                dictionary[w][lang].add(word)
            file.seek(0)
        return dictionary

    def cognet_translate(self, word, lang):
        return ';'.join(self.cognet.get(word, {}).get(lang, ''))

    def uniwordnet_translate(self, word, lang):
        return ';'.join(self.uniwordnet.get(word, {}).get(lang, ''))


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source_path')
parser.add_argument('--input_data')
parser.add_argument('--output_data')
args = parser.parse_args()


# set translation, load models
parse_language = {'en': 'eng', 'fr': 'fra', 'cs': 'ces', 'de': 'deu', 'ru': 'rus', 'es': 'spa', 'nl': 'nld'}

model_cs2oth = TranslationCogNetAndUniWordNet(
    source_language=parse_language['cs'],
    target_languages=[parse_language['en'], parse_language['de'], parse_language['nl'], parse_language['ru'], parse_language['es'], parse_language['fr']],
    path_cognet=args.source_path
)

model_en2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['en'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)
model_de2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['de'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)
model_nl2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['nl'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)
model_ru2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['ru'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)
model_fr2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['fr'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)
model_es2cs = TranslationCogNetAndUniWordNet(
    source_language=parse_language['es'],
    target_languages=[parse_language['cs'],],
    path_cognet=args.source_path
)


# translate input data
with open(args.input_data, mode='r', encoding='U8') as input_file, \
     open(args.output_data, mode='w', encoding='U8') as output_file:
    
    # two-lines header for output file
    print(
        'source', '\t'.join(6*['forward']), '\t'.join(6*['backward']),
        sep='\t', file=output_file
    )
    print(
        'Czech',
        '\t'.join(['English', 'Deutch', 'Dutch', 'Russian', 'Spanish', 'French']),
        '\t'.join(['English', 'Deutch', 'Dutch', 'Russian', 'Spanish', 'French']),
        sep='\t', file=output_file
    )

    # translate individual words from input file, store them into output file
    for line in input_file:
        word, _, _ = line.strip().split('\t')

        data_line = [
            word,
            model_cs2oth.cognet_translate(word=word, lang=parse_language['en']),
            model_cs2oth.cognet_translate(word=word, lang=parse_language['de']),
            model_cs2oth.cognet_translate(word=word, lang=parse_language['nl']),
            model_cs2oth.cognet_translate(word=word, lang=parse_language['ru']),
            model_cs2oth.cognet_translate(word=word, lang=parse_language['es']),
            model_cs2oth.cognet_translate(word=word, lang=parse_language['fr']),
            ';'.join(list(itertools.chain(*[model_en2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['en']).split(';')]]))),
            ';'.join(list(itertools.chain(*[model_de2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['de']).split(';')]]))),
            ';'.join(list(itertools.chain(*[model_nl2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['nl']).split(';')]]))),
            ';'.join(list(itertools.chain(*[model_ru2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['ru']).split(';')]]))),
            ';'.join(list(itertools.chain(*[model_es2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['es']).split(';')]]))),
            ';'.join(list(itertools.chain(*[model_fr2cs.cognet_translate(word=w, lang=parse_language['cs']).split(';') for w in [item for item in model_cs2oth.cognet_translate(word=word, lang=parse_language['fr']).split(';')]])))
        ]

        print(*data_line, sep='\t', file=output_file)
