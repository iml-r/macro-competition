#!/usr/bin/env python3
# coding: utf-8


# commands:
# python3 annotation_procedure.py --source_data 'cognet/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'google/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'panlex/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'parallel-corpora/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'treq/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'universalwordnet/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'unsup-nn/social-gender' --semantic_concept 'social-gender' --uder_data $(ls -1 UDer-1.1/*/*.gz)

# python3 annotation_procedure.py --source_data 'cognet/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'google/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'panlex/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'parallel-corpora/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'treq/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'universalwordnet/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)
# python3 annotation_procedure.py --source_data 'unsup-nn/diminutives' --semantic_concept 'diminutives' --uder_data $(ls -1 UDer-1.1/*/*.gz)

# python3 annotation_procedure.py --source_data '03-0-evaluation-data/annotated-by-tool/eval-by-tool' --semantic_concept 'any' --uder_data $(ls -1 UDer-1.1/*/*.gz)


import gzip
import random
import argparse
import regex as re
from collections import defaultdict



# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source_data')
parser.add_argument('--semantic_concept', choices=('diminutives', 'social-gender', 'any'))
parser.add_argument('--uder_data', nargs='+')
args = parser.parse_args()


def load_uder(paths):
    # načte relevantní UDer data a vrátí jako velikou databázi (dictionary)
    uder_database = defaultdict(lambda: defaultdict())
    for path in paths:
        # vybere relevantní jazyk
        with gzip.open(path, 'rb') as gz_file:
            language_name = re.search(r'UDer-1.1-(..)-', path).group(1)
            if language_name not in ['en', 'de', 'ru', 'nl', 'es', 'fr', 'cs']:
                continue

            # zpracuje data
            data = defaultdict()
            for line in gz_file:
                # načte řádek
                line = line.decode('utf-8').rstrip().split('\t')
                if len(line) == 1:
                    continue

                # uloží informace
                data[line[0]] = line
            
            # zpracuje anotaci
            for _, entry in data.items():
                if entry[7] != '':
                    parent = data[entry[6]]
                    if re.search(r'Type=([A-Z][a-z]+)', entry[7]).group(1) == 'Compounding':
                        uder_database[language_name][entry[2]] = 'Compound'
                    elif entry[2] == parent[2]:  # and entry[3] == parent[3]:
                        uder_database[language_name][entry[2]] = 'Derivative'
                    elif entry[2] != parent[2]:  # and entry[3] == parent[3]:
                        uder_database[language_name][entry[2]] = 'Derivative'
                    else:
                        continue

    return uder_database


def analyse_using_Uder(word, language, uder_database):  # --> 'Compound', 'Derivative', 'None'
    return uder_database.get(language, {}).get(word, 'None')


def exclude_articles(word, language):
    en_articles = ['a ', 'an ', 'the ']
    de_articles = ['ein ', 'eine ', 'einem ', 'einer ', 'eines ', 'der ', 'die ', 'das ', 'dem ', 'den ', 'des ']
    nl_articles = ['het ', 'de ', 'een ']
    fr_articles = ['un ', 'une ', 'des ', 'le ', 'la ', 'les ']
    es_articles = ['un ', 'una ', 'unos ', 'unas ', 'el ', 'la ', 'los ', 'las ', 'lo ']

    if language == 'en':
        for article in en_articles:
            if word.startswith(article):
                word = word[len(article):]

    elif language == 'de':
        for article in de_articles:
            if word.startswith(article):
                word = word[len(article):]

    elif language == 'nl':
        for article in nl_articles:
            if word.startswith(article):
                word = word[len(article):]

    elif language == 'fr':
        for article in fr_articles:
            if word.startswith(article):
                word = word[len(article):]

    elif language == 'es':
        for article in es_articles:
            if word.startswith(article):
                word = word[len(article):]

    return word


