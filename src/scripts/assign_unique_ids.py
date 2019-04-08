import sys
import pandas as pd
import os

tsv = sys.argv[1]
id_map = sys.argv[2]
reserved_ids = sys.argv[3]
accession = int(sys.argv[4])
prefix = sys.argv[5]

#tsv = "/ws/xenopus-phenotype-ontology/src/patterns/data/manual/decreasedProcessQualityInLocation.tsv"
#id_map = "/ws/xenopus-phenotype-ontology/src/patterns/id_map.tsv"
#reserved_ids = "/ws/xenopus-phenotype-ontology/src/patterns/reserved_iris.txt"
#accession = int("9898")
#prefix = "http://purl.obolibrary.org/obo/XPO_"
obo_prefix = "http://purl.obolibrary.org/obo/"

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

# For the following function to work properly it is important to note that there should be absolutely no columns in teh tsv file other than the defi
# defined_class and columns whos names end with _label other than the ones that contribute to the identity of the entity in question

def add_id_column(df):
    global df_ids, pattern
    #df = pd.read_csv(tsv, sep='\t')
    if 'defined_class' not in df.columns:
        df['defined_class'] = ''

    df_ids['iritemp001'] = df_ids['iri'] #we change the iri column name here temporarily to make merging and amending easier. Is changed back to normal at the end of the function
    df_ids = df_ids.drop("iri", axis=1)

    if 'iritemp001' in df.columns:
        df = df.drop(['iritemp001'], axis=1)
        print("Warning: There was a colum labelled iritemp001, which is reserved vocabulary and will be overwritten")

    df['pattern'] = pattern
    cols = df.columns
    idcolumns = [i for i in cols if not i.endswith('label')]
    idcolumns.remove("defined_class")

    df_copy = df.copy()

    for col in idcolumns:
        df_copy[col] = [i.replace(obo_prefix,"") for i in df_copy[col]]
        df_copy[col] = [i.replace("_", ":") for i in df_copy[col]]

    df['id'] = df_copy[idcolumns].apply('-'.join, axis=1)

    if df_ids.empty:
        df['iritemp001'] = ""
    else:
        df = pd.merge(df, df_ids, on='id', how='left')

    df = df.replace(pd.np.nan, '', regex=True)
    #df.loc[(df['defined_class'] != '') & (df['iritemp001'] == ''), 'iritemp001'] = df['']
    broken = pd.np.where((df['defined_class'] != '') & (df['iritemp001'] != '' )& (df['iritemp001'] != df['defined_class']), df[['defined_class','iritemp001']].apply('-'.join, axis=1),"OK")
    print(broken)

    df['iritemp001'] = pd.np.where(df['defined_class'] != '', df['defined_class'], df['iritemp001'])

    df['defined_class'] = [generate_id(i) for i in df['iritemp001']]
    x = df[['defined_class','id']]
    x.columns = ['iritemp001','id']
    df_ids = pd.concat([df_ids,x],sort=True)
    df_ids = df_ids.drop_duplicates()
    df = df.drop(['pattern', 'id','iritemp001'], axis=1)
    df_ids['iri'] = df_ids['iritemp001']
    df_ids = df_ids.drop("iritemp001", axis=1)
    #print(df.head(4))
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
defclass = df['defined_class']
df.drop(labels=['defined_class'], axis=1,inplace = True)
df.insert(0, 'defined_class', defclass)
df = df.sort_values('defined_class')
df_ids = df_ids.sort_values('iri')
df.drop_duplicates().to_csv(tsv, sep = '\t', index=False)
idstest = df_ids['iri']
if len(idstest) != len(set(idstest)):
    print("ERROR DUPLICATE IRIS")
else:
    print("ID map consistent.")
df_ids.to_csv(id_map, sep = '\t', index=False)
with open(reserved_ids, 'w') as f:
    for item in ids:
        f.write("%s\n" % item)