#!/usr/bin/env python3
# coding: utf-8

import sys
import time
import json
import logging
import itertools
import argparse
import requests


# commands:
# python3 translate_by_treq.py --input_data ../../00-input-data/pairs-of-diminutives.tsv --output_data diminutives-cs2oth.tsv
# python3 translate_by_treq.py --input_data ../../00-input-data/pairs-of-social-gender.tsv --output_data social-gender-cs2oth.tsv


# format of logs
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_data')
parser.add_argument('--output_data')
args = parser.parse_args()


# function: requesting Treq API
def treq_translate(word, source, target):
    """Translate a given data using TreQ translation tool."""
    # select all possible subcorpora for the individual pairs of languages
    available_subsorpora = {
        'cs': {
            'en': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'de': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'nl': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'ru': 'CORE,BIBLE,SUBTITLE,SYNDICATE',
            'fr': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'es': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        },

        'en': {
            'cs': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'de': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'nl': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'ru': 'CORE,BIBLE,SUBTITLE,SYNDICATE',
            'fr': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'es': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        },

        'de': {
            'en': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'cs': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'nl': '',
            'ru': '',
            'fr': '',
            'es': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        },

        'nl': {
            'en': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'de': '',
            'cs': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'ru': '',
            'fr': '',
            'es': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        },

        'ru': {
            'en': 'CORE,BIBLE,SUBTITLE,SYNDICATE',
            'de': '',
            'nl': '',
            'cs': 'CORE,BIBLE,SUBTITLE,SYNDICATE',
            'fr': '',
            'es': 'CORE,SUBTITLE,SYNDICATE'
        },

        'fr': {
            'en': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'de': '',
            'nl': '',
            'ru': '',
            'cs': 'ACQUIS,CORE,BIBLE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'es': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        },

        'es': {
            'en': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'de': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'nl': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'ru': 'CORE,SUBTITLE,SYNDICATE',
            'fr': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE',
            'cs': 'ACQUIS,CORE,EUROPARL,PRESEUROP,SUBTITLE,SYNDICATE'
        }
    }

    subcorpora = available_subsorpora.get(source, {}).get(target, None)
    if subcorpora is None:
        return None

    # request translation
    req = requests.get(
        url=f'https://treq.korpus.cz/api.php?api=true&left={source}&right={target}&viceslovne=true&regularni=false&lemma=true&aJeA=false&hledejKde={subcorpora}&hledejCo={word}&order=percDesc',
    )
    
    # if API does not answer, try it again until getting an answer
    while req.status_code != 200:
        print(req.status_code)
        time.sleep(1)
        req = requests.get(
            url=f'https://treq.korpus.cz/api.php?api=true&left={source}&right={target}&viceslovne=true&regularni=false&lemma=true&aJeA=false&hledejKde={subcorpora}&hledejCo={word}&order=percDesc',
        )
    # print(req.status_code)

    # process answer
    treq = json.loads(
        req.text.strip()
    )['lines']

    return ';'.join([item['righ'] for item in treq])


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
    n = 0
    for line in input_file:
        word, _, _ = line.strip().split('\t')

        logging.info(f'Translation of: {word}')
        if n != 0 and n % 50 == 0:
            wait_time = 5
            logging.info(f'Wainting {wait_time} seconds.')
            time.sleep(wait_time)

        data_line = [
            word,
            treq_translate(word=word, source='cs', target='en'),
            treq_translate(word=word, source='cs', target='de'),
            treq_translate(word=word, source='cs', target='nl'),
            treq_translate(word=word, source='cs', target='ru'),
            treq_translate(word=word, source='cs', target='es'),
            treq_translate(word=word, source='cs', target='fr'),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='en', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='en').split(';')]]))),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='de', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='de').split(';')]]))),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='nl', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='nl').split(';')]]))),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='ru', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='ru').split(';')]]))),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='es', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='es').split(';')]]))),
            ';'.join(list(itertools.chain(*[treq_translate(word=w, source='fr', target='cs').split(';') for w in [item for item in treq_translate(word=word, source='cs', target='fr').split(';')]])))
        ]

        print(*data_line, sep='\t', file=output_file)
        n += 1
