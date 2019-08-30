AUTOPATTERNACCESSION = 99999
PURL=http://purl.obolibrary.org/obo/XPO_
OBOPURL=http://purl.obolibrary.org/obo/
ROBOT=robot -vv

###########
## Paths ##
###########

PATTERNDIR=../patterns/dosdp-patterns
TEMPLATEDIR=../patterns/templates
AUTOPATTERNDIR=../patterns/data/anatomy
MANUALPATTERNDIR=../patterns/data/manual
TODOPATTERNDIR=../patterns/data/todo

###########
## Files ##
###########

SRC=../ontology/xpo-edit.owl
ID_MAP=id_map.tsv

#############################################
### WHOLE PIPELINE (main job)      ##########
#############################################

.PHONY: .FORCE

xpo_pattern_pipeline: templates anatomy_pipeline missing_iris

#../patterns/tmp/subclasses.sparql:
#	sh ../scripts/generate_sparql_subclass_query.sh blacklist_branch.txt $@

#############################################
### Computing all reserved iris in XPO ######
#############################################
RESERVED_IRI=tmp/reserved_iris.txt
XPO_SRC_SEED=tmp/editseed.txt
pattern_term_lists_auto := $(patsubst %.tsv, $(AUTOPATTERNDIR)/%.txt, $(notdir $(wildcard ../patterns/data/anatomy/*.tsv)))
pattern_term_lists_manual := $(patsubst %.tsv, $(MANUALPATTERNDIR)/%.txt, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))

../patterns/data/manual/%.txt: ../patterns/data/manual/%.tsv
	grep -Eo '($(PURL))[^[:space:]"]+' $< | sort | uniq > $@

../patterns/data/anatomy/%.txt: ../patterns/data/anatomy/%.tsv
	grep -Eo '($(PURL))[^[:space:]"]+' $< | sort | uniq > $@

$(XPO_SRC_SEED): $(SRC)
	robot query -f csv -i $< --query ../sparql/xpo_terms.sparql $@

$(RESERVED_IRI): $(pattern_term_lists_auto) $(pattern_term_lists_manual) $(XPO_SRC_SEED)
	cat $^ | sort | uniq > $@

#####################################################
### Filling in missing IRIs in manual patterns ######
#####################################################

MANUALPATTERNIDS=$(patsubst %.tsv, $(MANUALPATTERNDIR)/%_ids, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))

$(MANUALPATTERNDIR)/%_ids: $(RESERVED_IRI) $(ID_MAP)
	python3 ../scripts/assign_unique_ids.py $(MANUALPATTERNDIR)/$*.tsv id_map.tsv $(RESERVED_IRI) $(AUTOPATTERNACCESSION) $(PURL) $(PATTERNDIR)

missing_iris: $(MANUALPATTERNIDS)

###################################
### Running anatomy pipeline ######
###################################

XAO_IRI = https://raw.githubusercontent.com/xenopus-anatomy/xao/master/xenopus_anatomy.owl
XAO = tmp/xenopus_anatomy.owl
PATTERN_CONFIG=pattern-config.yaml
PIPELINE_DATA_PATH=data/anatomy/
SPARQLDIR=../sparql

download_patterns: .FORCE
	cat $(PATTERNDIR)/external.txt | sed 's!.*/!!' | sed 's! !!g' |  xargs -I{} rm -f $(PATTERNDIR)/{}
	cat $(PATTERNDIR)/external.txt | sed 's! !!g' | xargs -I{} wget -q {} -P $(PATTERNDIR)/

$(XAO):
	$(ROBOT) reason --reasoner ELK -I $(XAO_IRI) --output $@

anatomy_pipeline: download_patterns $(XAO) $(ID_MAP) $(RESERVED_IRI) 
	echo "Using $(XAO_IRI), make sure this is correct!"
	python3 ../scripts/xpo_anatomy_pipeline.py  $(XAO) $(ID_MAP) $(RESERVED_IRI) dosdp-patterns $(SPARQLDIR) $(PIPELINE_DATA_PATH) $(PATTERN_CONFIG)
	
#########################################
### Generating all ROBOT templates ######
#########################################

TEMPLATES=$(patsubst %.tsv, templates/%.owl, $(notdir $(wildcard $(TEMPLATEDIR)/*.tsv)))

templates/%.owl: templates/%.tsv
	robot -vvv merge --catalog ../ontology/catalog-v001.xml --input $(SRC) template   --prefix 'rdfs: http://www.w3.org/2000/01/rdf-schema#'  --prefix "IAO: http://purl.obolibrary.org/obo/IAO_" --template $< --output $@ && \
	robot annotate --input $@ --ontology-iri $(OBOPURL)xpo/patterns/$@ -o $@

templates: $(TEMPLATES)
	echo $(TEMPLATES)