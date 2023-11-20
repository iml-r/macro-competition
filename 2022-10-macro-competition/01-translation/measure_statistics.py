#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
import regex as re
from collections import defaultdict

# commands:
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'google/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/google-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'google/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/google-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'cognet/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/cognet-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'cognet/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/cognet-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'universalwordnet/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/universalwordnet-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'universalwordnet/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/universalwordnet-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'panlex/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/panlex-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'panlex/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/panlex-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'treq/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/treq-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'yes' --input_translations 'treq/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/treq-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'no' --input_translations 'unsup-nn/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/unsup-nn-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'no' --input_translations 'unsup-nn/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/unsup-nn-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'no' --input_translations 'parallel-corpora/social-gender-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-1-statistics-before-filtering/parallel-corpora-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'no' --has_header 'no' --input_translations 'parallel-corpora/diminutives-cs2oth.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-1-statistics-before-filtering/parallel-corpora-diminution.tsv'

# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'google/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/google-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'google/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/google-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'cognet/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/cognet-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'cognet/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/cognet-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'universalwordnet/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/universalwordnet-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'universalwordnet/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/universalwordnet-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'panlex/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/panlex-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'panlex/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/panlex-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'treq/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/treq-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'treq/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/treq-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'unsup-nn/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/unsup-nn-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'unsup-nn/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/unsup-nn-diminution.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'parallel-corpora/social-gender-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-social-gender.tsv' --output_statistics '01-2-statistics-after-filtering/parallel-corpora-social-gender.tsv'
# python3 measure_statistics.py --source_of_translation 'google-type' --tagged 'yes' --has_header 'yes' --input_translations 'parallel-corpora/diminutives-cs2oth-filtred-with-pos.tsv' --input_sources '../00-input-data/pairs-of-diminutives.tsv' --output_statistics '01-2-statistics-after-filtering/parallel-corpora-diminution.tsv'

# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source_of_translation', choices=('google-type', 'panlex-type'))
parser.add_argument('--tagged', choices=('yes', 'no'))
parser.add_argument('--has_header', choices=('yes', 'no'))
parser.add_argument('--input_translations', nargs='+', default='google/social-gender-cs2oth.tsv')
parser.add_argument('--input_sources', default='../00-input-data/pairs-of-social-gender.tsv')
parser.add_argument('--output_statistics', default='google-social-gender.tsv')
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


# load data
def load_google(path, header, tagged):
    data = list()
    with open(path, mode='r', encoding='U8') as file:
        if header == 'yes':
            next(file)
            next(file)
        for line in file:
            if tagged == 'yes':
                line = re.sub(r'\|[A-Z]+', '', line)
            line = line.rstrip('\n').split('\t')
            line = [item.lower() for item in line]
            data.append(line)
    return data


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


if args.source_of_translation == 'google-type':
    data = load_google(args.input_translations[0], args.has_header, args.tagged)
elif args.source_of_translation == 'panlex-type':
    data = load_panlex(args.input_translations)


# load parents
parents = defaultdict()
with open(args.input_sources, mode='r', encoding='U8') as file:
    for line in file:
        line = line.rstrip('\n').split('\t')
        parents[line[0]] = line[-1]


