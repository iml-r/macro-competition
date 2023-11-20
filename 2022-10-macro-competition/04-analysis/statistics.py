#!/usr/bin/env python3
# coding: utf-8

# commands:
# python3 statistics.py --input_files_before $(ls -1 ../01-translation/01-1-statistics-before-filtering/*) --input_files_after $(ls -1 ../01-translation/01-2-statistics-after-filtering/*) --translation_counts_before_after_plot statistics/translation-counts.pdf --translation_counts_complete_plot statistics/translation-counts-complete.pdf --translation_counts_candidates_plot statistics/translation-counts-candidates.pdf --translation_counts_exact_vs_included_after_plot statistics/translation-counts-exact_vs_included-after.pdf --translation_counts_include_neutral_after_plot statistics/translation-counts-include-neutral-after.pdf


import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--input_files_before', nargs='+')
parser.add_argument('--input_files_after', nargs='+')
parser.add_argument('--translation_counts_before_after_plot')
parser.add_argument('--translation_counts_complete_plot')
parser.add_argument('--translation_counts_candidates_plot')
parser.add_argument('--translation_counts_exact_vs_included_after_plot')
parser.add_argument('--translation_counts_include_neutral_after_plot')

args = parser.parse_args()

sns.set(font_scale=2.2)

data_per_source = defaultdict(list)

