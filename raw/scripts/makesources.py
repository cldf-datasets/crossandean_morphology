from csvw.dsv import UnicodeDictReader
from collections import defaultdict
from pyedictor import fetch
from lexibase import LexiBase

data = {}
source2lang = defaultdict(set)
out = []
sla = {}
with UnicodeDictReader("crossandeanm.csv", delimiter=",") as reader:
    for i, row in enumerate(reader):
        data[i+1] = row
        source2lang[row["LANGUAGE"]].add(row["SOURCE"])
        out += [[row["LANGUAGE"], row["FORM"], row["SOURCE"]]]
        sla[row["LANGUAGE"], row["FORM"]] = row["SOURCE"]
with open("sourcelookup.tsv", "w") as f:
    f.write("DOCULECT\tFORM\tSOURCE\n")
    for row in out:
        f.write("\t".join(row)+"\n")

for k, vals in source2lang.items():
    if len(vals) > 1:
        print(k, vals)


wl = fetch("crossandeanm", to_lingpy=True,
    columns=["ALIGNMENT", "CONCEPT",
                        "DOCULECT", "FORM", "VALUE",
                        "TOKENS", "COGIDS", "BORROWING", "NOTE",
                        "SOURCE"]
        )
count = 0
for idx, language, form in wl.iter_rows("doculect", "value"):
    if (language, form) in sla:
        wl[idx, "source"] = sla[language, form]
    elif language == 'Apurimac':
        wl[idx, "source"] = 'camacho2006'
    elif language == 'Chachapoyas':
        wl[idx, "source"] = 'taylor1979'
    elif language == 'Imbabura':
        wl[idx, "source"] = 'cole1985'
    else:
        count += 1

print(count)

lex = LexiBase(wl)
lex.db = "crossandeanm-new.sqlite3"
lex.create("crossandeanm")

lex.output('tsv', filename="dummy", ignore="all")

