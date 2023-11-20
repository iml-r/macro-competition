#!/usr/bin/env python3

import argparse
import csv
import pathlib
import sys
import zipfile

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

def parse_args():
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("zip_name", metavar="ZIPFILE", help="A ZIP file with the PanLex CSVs.")
    parser.add_argument("words", type=argparse.FileType("rt", encoding="utf-8"), help="File containing words to translate, in format `word TAB lang-code`.")
    parser.add_argument(
        "--target-langs",
        dest="tgt_langs",
        required=True,
        help="A comma-separated list of languages to translate to."
    )

    return parser.parse_args()

def load_lang_codes(zip_file, dir_name, wanted_lang_codes):
    lang_file = zip_file.open(dir_name + "/langvar.csv")
    #id,lang_code,var_code,mutable,name_expr,script_expr,meaning,region_expr,uid_expr,grp
    #10549,jpn,45,t,24099974,18147719,35686454,26533785,25839634,10547

    lang_types = {"id": np.int32,
                  "lang_code": pd.StringDtype(),
                  "var_code": np.int32,
                  "mutable": CategoricalDtype(categories=["t", "f"], ordered=False),
                  "name_expr": np.int32,
                  "script_expr": np.int32,
                  "meaning": np.int32,
                  "region_expr": np.int32,
                  "uid_expr": np.int32,
                  "grp": np.int32}

    loaded_data = pd.read_csv(lang_file, sep=",", header=0, index_col="id", dtype=lang_types, engine="c", quoting=csv.QUOTE_NONE)
    is_lang_needed = loaded_data["lang_code"].isin(wanted_lang_codes)
    selected_langs = loaded_data[["lang_code", "var_code"]][is_lang_needed]

    langvars = {}

    for x in selected_langs.itertuples(name="Langvar"):
        langvar = str(x.Index)
        if x.lang_code in langvars:
            langvars[x.lang_code].append(langvar)
        else:
            langvars[x.lang_code] = [langvar]

    return langvars

def get_expr_indices(zip_file, dir_name, langvar_to_lang, needed_words_langs):
    """
    Return a Pandas DataFrame of `langvar`s and `text`s corresponding
    to exprs of words from the set of needed_words_langs. The index
    corresponds to the indices of the exprs.
    """
    expr_file = zip_file.open(dir_name + "/expr.csv")
    expr_types = {"id": np.int32,
                  "langvar": pd.StringDtype(),
                  "txt": pd.StringDtype(),
                  "txt_degr": pd.StringDtype()}

    needed_words = {word for word, lang in needed_words_langs}
    word_to_langs = {}
    for word, lang in needed_words_langs:
        # Each word may be found in multiple languages
        if word in word_to_langs:
            word_to_langs[word].append(lang)
        else:
            word_to_langs[word] = [lang]

    needed_data = []

    loaded_data_iter = pd.read_csv(expr_file, sep=",", header=0, index_col="id", dtype=expr_types, engine="c", chunksize=1000, quoting=csv.QUOTE_MINIMAL)
    for loaded_data in loaded_data_iter:
        #print(".", end="", file=sys.stderr)
        # Get only rows corresponding to words that we seek.
        # Note that this filtering overgenerates – it filters by all
        #  words and all languages, but there may be wrong combinations
        #  of word and language included. These will be filtered
        #  afterwards.
        # TODO actually do that extra filtering.
        is_word_needed = loaded_data["txt"].isin(needed_words)
        needed_rows = loaded_data[["langvar", "txt"]][is_word_needed]

        for x in needed_rows.itertuples(name="Expr"):
            #print("Got word {} with langvar {}".format(x.txt, x.langvar), file=sys.stderr)
            for lang in word_to_langs[x.txt]:
                if x.langvar in langvar_to_lang and langvar_to_lang[x.langvar] == lang:
                    needed_data.append(x)

    return pd.DataFrame.from_records(needed_data, index="Index", columns=["Index", "langvar", "txt"])

def expr_to_meanings(zip_file, dir_name, exprs):
    denotation_file = zip_file.open(dir_name + "/denotation.csv")
    denotation_types = {"id": np.int32,
                        "meaning": np.int32,
                        "expr": np.int32}

    meanings = []

    loaded_data_iter = pd.read_csv(denotation_file, sep=",", header=0, index_col="id", dtype=denotation_types, engine="c", chunksize=1000, quoting=csv.QUOTE_NONE)
    for loaded_data in loaded_data_iter:
        needed_rows = loaded_data.join(exprs, on="expr", how="inner")

        if not needed_rows.empty:
            # Add the IDs to the list of all.
            # TODO join with the exprs to keep the origin language and
            #  text.
            #print("Joined", loaded_data, "and", exprs, "got", needed_rows, file=sys.stderr)
            meanings.append(needed_rows)

    return pd.concat(meanings)