# load data before
data_per_language_before = defaultdict(list)
for path in args.input_files_before:
    name = path.replace('../01-translation/01-1-statistics-before-filtering/', '').replace('.tsv', '').split('-')
    source = {'google': 'Google', 'panlex': 'PanLex', 'parallel': 'SD', 'treq': 'Treq', 'unsup': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet'}[name[0]]
    concept = 'diminutives' if 'diminution' in name else 'social-gender'
    
    with open(path, mode='r', encoding='U8') as input_file:
        header = next(input_file).rstrip('\n').split('\t')[1:]

        sub_matrix = defaultdict()
        for line in input_file:
            line = line.rstrip('\n').split('\t')

            if len(line[0]) < 2:
                continue

            if line[0] == 'kolik_prekladu_pro_vsechny_jazyky':
                data_per_source['concept'].append(concept)
                data_per_source['source'].append(source)
                data_per_source['before'].append(int(line[1]))
            else:
                sub_matrix[line[0]] = line[1:]
        
        for lang in header:
            data_per_language_before['language'].append({'English': 'EN (before)', 'German': 'DE (before)', 'Dutch': 'NL (before)', 'Russian': 'RU (before)', 'French': 'FR (before)', 'Spanish': 'ES (before)'}[lang])
            data_per_language_before['concept'].append(concept)
            data_per_language_before['source'].append(source)
        
        for key, values in sub_matrix.items():
            for idx in range(len(values)):
                data_per_language_before[key].append(float(values[idx]))

df_data_per_language_before = pd.DataFrame.from_dict(dict(data_per_language_before))


# load data after
data_per_language_after = defaultdict(list)
for path in args.input_files_after:
    name = path.replace('../01-translation/01-2-statistics-after-filtering/', '').replace('.tsv', '').split('-')
    source = {'google': 'Google', 'panlex': 'PanLex', 'parallel': 'SD', 'treq': 'Treq', 'unsup': 'ND', 'universalwordnet': 'UWN', 'cognet': 'CogNet'}[name[0]]
    concept = 'diminutives' if 'diminution' in name else 'social-gender'
    
    with open(path, mode='r', encoding='U8') as input_file:
        header = next(input_file).rstrip('\n').split('\t')[1:]

        sub_matrix = defaultdict()
        for line in input_file:
            line = line.rstrip('\n').split('\t')

            if len(line[0]) < 2:
                continue

            if line[0] == 'kolik_prekladu_pro_vsechny_jazyky':
                data_per_source['after'].append(int(line[1]))
            else:
                sub_matrix[line[0]] = line[1:]
        
        for lang in header:
            data_per_language_after['language'].append({'English': 'EN (after)', 'German': 'DE (after)', 'Dutch': 'NL (after)', 'Russian': 'RU (after)', 'French': 'FR (after)', 'Spanish': 'ES (after)'}[lang])
            data_per_language_after['concept'].append(concept)
            data_per_language_after['source'].append(source)
        
        for key, values in sub_matrix.items():
            for idx in range(len(values)):
                data_per_language_after[key].append(float(values[idx]))

df_data_per_language_after = pd.DataFrame.from_dict(dict(data_per_language_after))


df_data_per_source = pd.DataFrame.from_dict(dict(data_per_source))


# exclude cognet and universalwordnet
df_data_per_language_before = df_data_per_language_before[(df_data_per_language_before['source'] != 'CogNet') & (df_data_per_language_before['source'] != 'UWN')]
df_data_per_language_after = df_data_per_language_after[(df_data_per_language_after['source'] != 'CogNet') & (df_data_per_language_after['source'] != 'UWN')]
df_data_per_source = df_data_per_source[(df_data_per_source['source'] != 'CogNet') & (df_data_per_source['source'] != 'UWN')]
# print(df_data_per_language_before)
# print(df_data_per_language_after)
# print(df_data_per_source)


# translation_counts_complete_plot
df_to_plot = df_data_per_source[df_data_per_source["concept"] == "social-gender"]
df_to_plot.loc[len(df_to_plot.index)] = ['social-gender', 'Merged', 8108, 619]

plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(x="before", y="source", data=df_to_plot.sort_values("before", ascending=False), label="Before", color="b")

sns.set_color_codes("muted")
sns.barplot(x="after", y="source", data=df_to_plot.sort_values("before", ascending=False), label="After", color="b", width=0.4)

plt.ylabel("Translation source")
plt.xlabel("Number of Czech units translated to all other languages")
plt.legend(ncol=2, loc="lower right", frameon=False)
plt.savefig(args.translation_counts_complete_plot.replace('.pdf', '-social-gender.pdf'), bbox_inches='tight')
plt.clf()


df_to_plot = df_data_per_source[df_data_per_source["concept"] == "diminutives"]
df_to_plot.loc[len(df_to_plot.index)] = ['diminutives', 'Merged', 3912, 930]

plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(x="before", y="source", data=df_to_plot.sort_values("before", ascending=False), label="Before", color="r")

sns.set_color_codes("muted")
sns.barplot(x="after", y="source", data=df_to_plot.sort_values("before", ascending=False), label="After", color="r", width=0.4)

plt.ylabel("Translation source")
plt.xlabel("Number of Czech units translated to all other languages")
plt.legend(ncol=2, loc="lower right", frameon=False)
plt.savefig(args.translation_counts_complete_plot.replace('.pdf', '-diminution.pdf'), bbox_inches='tight')
plt.clf()


# translation_counts_before_after_plot
plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs", hue="language", data=df_data_per_language_before[df_data_per_language_before["concept"] == "diminutives"], color="r")

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs", hue="language", data=df_data_per_language_after[df_data_per_language_after["concept"] == "diminutives"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=2, loc="upper right", frameon=False)
plt.savefig(args.translation_counts_before_after_plot.replace('.pdf', '-cs2oth2cs-diminution.pdf'), bbox_inches='tight')
plt.clf()


plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs", hue="language", data=df_data_per_language_before[df_data_per_language_before["concept"] == "social-gender"], color="r")

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_se_najde_prekladu_z_cs_pres_ostatni_do_cs", hue="language", data=df_data_per_language_after[df_data_per_language_after["concept"] == "social-gender"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=2, loc="upper right", frameon=False)
plt.savefig(args.translation_counts_before_after_plot.replace('.pdf', '-cs2oth2cs-social-gender.pdf'), bbox_inches='tight')
plt.clf()


# translation_counts_candidates_plot
plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni", hue="language", data=df_data_per_language_before[df_data_per_language_before["concept"] == "diminutives"], color="r")

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni", hue="language", data=df_data_per_language_after[df_data_per_language_after["concept"] == "diminutives"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Average number of translation equivalents\nCzech -> other languages")
plt.legend(ncol=1, loc="upper left", frameon=False)
plt.savefig(args.translation_counts_candidates_plot.replace('.pdf', '-cs2oth-diminution.pdf'), bbox_inches='tight')
plt.clf()


