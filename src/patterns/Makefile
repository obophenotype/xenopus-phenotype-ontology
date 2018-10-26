XAO = xenopus_anatomy.owl
AUTOPATTERNS = ../patterns/data/auto/
AUTOPATTERNACCESSION = 99999

$(XAO):
	curl -L -O https://raw.githubusercontent.com/xenopus-anatomy/xao/xpo/xpo_draft/xenopus_anatomy.owl

#https://raw.githubusercontent.com/obophenotype/upheno/master/src

$(AUTOPATTERNS): 
	mkdir -p $@

reserved_iris.txt: 
	robot query -f csv -i ../ontology/xpo-edit.owl --query ../sparql/xpo_terms.sparql $@
 
anatomy_seed.txt: $(XAO)
	robot query -f csv -i $< --query ../sparql/xao_terms.sparql $@

$(AUTOPATTERNS)abnormal.tsv: anatomy_seed.txt $(AUTOPATTERNS) reserved_iris.txt
	cp $< $@
	sed -i '' "1s/.*/entity/" $@
	python3 ../scripts/assign_unique_ids.py $@ id_map.tsv reserved_iris.txt $(AUTOPATTERNACCESSION) http://purl.obolibrary.org/obo/XPO_

$(AUTOPATTERNS)abnormalMorphology.tsv: anatomy_seed.txt $(AUTOPATTERNS) reserved_iris.txt
	cp $< $@
	sed -i '' "1s/.*/entity/" $@
	python3 ../scripts/assign_unique_ids.py $@ id_map.tsv reserved_iris.txt $(AUTOPATTERNACCESSION) http://purl.obolibrary.org/obo/XPO_

update_patterns: $(AUTOPATTERNS)abnormal.tsv $(AUTOPATTERNS)abnormalMorphology.tsv
