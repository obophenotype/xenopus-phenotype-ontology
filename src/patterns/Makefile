XAO = xenopus_anatomy.owl
AUTOPATTERNS = ../patterns/data/auto/
AUTOPATTERNACCESSION = 99999
PURL=http://purl.obolibrary.org/obo/XPO_

$(XAO):
	curl -L -O https://raw.githubusercontent.com/xenopus-anatomy/xao/xpo/xpo_draft/xenopus_anatomy.owl

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
 
anatomy_seed.txt: $(XAO)
	robot query -f csv -i $< --query ../sparql/xao_terms.sparql $@

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