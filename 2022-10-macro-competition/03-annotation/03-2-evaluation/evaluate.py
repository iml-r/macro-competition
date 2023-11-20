#!/usr/bin/env python3
# coding: utf-8

import argparse
from collections import defaultdict


# python3 evaluate.py --reference_data '../03-0-evaluation-data/eval-data-XX.tsv' --predicted_data '../03-0-evaluation-data/eval-data-XX.tsv' --results 'prediction-same-as-reference.tsv'
# python3 evaluate.py --reference_data '../03-0-evaluation-data/eval-data-XX.tsv' --predicted_data '../03-0-evaluation-data/annotated-by-tool/eval-by-tool-XX.tsv' --results 'prediction-only-by-tool.tsv'
# python3 evaluate.py --reference_data '../03-0-evaluation-data/eval-data-XX.tsv' --predicted_data '../03-0-evaluation-data/annotated-by-tool/eval-by-tool-XX-final.tsv' --results 'prediction-after-procedure.tsv'
# python3 evaluate.py --reference_data '../03-0-evaluation-data/eval-data-XX.tsv' --predicted_data '../03-0-evaluation-data/annotated-random/eval-data-XX-final.tsv' --results 'prediction-baseline.tsv'


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--reference_data')
parser.add_argument('--predicted_data')
parser.add_argument('--results')
args = parser.parse_args()


# load data
def load_data(path):
    data = defaultdict(lambda: defaultdict())
    for language in ('cs', 'en', 'de', 'nl', 'ru', 'fr', 'es'):
        with open(path.replace('XX', language), mode='r', encoding='U8') as input_file:
            for line in input_file:
                line = line.strip().split('\t')
                data[line[0]][language] = line[1]
    return data


reference_data = load_data(args.reference_data)  # load referenced data
predicted_data = load_data(args.predicted_data)  # load predicted data


# calculate accuracy for individual languages
accuracy = defaultdict()
for language in ('cs', 'en', 'de', 'nl', 'ru', 'fr', 'es'):
    n_all, n_correct = 0, 0
    for word in list(reference_data.keys()):
        refe = reference_data.get(word, {}).get(language, None)
        pred = predicted_data.get(word, {}).get(language, None)

        if refe == pred:
            n_correct += 1
        n_all += 1

        # if language == 'es' and refe != pred:
        #     print(word, refe, pred)

    accuracy[language] = n_correct / n_all



# calculate balanced accuracy for individual languages
ballanced_accuracy = defaultdict()
for language in ('cs', 'en', 'de', 'nl', 'ru', 'fr', 'es'):
    der_correct, der_all, com_correct, com_all, unmot_correct, unmot_all = 0, 0, 0, 0, 0, 0
    for word in list(reference_data.keys()):
        refe = reference_data.get(word, {}).get(language, None)
        pred = predicted_data.get(word, {}).get(language, None)

        if refe == pred:
            if refe == 'Derivative':
                der_correct += 1
            elif refe == 'Compound':
                com_correct += 1
            elif refe == 'Unmotivated':
                unmot_correct += 1

        if refe == 'Derivative':
            der_all += 1
        elif refe == 'Compound':
            com_all += 1
        elif refe == 'Unmotivated':
            unmot_all += 1

    der = der_correct/der_all if der_all > 0 else 0
    com = com_correct/com_all if com_all > 0 else 0
    unm = unmot_correct/unmot_all if unmot_all > 0 else 0
    ballanced_accuracy[language] = (der + com + unm) / 3


# Precision
precision = defaultdict()
for language in ('cs', 'en', 'de', 'nl', 'ru', 'fr', 'es'):
    der_correct, der_incor, com_correct, com_incor, unmot_correct, unmot_incor = 0, 0, 0, 0, 0, 0
    for word in list(reference_data.keys()):
        refe = reference_data.get(word, {}).get(language, None)
        pred = predicted_data.get(word, {}).get(language, None)

        if refe == pred:
            if refe == 'Derivative':
                der_correct += 1
            elif refe == 'Compound':
                com_correct += 1
            elif refe == 'Unmotivated':
                unmot_correct += 1
        else:
            if pred == 'Derivative':
                der_incor += 1
            elif pred == 'Compound':
                com_incor += 1
            elif pred == 'Unmotivated':
                unmot_incor += 1

    der = der_correct / (der_correct + der_incor) if der_correct + der_incor > 0 else 0
    com = com_correct / (com_correct + com_incor) if com_correct + com_incor > 0 else 0
    unm = unmot_correct / (unmot_correct + unmot_incor) if unmot_correct + unmot_incor > 0 else 0
    precision[language] = (der + com + unm) / 3

    # if language == 'es':
    #     print('Der:', der)
    #     print('Com:', com)
    #     print('Unm:', unm)


# Recall
recall = defaultdict()
for language in ('cs', 'en', 'de', 'nl', 'ru', 'fr', 'es'):
    der_correct, der_incor, com_correct, com_incor, unmot_correct, unmot_incor = 0, 0, 0, 0, 0, 0
    for word in list(reference_data.keys()):
        refe = reference_data.get(word, {}).get(language, None)
        pred = predicted_data.get(word, {}).get(language, None)

        if refe == pred:
            if refe == 'Derivative':
                der_correct += 1
            elif refe == 'Compound':
                com_correct += 1
            elif refe == 'Unmotivated':
                unmot_correct += 1
        else:
            if refe == 'Derivative':
                der_incor += 1
            elif refe == 'Compound':
                com_incor += 1
            elif refe == 'Unmotivated':
                unmot_incor += 1

    der = der_correct / (der_correct + der_incor) if der_correct + der_incor > 0 else 0
    com = com_correct / (com_correct + com_incor) if com_correct + com_incor > 0 else 0
    unm = unmot_correct / (unmot_correct + unmot_incor) if unmot_correct + unmot_incor > 0 else 0
    recall[language] = (der + com + unm) / 3

    # if language == 'es':
    #     print('Der:', der)
    #     print('Com:', com)
    #     print('Unm:', unm)


# store results
with open(args.results, mode='w', encoding='U8') as output_file:
    print('Language', 'Acc', 'B-Acc', 'Prec', 'Rec', 'F1', sep=' & ', file=output_file)
    for language in sorted(list(accuracy.keys())):
        print(
            language.upper(), round(accuracy[language], 4), round(ballanced_accuracy[language], 4),
            round(precision[language], 4), round(recall[language], 4),
            round(2*((precision[language] * recall[language]) / (precision[language] + recall[language])), 4),
            sep=' & ', file=output_file)