def analyse_words_with_hyphen(word, language):  # --> 'None', 'Derivative', 'Compound'
    if '-' not in word:
        return 'None'

    en_prefixes = [
        'non-', 'post-', 'pre-', 'ex-', 'multi-', 'semi-', 'sub-', 'anti-', 'mini-', 'macro-', 'micro-',
        'intra-', 'co-', 're-', 'mid-', 'aero-', 'bio-', 'cross-', 'multi-', 'electro-', 'bi-', 'vice-',
        'demi-', 'infra-', 'supra-', 'pro-', 'pseudo-', 'over-', 'ultra-', 'psycho-', 'de-', 'inter-',
        'top-', 'homo-', 'hereto-', 'cyber-', 'uni-', 'endo-', 'socio-', 'after-', 'auto-', 'mega-',
        'giga-', 'kilo-', 'radio-', '-up', 'hetero-'
    ]
    de_prefixes = en_prefixes[:-1] + [
        'uber-', 'nicht-'
    ]
    fr_prefixes = en_prefixes[:-1] + [
        'contre-', 'sur-', 'pour-', 'proto-', 'mi-', 'trente-', 'agro-', 'sous-', 'électro-', 'stéréo-',
        'cani-', 'extra-', 'grand-', 'néo-', 'double-', 'oculo-', 'sus-', 'quasi-', 'utéro-', 'gastro-',
        'saint-', 'hépato-', 'paléo-', 'rétro-', 'néphro-', 'cardio-', 'pré-', 'ré-', 'mono-', 'pauci-',
        'mi-', 'super-', 'tout-', 'contro-', 'proto-', 'e-', 'cyto-', 'physio-', 'a-', 'cyclo-', 'fibro-',
        'demi-', 
    ]
    ru_prefixes = [
        'махи-', 'по-', 'минни-', 'вице-', 'не-', 'пресс-', 'супер-'
    ]
    es_prefixes = en_prefixes[:-1] + [
        'no-'
    ]
    nl_prefixes = en_prefixes[:-1] + [
        'niet-'
    ]

    if language == 'en':
        if any(item in word.lower() for item in en_prefixes):
            return 'Derivative'
        return 'Compound'

    elif language == 'de':
        if any(item in word.lower() for item in de_prefixes):
            return 'Derivative'
        return 'Compound'

    elif language == 'fr':
        if any(item in word.lower() for item in fr_prefixes):
            return 'Derivative'
        return 'Compound'

    elif language == 'ru':
        if any(item in word.lower() for item in ru_prefixes):
            return 'Derivative'
        return 'Compound'

    elif language == 'es':
        if any(item in word.lower() for item in es_prefixes + en_prefixes):
            return 'Derivative'
        return 'Compound'

    elif language == 'nl':
        if any(item in word.lower() for item in nl_prefixes + en_prefixes):
            return 'Derivative'
        return 'Compound'

    return 'None'


