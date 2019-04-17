import sys
import pandas as pd
import os

#tsv = sys.argv[1]

tsv = "/ws/xenopus-phenotype-ontology/src/metadata/xenbase_phenotype_annotation.csv"
data_dir = "/ws/xenopus-phenotype-ontology/src/patterns/data/manual/"

obo_prefix = "http://purl.obolibrary.org/obo/"

# Load data
df = pd.read_csv(tsv, sep='\t')

#df_ids.to_csv(id_map, sep = '\t', index=False)
