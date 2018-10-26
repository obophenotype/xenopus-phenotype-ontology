import sys
import pandas as pd
import os
import math

tsv = sys.argv[1]
id_map = sys.argv[2]
reserved_ids = sys.argv[3]
accession = int(sys.argv[4])
prefix = sys.argv[5]

# tsv = "/ws/xenopus-phenotype-ontology/src/patterns/data/auto/abnormal.tsv"
# id_map = "/ws/xenopus-phenotype-ontology/src/scripts/id_map.tsv"
# reserved_ids = "/ws/xenopus-phenotype-ontology/src/ontology/reserved_iris.txt"
# accession = int("9898")
# prefix = "http://purl.obolibrary.org/obo/XPO_"

maxid = 9999999
pattern = os.path.basename(tsv)

def get_highest_id(ids):
    global prefix
    x = [i.replace(prefix, "").lstrip("0") for i in ids]
    x = [s for s in x if s!='']
    if len(x)==0:
        x=[0,]
    x = [int(i) for i in x]
    return max(x)


def generate_id(i):
    global startid, maxid
    if(isinstance(i,str)):
        if(i.startswith(prefix)):
            return i
    startid = startid + 1
    if startid>maxid:
        raise ValueError('The ID space has been exhausted (maximum 10 million). Order a new one!')
    id = prefix+str(startid).zfill(7)
    return id


def add_id_column(df):
    global df_ids, pattern
    if 'defined_class' in df.columns:
        df = df.drop(['defined_class'], axis=1)
    if 'iri' in df.columns:
        df = df.drop(['iri'], axis=1)
    df['pattern'] = pattern
    df['id'] = df.apply('-'.join, axis=1)
    if df_ids.empty:
        df['iri'] = ""
    else:
        df = pd.merge(df, df_ids, on='id', how='left')
    df['defined_class'] = [generate_id(i) for i in df['iri']]
    x = df[['defined_class','id']]
    x.columns = ['iri','id']
    df_ids = pd.concat([df_ids,x])
    df_ids = df_ids.drop_duplicates()
    df = df.drop(['pattern', 'id','iri'], axis=1)
    return df


# Load data
df = pd.read_csv(tsv, sep='\t')
df_ids = pd.read_csv(id_map, sep='\t')
df_ids = df_ids.drop_duplicates()

with open(reserved_ids) as f:
    ids = f.readlines()

ids = [x.strip() for x in ids]
ids = [s for s in ids if s.startswith(prefix)]


# compute next assignable id
startid = get_highest_id(ids)
if startid<accession:
    startid=accession

# create ids in df
df = add_id_column(df)

ids=list(set(ids+df_ids['iri'].tolist()))
# wherever there is NULL assign new id starting with start id, make sure that value is then appended to df_ids and ids

df.to_csv(tsv, sep = '\t', index=False)
df_ids.to_csv(id_map, sep = '\t', index=False)
with open(reserved_ids, 'w') as f:
    for item in ids:
        f.write("%s\n" % item)