# function: calculate statistics for individual languages; TODO: slovní druhy (?)
def calculate(dataset, sources):
    kolik_se_najde_prekladu_z_cs_do_ostatnich = defaultdict(int)  # cs->oth
    kolik_se_najde_prekladu_z_ostatnich_do_cs = defaultdict(int)  # oth->cs
    kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs = defaultdict(int)  # cs->oth->cs, tzv. kompletni preklady

    jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni = defaultdict(list)
    jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs = defaultdict(list)
    jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs = defaultdict(list)

    kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu = defaultdict(int)
    kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu = defaultdict(int)
    kolik_kompletnich_prekladu_ma_pouze_neutralni_formu = defaultdict(int)
    kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu = defaultdict(int)

    kolik_prekladu_z_cs_do_ostatni_je_kopie = defaultdict(int)
    kolik_prekladu_z_ostatni_do_cs_je_kopie = defaultdict(int)

    for entry in dataset:
        for idx_z_cs_do_ostatni in (1, 2, 3, 4, 5, 6):
            kolik_se_najde_prekladu_z_cs_do_ostatnich[idx_z_cs_do_ostatni-1] += 1 if entry[idx_z_cs_do_ostatni] != '' else 0
            kolik_prekladu_z_cs_do_ostatni_je_kopie[idx_z_cs_do_ostatni-1] += 1 if entry[0] == entry[idx_z_cs_do_ostatni] and entry[idx_z_cs_do_ostatni] != '' else 0
            if entry[idx_z_cs_do_ostatni] != '':
                jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni[idx_z_cs_do_ostatni-1].append(len(entry[idx_z_cs_do_ostatni].split(';')))

        for idx_z_ostatni_do_cs in (7, 8, 9, 10, 11, 12):
            kolik_se_najde_prekladu_z_ostatnich_do_cs[idx_z_ostatni_do_cs-7] += 1 if entry[idx_z_ostatni_do_cs] != '' else 0
            kolik_prekladu_z_ostatni_do_cs_je_kopie[idx_z_ostatni_do_cs-7] += 1 if entry[idx_z_ostatni_do_cs] == entry[idx_z_ostatni_do_cs-6] and entry[idx_z_ostatni_do_cs] != '' else 0
            if entry[idx_z_ostatni_do_cs] != '':
                jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs[idx_z_ostatni_do_cs-7].append(len(entry[idx_z_ostatni_do_cs].split(';')))

        for idx_z_cs_do_ostatni, idx_z_ostatni_do_cs in zip((1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)):
            if entry[idx_z_cs_do_ostatni] != '' and entry[idx_z_ostatni_do_cs] != '':
                kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs[idx_z_cs_do_ostatni-1] += 1
                jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs[idx_z_cs_do_ostatni-1].append(len(entry[idx_z_ostatni_do_cs].split(';')))
                kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu[idx_z_cs_do_ostatni-1] += 1 if entry[0] == entry[idx_z_ostatni_do_cs] else 0
                kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu[idx_z_cs_do_ostatni-1] += 1 if entry[0] in entry[idx_z_ostatni_do_cs].split(';') else 0
                kolik_kompletnich_prekladu_ma_pouze_neutralni_formu[idx_z_cs_do_ostatni-1] += 1 if sources.get(entry[0], None) == entry[idx_z_ostatni_do_cs] else 0
                kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu[idx_z_cs_do_ostatni-1] += 1 if sources.get(entry[0], None) in entry[idx_z_ostatni_do_cs].split(';') else 0

    # calculate means
    for key, values in jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni.items():
        jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni[key] = round(sum(values) / len(values), 2)
    
    for key, values in jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs.items():
        jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs[key] = round(sum(values) / len(values), 2)
    
    for key, values in jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs.items():
        jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs[key] = round(sum(values) / len(values), 2)

    return (
        kolik_se_najde_prekladu_z_cs_do_ostatnich,
        kolik_se_najde_prekladu_z_ostatnich_do_cs,
        kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs,
        jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni,
        jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs,
        jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs,
        kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu,
        kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu,
        kolik_kompletnich_prekladu_ma_pouze_neutralni_formu,
        kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu,
        kolik_prekladu_z_cs_do_ostatni_je_kopie,
        kolik_prekladu_z_ostatni_do_cs_je_kopie
    )


# function: calculate size of the complete translation table
def complete_table(dataset):
    kolik_prekladu_pro_vsechny_jazyky = 0
    for entry in dataset:
        if all(item != '' for item in entry):
            kolik_prekladu_pro_vsechny_jazyky += 1
    return kolik_prekladu_pro_vsechny_jazyky


# return statistics
with open(args.output_statistics, mode='w', encoding='U8') as file:
    results = calculate(data, parents)

    print('Feature', 'English', 'German', 'Dutch', 'Russian', 'French', 'Spanish', sep='\t', file=file)
    header = (
        'kolik_se_najde_prekladu_z_cs_do_ostatnich',
        'kolik_se_najde_prekladu_z_ostatnich_do_cs',
        'kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs',
        'jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni',
        'jaky_je_prumerny_pocet_kandidatu_pri_ostatni_do_cs',
        'jaky_je_prumerny_pocet_kandidatu_pri_cs_pres_ostatni_do_cs',
        'kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu',
        'kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu',
        'kolik_kompletnich_prekladu_ma_pouze_neutralni_formu',
        'kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu',
        'kolik_prekladu_z_cs_do_ostatni_je_kopie',
        'kolik_prekladu_z_ostatni_do_cs_je_kopie'
    )
    for idx in range(len(results)):
        print(
            header[idx],
            results[idx][0],
            results[idx][1],
            results[idx][2],
            results[idx][3],
            results[idx][4],
            results[idx][5],
            sep='\t', file=file
        )
    print(file=file)
    
    print(
        'kolik_prekladu_pro_vsechny_jazyky', complete_table(data),
        sep='\t', file=file
    )
