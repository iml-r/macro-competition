#!/usr/bin/env python3
# coding: utf-8

# commands:
# python3 competition.py --distributions_plot individual-distributions/plot-.pdf --distributions_table individual-distributions/table.tsv --correspondence_plot correspondence/plot-.pdf --entropy_plot individual-distributions/plot-entropy-.pdf


import argparse
import pandas as pd
import numpy as np
from math import log2
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import seaborn as sns
from collections import defaultdict, Counter
from scipy.stats import wasserstein_distance


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--distributions_table')
parser.add_argument('--distributions_plot')
parser.add_argument('--correspondence_plot')
parser.add_argument('--entropy_plot')
args = parser.parse_args()

sns.set(font_scale=1.5)

##Entropy
def entropy(Y):
    """
    Also known as Shanon Entropy
    Reference: https://en.wikipedia.org/wiki/Entropy_(information_theory)
    """
    en = 0
    for d in Y:
        if d == 0:
            pass
        else:
            en += d * log2(d)
    return -1*en
    # unique, count = np.unique(Y, return_counts=True, axis=0)
    # prob = count/len(Y)
    # en = np.sum((-1)*prob*np.log2(prob))
    # return en


## EMD
def emd(a, b):
    earth = 0
    earth1 = 0
    diff = 0
    s= len(a)
    su = []
    diff_array = []
    for i in range (0,s):
        diff = a[i]-b[i]
        diff_array.append(diff)
        diff = 0
    for j in range (0,s):
        earth = (earth + diff_array[j])
        earth1= abs(earth)
        su.append(earth1)
    emd_output = sum(su)/(s-1)
    return emd_output

# load data
statistics = defaultdict(list)
for semantic_concept in ('diminutives', 'social-gender'):
    for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        for language in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
            with open('../03-annotation/' + translation_source + '/' + semantic_concept + '-' + language + '-final.tsv', mode='r', encoding='U8') as input_file:
                for line in input_file:
                    word, strategy = line.rstrip().split('\t')
                    statistics['language'].append(language.upper())
                    statistics['semantic_concept'].append(semantic_concept)
                    statistics['translation_source'].append({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source])
                    statistics['naming_strategy'].append(strategy)
                    statistics['naming_unit'].append(word)
statistics = pd.DataFrame.from_dict(dict(statistics))


