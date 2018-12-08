XAO = xenopus_anatomy.owl
AUTOPATTERNS = ../patterns/data/auto/
AUTOPATTERNACCESSION = 99999
PURL=http://purl.obolibrary.org/obo/XPO_
OBOPURL=http://purl.obolibrary.org/obo/

$(XAO):
	curl -L -O https://raw.githubusercontent.com/xenopus-anatomy/xao/xpo/xpo_draft/xenopus_anatomy.owl
	robot reason --reasoner ELK --input $@ --output $@

#https://raw.githubusercontent.com/obophenotype/upheno/master/src


MANUALPATTERNS=$(patsubst %.tsv, $(MANUALPATTERNDIR)/%.tsv, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))
AUTOPATTERNS=$(patsubst %.tsv, $(AUTOPATTERNDIR)/%.tsv, $(notdir $(wildcard ../patterns/data/auto/*.tsv)))
AUTOPATTERNDIR=../patterns/data/auto
MANUALPATTERNDIR=../patterns/data/manual
pattern_term_lists_auto := $(patsubst %.tsv, $(AUTOPATTERNDIR)/%.txt, $(notdir $(wildcard ../patterns/data/auto/*.tsv)))
pattern_term_lists_manual := $(patsubst %.tsv, $(MANUALPATTERNDIR)/%.txt, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))

../patterns/data/manual/%.txt: ../patterns/data/manual/%.tsv
	grep -Eo '($(PURL))[^[:space:]"]+' $< | sort | uniq > $@

../patterns/data/auto/%.txt: ../patterns/data/auto/%.tsv
	grep -Eo '($(PURL))[^[:space:]"]+' $< | sort | uniq > $@

reserved_iris.txt: $(pattern_term_lists_auto) $(pattern_term_lists_manual)
	robot query -f csv -i ../ontology/xpo-edit.owl --query ../sparql/xpo_terms.sparql editseed.txt
	cat $(pattern_term_lists_auto) $(pattern_term_lists_manual) editseed.txt | sort | uniq >$@
 
../patterns/tmp/subclasses.sparql: 
	sh ../scripts/generate_sparql_subclass_query.sh blacklist_branch.txt $@
 
../patterns/tmp/blacklist.txt: $(XAO) ../patterns/tmp/subclasses.sparql
	robot query --input $< --query ../patterns/tmp/subclasses.sparql ../patterns/tmp/blacklist_tmp.txt
	cat ../patterns/tmp/blacklist_tmp.txt ../patterns/blacklist.txt | grep -Eo '($(OBOPURL))[^[:space:]"]+' | sort | uniq >$@

anatomy_seed.txt: $(XAO) ../patterns/tmp/blacklist.txt
	robot query -f csv -i $< --query ../sparql/xao_terms.sparql ../patterns/tmp/anatomy_seed.txt
	sort -o ../patterns/tmp/anatomy_seed.txt ../patterns/tmp/anatomy_seed.txt
	sort -o ../patterns/tmp/blacklist.txt ../patterns/tmp/blacklist.txt
	#comm -23 ../patterns/tmp/anatomy_seed.txt ../patterns/tmp/blacklist.txt > $@
	#awk 'NR==FNR{a[$0];next} !($0 in a)' ../patterns/tmp/blacklist.txt ../patterns/tmp/anatomy_seed.txt
	python3 ../scripts/blacklist.py ../patterns/tmp/anatomy_seed.txt ../patterns/tmp/blacklist.txt anatomy_seed.txt 


$(AUTOPATTERNDIR)/abnormal.tsv: anatomy_seed.txt
	cp $< $@
	sed -i '' "1s/.*/entity/" $@
	python3 ../scripts/assign_unique_ids.py $@ id_map.tsv reserved_iris.txt $(AUTOPATTERNACCESSION) $(PURL)

$(AUTOPATTERNDIR)/abnormalMorphology.tsv: anatomy_seed.txt
	cp $< $@
	sed -i '' "1s/.*/entity/" $@
	python3 ../scripts/assign_unique_ids.py $@ id_map.tsv reserved_iris.txt $(AUTOPATTERNACCESSION) $(PURL)

$(MANUALPATTERNDIR)/%.tsv:
	python3 ../scripts/assign_unique_ids.py $@ id_map.tsv reserved_iris.txt $(AUTOPATTERNACCESSION) $(PURL)

auto_patterns: $(AUTOPATTERNDIR)/abnormal.tsv $(AUTOPATTERNDIR)/abnormalMorphology.tsv 

pattern_iris: $(MANUALPATTERNS)
	
xpo.csv:
	robot query -f csv -i ../patterns/definitions.owl --query ../sparql/xpol_terms.sparql $@