plt.figure(figsize=(15,15))

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni", hue="language", data=df_data_per_language_before[df_data_per_language_before["concept"] == "social-gender"], color="r")

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="jaky_je_prumerny_pocet_kandidatu_pri_cs_do_ostatni", hue="language", data=df_data_per_language_after[df_data_per_language_after["concept"] == "social-gender"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Average number of translation equivalents\nCzech -> other languages")
plt.legend(ncol=1, loc="upper left", frameon=False)
plt.savefig(args.translation_counts_candidates_plot.replace('.pdf', '-cs2oth-social-gender.pdf'), bbox_inches='tight')
plt.clf()


# translation_counts_exact_vs_included_after_plot
plt.figure(figsize=(15,15))

languages = df_data_per_language_after['language']
languages = [lang.replace('(after)', '(include)') for lang in languages]
to_plot = df_data_per_language_after.copy()
to_plot['language'] = languages

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu", hue="language", data=to_plot[to_plot["concept"] == "diminutives"], color="r")

languages = df_data_per_language_after['language']
languages = [lang.replace('(after)', '(exact)') for lang in languages]
to_plot = df_data_per_language_after.copy()
to_plot['language'] = languages

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu", hue="language", data=to_plot[to_plot["concept"] == "diminutives"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=1, loc="upper left", frameon=False)
plt.savefig(args.translation_counts_exact_vs_included_after_plot.replace('.pdf', '-cs2oth2cs-diminution.pdf'), bbox_inches='tight')
plt.clf()


plt.figure(figsize=(15,15))

languages = df_data_per_language_after['language']
languages = [lang.replace('(after)', '(include)') for lang in languages]
to_plot = df_data_per_language_after.copy()
to_plot['language'] = languages

sns.set_color_codes("pastel")
sns.barplot(palette="pastel", x="source", y="kolik_kompletnich_prekladu_ma_soucasti_pozadovanou_formu", hue="language", data=to_plot[to_plot["concept"] == "social-gender"], color="r")

languages = df_data_per_language_after['language']
languages = [lang.replace('(after)', '(exact)') for lang in languages]
to_plot = df_data_per_language_after.copy()
to_plot['language'] = languages

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_kompletnich_prekladu_ma_pouze_pozadovanou_formu", hue="language", data=to_plot[to_plot["concept"] == "social-gender"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=1, loc="upper left", frameon=False)
plt.savefig(args.translation_counts_exact_vs_included_after_plot.replace('.pdf', '-cs2oth2cs-social-gender.pdf'), bbox_inches='tight')
plt.clf()


# translation_counts_include_neutral_after_plot
plt.figure(figsize=(15,15))

languages = df_data_per_language_after['language']
languages = [lang.replace('(after)', '') for lang in languages]
to_plot = df_data_per_language_after.copy()
to_plot['language'] = languages

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu", hue="language", data=to_plot[to_plot["concept"] == "diminutives"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=1, loc="upper right", frameon=False)
plt.savefig(args.translation_counts_include_neutral_after_plot.replace('.pdf', '-diminution.pdf'), bbox_inches='tight')
plt.clf()


plt.figure(figsize=(15,15))

sns.set_color_codes("muted")
sns.barplot(palette="muted", x="source", y="kolik_kompletnich_prekladu_ma_soucasti_neutralni_formu", hue="language", data=to_plot[to_plot["concept"] == "social-gender"], color="r")

plt.xlabel("Translation source")
plt.ylabel("Number of translations\nCzech -> other languages -> Czech")
plt.legend(ncol=1, loc="upper right", frameon=False)
plt.savefig(args.translation_counts_include_neutral_after_plot.replace('.pdf', '-social-gender.pdf'), bbox_inches='tight')
plt.clf()
