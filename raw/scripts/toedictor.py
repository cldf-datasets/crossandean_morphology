from lingpy import *
from lingpy.compare.partial import *
from lexibase.lexibase import LexiBase


cols = ['concept_id', 'concept_name', 'language_id', 'language_name',
        "language_subgroup", 'value',
        'form', 'segments', 'glottocode', 'concept_concepticon_id',
        'comment']


lex = Partial.from_cldf("../cldf/cldf-metadata.json",
        columns=cols)
lex.partial_cluster(method='sca', threshold=0.45, ref="cogids")
alms = Alignments(lex, ref="cogids")
alms.align()
alms.add_entries("morphemes", "tokens", lambda x: "")
alms.add_entries("subgroup", "language_subgroup", lambda x: x)
alms.add_entries("note", "comment", lambda x: x if x else "")


D = {0: ["doculect", "subgroup", "concept", "value", "form",
    "tokens", "cogids", "morphemes", "alignment", "note"]}
for idx in alms:
    D[idx] = [alms[idx, h] for h in D[0]]
lex = LexiBase(D, dbase="crossandeanm.sqlite3")
lex.create("crossandeanm")
