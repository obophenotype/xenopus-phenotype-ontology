import sys
import os

list_f = sys.argv[1]
blacklist_f = sys.argv[2]
out_f = sys.argv[3]

#list_f = "/ws/xenopus-phenotype-ontology/src/patterns/tmp/anatomy_seed.txt"
#blacklist_f = "/ws/xenopus-phenotype-ontology/src/patterns/tmp/blacklist.txt"
#out_f = "/ws/xenopus-phenotype-ontology/src/patterns/anatomy_seed.txt"

try:
    os.remove(out_f)
except OSError:
    pass

with open(list_f) as f:
    l = f.readlines()

l = [w.replace('\n', '') for w in l]


with open(blacklist_f) as f2:
    blacklist = f2.readlines()

blacklist = [i.strip() for i in blacklist if i in blacklist]
nlist = [i.strip() for i in l if i not in blacklist and i.startswith("http")]

with open(out_f, 'w') as f:
    for item in nlist:
        f.write("%s\n" % item)