def meaning_to_exprs(zip_file, dir_name, meanings):
    denotation_file = zip_file.open(dir_name + "/denotation.csv")
    denotation_types = {"id": np.int32,
                        "meaning": np.int32,
                        "expr": np.int32}

    exprs = []

    loaded_data_iter = pd.read_csv(denotation_file, sep=",", header=0, index_col="id", dtype=denotation_types, engine="c", chunksize=1000, quoting=csv.QUOTE_NONE)
    for loaded_data in loaded_data_iter:
        needed_rows = loaded_data.merge(meanings, on="meaning", how="inner", suffixes=("_xlated", "_orig"))

        if not needed_rows.empty:
            # Add the IDs to the list of all.
            #print("Got meaning(s)", needed_rows["meaning"], file=sys.stderr)
            exprs.append(needed_rows)

    return pd.concat(exprs)

def get_index_expr(zip_file, dir_name, target_langvars, xlated_expr_indices):
    expr_file = zip_file.open(dir_name + "/expr.csv")
    expr_types = {"id": np.int32,
                  "langvar": pd.StringDtype(),
                  "txt": pd.StringDtype(),
                  "txt_degr": pd.StringDtype()}

    needed_words = []

    loaded_data_iter = pd.read_csv(expr_file, sep=",", header=0, index_col="id", dtype=expr_types, engine="c", chunksize=1000, quoting=csv.QUOTE_MINIMAL)
    for loaded_data in loaded_data_iter:
        loaded_data = loaded_data[loaded_data["langvar"].isin(target_langvars)]
        needed_rows = xlated_expr_indices.join(loaded_data, on="expr_xlated", how="inner", lsuffix="_orig", rsuffix="_xlated")

        if not needed_rows.empty:
            # Add the IDs to the list of all.
            needed_words.append(needed_rows)

    return pd.concat(needed_words)

def read_words(f):
    words = []

    for line in f:
        fields = line.rstrip().split("\t")
        assert len(fields) == 2
        # The fields are [word, lang], which is exactly the layout we
        #  need to pass downstream.
        words.append(fields)

    return words

def main(args):
    pd.set_option('display.max_rows', None)

    needed_words = read_words(args.words)
    target_languages = set(args.tgt_langs.split(","))

    source_languages = {l for w, l in needed_words}

    zip_name = args.zip_name
    # Name of the directory within the file.
    dir_name = pathlib.PurePath(zip_name).stem
    zip_file = zipfile.ZipFile(zip_name, mode="r")

    lang_to_langvar = load_lang_codes(zip_file, dir_name, source_languages | target_languages)
    langvar_to_lang = {}
    for lang, langvars in lang_to_langvar.items():
        for langvar in langvars:
            assert langvar not in langvar_to_lang
            langvar_to_lang[langvar] = lang
    #print("Lang codes:", langvar_to_lang, file=sys.stderr)
    target_langvars = set(sum((lang_to_langvar[lang] for lang in target_languages), start=[]))
    #print("Target languages:", target_langvars, file=sys.stderr)

    needed_indices = get_expr_indices(zip_file, dir_name, langvar_to_lang, needed_words)
    #print("Got indices", needed_indices, file=sys.stderr)

    incident_meanings = expr_to_meanings(zip_file, dir_name, needed_indices)
    #print("Got meanings", incident_meanings, file=sys.stderr)

    translated_indices = meaning_to_exprs(zip_file, dir_name, incident_meanings)
    #print("Indices:", translated_indices, file=sys.stderr)

    translated_words = get_index_expr(zip_file, dir_name, target_langvars, translated_indices)

    print("src-text", "src-lang", "tgt-text", "tgt-lang", "tgt-lang-var", sep="\t")
    for x in translated_words.itertuples(name="Translation"):
        print(x.txt_orig, langvar_to_lang[x.langvar_orig], x.txt_xlated, langvar_to_lang[x.langvar_xlated], x.langvar_xlated, sep="\t")

if __name__ == "__main__":
    main(parse_args())