def analyse_using_custom_rules(word, language, concept):  # --> 'None', 'Derivative', 'Compound', 'Unmotivated', 'Unmarked'
    if language == 'en':
        if concept == 'social-gender' or concept == 'any':
            suffixes = [
                'ix', 'ine', 'ess'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

            suffixes_man = [
                'er', 'or', 'ist', 'at'
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

            components = [
                'woman', 'mother', 'girl', 'lady', 'mom', 'mum', 'women', 'she'
            ]
            if any(component in word and len(word) > len(component) for component in components):
                return 'Compound'
            if any(component in word and len(word) == len(component) for component in components):
                return 'Unmotivated'
            
            components_man = [
                'man', 'father', 'boy', 'gentleman', 'daddy', 'dad', 'men', 'brother'
            ]
            if any(component in word for component in components_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'ie', 'ling', 'y', 'let', 'sie', 'sies', 'sy', 'le', 'ish', 'kin', 'kins', 'poo',
                'pop', 'peg'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    if language == 'fr':
        if concept == 'social-gender' or concept == 'any':
            suffixes = [
                'esse', 'ric', 'sse', 'que', 'lle', 'tte', 'se', 'èr', 'ice', 'ïne', 'ante', 'iste', 'ste',
                # general suffixes
                'ment', 'ien', 'main', 'ible', 'isme', 'er', 'ure', 'al', 'emens', 'la', 'ire', 'ine', 'in', 'ate', 'ium',
                'ude', 'age', 'ir', 'iel', 'ité', 'ie', 'iel', 'yle', 'if', 'ide', 'ème', 'is', 'des', 'ade', 'ite', 'an',
                'ule', 'ien'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

            suffixes_man = [
                'eur', 'or', 'ist', 'ier', 'gue', 'ant'
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

            components = [
                'femme', 'fille', 'madame', 'mademoiselle', 'woman', 'miss', 'wife'
            ]
            general_components = [
                'bus', 'garde', 'dit', 'marché', 'graphe', 'graphie', 'bon', 'thérapie', 'phone', 'porte', 'porno', 'zoo'
            ]
            if any(component in word and len(word) > len(component) for component in components) or \
               any((word.startswith(component) or word.endswith(component)) and len(word) > len(component) for component in general_components):
                return 'Compound'
            if any(component in word and len(word) == len(component) for component in components):
                return 'Unmotivated'
            
            components_man = [
                'garçon', 'homme', 'monsieur'
            ]
            if any(component in word for component in components_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'tte', 'lle', 'let', 'ette', 'lette', 'net', 'on', 'nou', 'ot',
                'eau', 'et', 'oc', 'uc', 'oche'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    if language == 'ru':
        if concept == 'social-gender' or concept == 'any':
            suffixes = [
                'ца', 'ка', 'ница', 'ша', 'есса'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

            suffixes_man = [
                'чик', 'ник', 'тель', 'ец', 
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'ик', 'ка', 'ок', 'чик', 'че', 'чо', 'ец', 'ек', 'ёк', 'ик', 'очек', 'ечек',
                'ёчик', 'ица', 'ичка', 'очка', 'ечка', 'ико', 'ко', 'ышко', 'икл'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    if language == 'de':
        if concept == 'social-gender' or concept == 'any':
            suffixes = [
                'in', 'ère', 'euse'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'
            
            suffixes_man = [
                'er', 'or', 'ör', 'ist', 'it', 'ite', 'ant', 'ent', 'loge'
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

            components = [
                'frau', 'mutter', 'tochter', 'schwester', 'mädchen', 'tante', 'woman', 'girl'
            ]
            if any(component in word and len(word) > len(component) for component in components):
                return 'Compound'
            if any(component in word and len(word) == len(component) for component in components):
                return 'Unmotivated'

            components_man = [
                'herr', 'vater', 'junge', 'gentleman', 'vati', 'papa', 'mann', 'bruder', 'onkel', 'sohn'
            ]
            if any(component in word for component in components_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'chen', 'lein'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    if language == 'es':
        if concept == 'social-gender' or concept == 'any':
            components = [
                'abre', 'entre', 'traga', 'terreno', 'aguas', 'ventana', 'herpa', 'volea',
                'posición', 'supinación', 'sujetar', 'adiós', 'blusa', 'tacán',
                'pija', 'mecual', 'torgo', 'tegua', 'costar', 'acreer', 'apuro', 'continuo', 'apego',
                'fibroma', 'meneo', 'pava', 'renuncia', 'geosito', 'pobrete', 'axactriz', 'moide'
            ]
            if any(component in word and len(word) > len(component) for component in components):
                return 'Compound'
            if any(component in word and len(word) == len(component) for component in components):
                return 'Unmotivated'

            suffixes = [
                'esa', 'ésa', 'ona', 'ana', 'ina', 'riza', 'ína', 'ra', 'oga', 'ori', 'ear', 'izo',
                'ar', 'or', 'ión', 'mente', 'able', 'ide', 'azo', 'ado', 'ante', 'ados', 'ivo', 'ial',
                'ica', 'ivo', 'ero', 'ad', 'ento', ''
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

            prefixes = [
                'moto', 'gamma', 'radio', 'dia', 'mielo', 'tetra', 'triter', 'mono', 'anti',
                'en', 'renun', 'des', 're', 'sob'
            ]
            if any(word.startswith(prefix) for prefix in prefixes):
                return 'Derivative'

            suffixes_man = [
                'dor', 'ero', 'ista', 'ario', 'it', 'ite', 'ant', 'ent', 'ar', 'or', 'og'
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'onta', 'onlla', 'onuela', 'oncita', 'oncilla', 'onciuela',
                'onto', 'onllo', 'onuelo', 'oncito', 'oncillo', 'onciuelo',
                'ta', 'lla', 'uela', 'to', 'llo', 'uelo',
                'ita', 'illa', 'iuela', 'ito', 'illo', 'iuelo',
                'cita', 'cilla', 'ciuela', 'cito', 'cillo', 'ciuelo',
                'qta', 'qlla', 'quela', 'qto', 'qllo', 'quelo',
                'quita', 'quilla', 'quiuela', 'quito', 'quillo', 'quiuelo',
                'guita', 'guilla', 'guiuela', 'guito', 'guillo', 'guiuelo'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    if language == 'nl':
        if concept == 'social-gender' or concept == 'any':
            suffixes = [
                'ante', 'ente', 'iste', 'oste', 'ster', 'ester', 'fster', 'eefster', 'in',
                'avin', 'te', 'ge', 'eres', 'tes', 'rice', 'euse', 'ess', 'se', 'ische', 'rixg'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'
            
            suffixes_man = [
                'er', 'ende', 'or', 'iet', 'ant', 'aar', 'ateur', 'ent', 'eur', 'loog', 'ist'
            ]
            if any(word.endswith(suffix) for suffix in suffixes_man):
                return 'Unmarked'

            components = [
                'vrouw', 'moeder'
            ]
            if any(component in word and len(word) > len(component) for component in components):
                return 'Compound'
            if any(component in word and len(word) == len(component) for component in components):
                return 'Unmotivated'

            components_man = [
                'meneer', 'vater'
            ]
            if any(component in word for component in components_man):
                return 'Unmarked'

        if concept == 'diminutives' or concept == 'any':
            suffixes = [
                'je', 'ke', 'eken', 'jes', 'meisje', 'ijn'
            ]
            if any(word.endswith(suffix) for suffix in suffixes):
                return 'Derivative'

    return 'None'



# ANNOTATION PROCEDURE

# load UDer data
uder_database = load_uder(args.uder_data)


# go through files annotated by tools and apply heuristics
for language in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
    with open(args.source_data + '-' + language + '.tsv', mode='r', encoding='U8') as input_file, \
         open(args.source_data + '-' + language + '-final.tsv', mode='w', encoding='U8') as output_file:
        for line in input_file:
            word, dec_tool = line.rstrip().split('\t')
            word = exclude_articles(word, language)
            dec_hyp = analyse_words_with_hyphen(word, language)
            dec_uder = analyse_using_Uder(word, language, uder_database)
            dec_heur = analyse_using_custom_rules(word, language, args.semantic_concept)

            # # random annotation
            # print(word, random.choice(['Derivative', 'Compound', 'Phrase', 'Unmotivated']), sep='\t', file=output_file)
            # continue

            # space in word
            if ' ' in word:
                print(word, 'Phrase', sep='\t', file=output_file)
                continue

            # hyphen decision
            if dec_hyp != 'None':
                print(word, dec_hyp, sep='\t', file=output_file)
                continue

            # take decision from the tool in the case of selected languages
            if language in ('en', 'nl', 'de'):
                if dec_heur != dec_tool and args.semantic_concept != 'any' and dec_heur != 'None':
                    print(word, dec_heur, sep='\t', file=output_file)
                    continue
                print(word, dec_tool, sep='\t', file=output_file)
                continue

            # heuristics
            if dec_heur != 'None':
                if dec_heur == 'Unmarked' and args.semantic_concept == 'any':
                    print(word, 'Derivative', sep='\t', file=output_file)
                else:
                    if language == 'es' and len(word) < 7:
                        print(word, 'Unmotivated', sep='\t', file=output_file)
                        continue
                    print(word, dec_heur, sep='\t', file=output_file)
                continue

            # UDer decision
            if dec_uder != 'None':
                if dec_uder == 'Derivative':
                    print(word, 'Derivative', sep='\t', file=output_file)
                elif dec_uder == 'Compound':
                    print(word, 'Compound', sep='\t', file=output_file)
                else:
                    print(word, 'Unmotivated', sep='\t', file=output_file)
                continue

            # tool decision
            print(word, dec_tool, sep='\t', file=output_file)
