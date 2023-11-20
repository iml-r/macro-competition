#!/usr/bin/env python3
# coding: utf-8

import sys
import json
import time
import logging
import argparse
import requests


# commands:
# python3 morpho_annot_and_filter.py --input_file 'google/diminutives-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'google/social-gender-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'cognet/diminutives-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'cognet/social-gender-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'panlex/diminutives-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'panlex/social-gender-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'universalwordnet/diminutives-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'universalwordnet/social-gender-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'unsup-nn/diminutives-cs2oth.tsv' --has_header 'no'
# python3 morpho_annot_and_filter.py --input_file 'unsup-nn/social-gender-cs2oth.tsv' --has_header 'no'
# python3 morpho_annot_and_filter.py --input_file 'treq/diminutives-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'treq/social-gender-cs2oth.tsv' --has_header 'yes'
# python3 morpho_annot_and_filter.py --input_file 'parallel-corpora/diminutives-cs2oth.tsv' --has_header 'no'
# python3 morpho_annot_and_filter.py --input_file 'parallel-corpora/social-gender-cs2oth.tsv' --has_header 'no'


# format of logs
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_file')
parser.add_argument('--has_header', choices=('yes', 'no'))
args = parser.parse_args()


# function: obtain morphological analysis for the seven languages using UDPipe
def get_analysis(entry, lang):
    models = {
        'czech': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=czech-pdt-ud-2.10-220711&data={entry}',
        'english': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=english-ewt-ud-2.10-220711&data={entry}',
        'german': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=german-hdt-ud-2.10-220711&data={entry}',
        'russian': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=russian-syntagrus-ud-2.10-220711&data={entry}',
        'french': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=french-gsd-ud-2.10-220711&data={entry}',
        'spanish': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=spanish-ancora-ud-2.10-220711&data={entry}',
        'dutch': f'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&model=dutch-alpino-ud-2.10-220711&data={entry}'
    }

    try:
        result = json.loads(requests.get(models[lang]).text)['result']
    except:
        logging.info(f'Waiting {waiting_time*2} seconds.')
        time.sleep(waiting_time)
        try:
            result = json.loads(requests.get(models[lang]).text)['result']
        except:
            return 'None'

    if not result:
        return 'None'

    analysed = list()
    for line in result.split('\n'):
        if line.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            line = line.strip().split('\t')
            analysed.append(line[3])
    return entry + '|' + '|'.join(analysed)


# process the input file and store results
current_request, maximum_requests, waiting_time = 0, 100, 5
name_file_output = args.input_file.replace('.tsv', '-filtred-with-pos.tsv')

with open(args.input_file, mode='r', encoding='U8') as input_file, \
     open(name_file_output, mode='w', encoding='U8') as output_file:
    
    # skip header if necessary
    if args.has_header == 'yes':
        header1 = next(input_file)
        print(header1.strip(), file=output_file)
        header2 = next(input_file)
        print(header2.strip(), file=output_file)

    # process file
    for line in input_file:
        # store processed data in output_line
        # [
        #   cs, cs2en, cs2de, cs2nl, cs2ru, cs2es, cs2fr, en2cs,
        #   de2cs, nl2cs, ru2cs, es2cs, fr2cs
        # ]
        output_line = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        # load original data
        line = line.rstrip('\n').split('\t')

        # resolve capitalisation of all languages except for German
        for idx in range(len(line)):
            if idx != 2:
                line[idx] = line[idx].lower()

        # preproces original data
        line = [item.split(';') for item in line]

        # annotate (1) and filter (2)
        for idx, entries in enumerate(line):
            # 1. annotate
            # skip original Czech
            if idx == 0:
                output_line[idx].append(entries[0])
                continue

            # skip translated Czech
            if idx > 6:
                for item in entries:
                    output_line[idx].append(item)
                continue

            # process relevant translations
            for entry in entries:
                # annotation
                if entry != '':
                    # waiting time for not overlading server
                    if current_request % maximum_requests == 0 and current_request != 0:
                        logging.info(f'Waiting {waiting_time} seconds.')
                        time.sleep(waiting_time)
                    
                    # annotation
                    logging.info('Annotating {language}: {entry}'.format(entry=entry, language={1: 'en', 2: 'de', 3: 'nl', 4: 'ru', 5: 'es', 6: 'fr'}[idx]))
                    annotated = get_analysis(
                        entry,
                        {1: 'english', 2: 'german', 3: 'dutch', 4: 'russian', 5: 'spanish', 6: 'french'}[idx]
                    )
                    current_request += 1
            
                    # 2. filter out
                    if '|NOUN' in annotated:
                        output_line[idx].append(annotated)
                    else:
                        logging.info(f'Excluded: {entry} (annotated as: {annotated})')
                else:
                    output_line[idx].append('')

        # store annotated and filtered line
        print(*[';'.join(entries) for entries in output_line], sep='\t', file=output_file)
