.SUFFIXES:
.PHONY: all clean mrproper
.SECONDARY:

PANLEX::=panlex-20221001-csv.zip
IN_DATA_DIR::=../../00-input-data

all: translated-social-gender-parents-ces-all.tsv translated-diminutives-parents-ces-all.tsv translated-social-gender-parents-all-ces.tsv translated-diminutives-parents-all-ces.tsv

translated-%-parents-ces-all.tsv: $(IN_DATA_DIR)/pairs-of-%.tsv $(PANLEX) translate_by_panlex.py
	yes ces | paste -d'	' '$<' - | cut -f1,4 | LC_COLLATE=C sort -u | python3 translate_by_panlex.py --target-langs 'deu,eng,fra,nld,rus,spa' '$(PANLEX)' - > '$@'

translated-%-parents-all-ces.tsv: translated-%-parents-ces-all.tsv $(PANLEX) translate_by_panlex.py
	tail -n+2 '$<' | cut -f3,4 | LC_COLLATE=C sort -u | python3 translate_by_panlex.py --target-langs 'ces' '$(PANLEX)' - > '$@'

panlex-%-csv.zip:
	curl -o '$@' 'https://db.panlex.org/$@'

clean:
	rm -f translated-social-gender-parents-ces-all.tsv translated-diminutives-parents-ces-all.tsv
	rm -f translated-social-gender-parents-all-ces.tsv translated-diminutives-parents-all-ces.tsv

mrproper: clean
	rm -f panlex-*-csv.zip