# calculate distributions
final_counts = defaultdict(list)
for semantic_concept in ('diminutives', 'social-gender'):
    for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        for language in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):

            counts = Counter(
                    statistics[
                        (statistics['language'] == language.upper()) &
                        (statistics['semantic_concept'] == semantic_concept) &
                        (statistics['translation_source'] == {'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source])
                    ]['naming_strategy']
            )

            for naming_strategy in ('Compound', 'Derivative', 'Unmarked', 'Unmotivated', 'Phrase'):
                final_counts['semantic_concept'].append(semantic_concept)
                final_counts['translation_source'].append({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source])
                final_counts['language'].append(language.upper())
                final_counts['naming_strategy_n'].append(counts.get(naming_strategy, 0))
                final_counts['naming_strategy'].append(naming_strategy)
                final_counts['naming_strategy_r'].append(counts.get(naming_strategy, 0) / sum(counts.values()))

df_final_counts = pd.DataFrame.from_dict(dict(final_counts))


# store plot
for concept in ('social-gender', 'diminutives'):
    for source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        plt.figure(figsize=(20,20))
        a = sns.catplot(
            data=df_final_counts[(df_final_counts['semantic_concept'] == concept) & (df_final_counts['translation_source'] == {'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[source])], kind="bar",
            x="naming_strategy", y="naming_strategy_r", hue="language",
            errorbar="ci", palette="dark", alpha=.6, height=6
        )
        a._legend.remove()
        plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[concept])
        plt.legend(ncol=1, title='', bbox_to_anchor=(1.25, 0.6), loc='center right', borderaxespad=0, frameon=False)
        plt.xlabel('Naming strategy')
        plt.xticks(rotation=20)
        plt.ylabel('Relative number of naming units')
        if source == '03-1-merged/merged-data':
            source = 'merged'
        plt.savefig(args.distributions_plot.replace('.pdf', source + '-' + concept + '.pdf'), bbox_inches='tight')
        plt.clf()

for concept in ('social-gender', 'diminutives'):
    for source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        plt.figure(figsize=(20,20))
        a = sns.catplot(
            data=df_final_counts[(df_final_counts['semantic_concept'] == concept) & (df_final_counts['translation_source'] == {'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[source])], kind="bar",
            x="language", y="naming_strategy_r", hue="naming_strategy",
            errorbar="ci", palette="dark", alpha=.6, height=6
        )
        a._legend.remove()
        plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[concept])
        plt.legend(ncol=2, title='', bbox_to_anchor=(0.5,-0.15), loc='upper center', borderaxespad=0, frameon=False)
        plt.xlabel('Language')
        plt.ylabel('Relative number of naming units')
        if source == '03-1-merged/merged-data':
            source = 'merged'
        plt.savefig(args.distributions_plot.replace('.pdf', source + '-' + concept + '-2.pdf'), bbox_inches='tight')
        plt.clf()

# store table
with open(args.distributions_table, mode='w', encoding='U8') as output_file:
    for semantic_concept in ('diminutives', 'social-gender'):
        distributions_individual = list()
        for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
            row = list()
            row.append({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source])
            for language in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
                for strategy in ('Derivative', 'Compound', 'Phrase', 'Unmotivated', 'Unmarked'):
                    data = df_final_counts[
                        (df_final_counts['semantic_concept'] == semantic_concept) &
                        (df_final_counts['translation_source'] == {'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]) &
                        (df_final_counts['language'] == language.upper())
                    ]
                    idx = list(data['naming_strategy']).index(strategy)
                    row.append(str(list(data['naming_strategy_n'])[idx]))
            row.append('\\\\')
            distributions_individual.append(' & '.join(row))
        print('', *('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'), '\\\\', sep=' & ', file=output_file)
        print(semantic_concept, *('Derivative', 'Compound', 'Phrase', 'Unmotivated', 'Unmarked')*7, '\\\\', sep=' & ', file=output_file)
        print(*distributions_individual, sep='\n', file=output_file)
        print('', file=output_file)


# calculate correspondence
sets_of_distributions = defaultdict(lambda: defaultdict(lambda: defaultdict()))
entropies = defaultdict(lambda: defaultdict(lambda: defaultdict()))
for semantic_concept in ('diminutives', 'social-gender'):
    for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        for language in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
            distribs = df_final_counts[
                    (df_final_counts['language'] == language.upper()) &
                    (df_final_counts['semantic_concept'] == semantic_concept) &
                    (df_final_counts['translation_source'] == {'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source])
                ]['naming_strategy_r']
            
            sets_of_distributions[semantic_concept][{'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]][language.upper()] = list(distribs)
            entropies[semantic_concept][{'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]][language.upper()] = entropy(list(distribs))


# plot results of correspondences
for semantic_concept in ('diminutives', 'social-gender'):
    for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        data_to_plot = defaultdict(lambda: defaultdict(float))
        for lang1 in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
            for lang2 in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
                distance = emd(  # wasserstein_distance(
                    sets_of_distributions[semantic_concept][{'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]][lang1.upper()],
                    sets_of_distributions[semantic_concept][{'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]][lang2.upper()]
                )
                data_to_plot[lang1.upper()][lang2.upper()] = distance
        
        data_to_plot = pd.DataFrame(data_to_plot)

        if semantic_concept == 'diminutives':
            # heatmap
            ax = sns.heatmap(data_to_plot, cmap=sns.cubehelix_palette(as_cmap=True), vmin=0, vmax=1)
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '-1.pdf'), bbox_inches='tight')
            plt.clf()

            # dendrogram
            Z = linkage(data_to_plot, 'ward')
            dendrogram(Z, labels=data_to_plot.index, color_threshold=0, above_threshold_color='r')
            plt.xlabel('Language')
            plt.ylabel('Distrance')
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '-2.pdf'), bbox_inches='tight')
            plt.clf()

            # heatmap + dendrogram
            ax = sns.clustermap(data_to_plot, center=0, cmap=sns.cubehelix_palette(as_cmap=True), figsize=(5, 5), method='median', standard_scale=1)
            ax.ax_row_dendrogram.remove()
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '.pdf'), bbox_inches='tight')
            plt.clf()
        else:
            # heatmap
            ax = sns.heatmap(data_to_plot, cmap=sns.cubehelix_palette(start=2.8, rot=.1, as_cmap=True), vmin=0, vmax=1)
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '-1.pdf'), bbox_inches='tight')
            plt.clf()

            # dendrogram
            Z = linkage(data_to_plot, 'ward')
            dendrogram(Z, labels=data_to_plot.index, color_threshold=0)
            plt.xlabel('Language')
            plt.ylabel('Distrance')
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '-2.pdf'), bbox_inches='tight')
            plt.clf()

            # heatmap + dendrogram
            ax = sns.clustermap(data_to_plot, center=0, cmap=sns.cubehelix_palette(start=2.8, rot=.1, as_cmap=True), figsize=(5, 5), method='median', standard_scale=1)
            ax.ax_row_dendrogram.remove()
            plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged', 'merged': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
            if translation_source == '03-1-merged/merged-data':
                translation_source = 'merged'
            plt.savefig(args.correspondence_plot.replace('.pdf', semantic_concept + '-' + translation_source + '.pdf'), bbox_inches='tight')
            plt.clf()


# plot results of entopies
for semantic_concept in ('diminutives', 'social-gender'):
    for translation_source in ('google', 'panlex', 'parallel-corpora', 'treq', 'unsup-nn', 'cognet', 'universalwordnet', '03-1-merged/merged-data'):
        data_to_plot = defaultdict(lambda: defaultdict(float))
        for lang1 in ('cs', 'en', 'de', 'nl', 'fr', 'es', 'ru'):
            data_to_plot[lang1.upper()] = entropies[semantic_concept][{'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source]][lang1.upper()]
        data_to_plot = pd.DataFrame({'language': list(data_to_plot.keys()), 'entropy': list(data_to_plot.values())})

        sns.barplot(x="language", y="entropy", data=data_to_plot)
        plt.title({'google': 'Google', 'panlex': 'PanLex', 'parallel-corpora': 'SD', 'treq': 'Treq', 'unsup-nn': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet', '03-1-merged/merged-data': 'Merged'}[translation_source] + ' : ' + {'diminutives': 'Diminution', 'social-gender': 'Social gender'}[semantic_concept])
        plt.ylabel("Entropy")
        plt.xlabel("Language")
        if translation_source == '03-1-merged/merged-data':
            translation_source = 'merged'
        plt.savefig(args.entropy_plot.replace('.pdf', semantic_concept + '-' + translation_source + '.pdf'), bbox_inches='tight')
        plt.clf()
