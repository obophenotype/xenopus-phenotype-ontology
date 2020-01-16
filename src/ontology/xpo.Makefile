xpo_table.csv:
	robot query --use-graphs true -f csv -i $(SRC) --query ../sparql/xpo_metadata_table.sparql $@

#$(PATTERNDIR)/dosdp-patterns: .FORCE
#	echo "external.txt goal skipped until further notice"

UPHENO_REL=https://raw.githubusercontent.com/obophenotype/upheno/master/src/ontology/upheno_materialise_relations.owl
HASPART=http://purl.obolibrary.org/obo/BFO_0000051
SIMPLESEEDPLUS=simple_seed_xenbase.txt

$(SIMPLESEEDPLUS): #$(SIMPLESEED)
	cp $(SIMPLESEED) $@
	echo "http://purl.obolibrary.org/obo/UPHENO_9000001" >> $@
	echo "http://purl.obolibrary.org/obo/UPHENO_9000001" >> $@
	echo "http://purl.obolibrary.org/obo/UPHENO_9000001" >> $@
	echo "http://purl.obolibrary.org/obo/UPHENO_9000001" >> $@

xpo-xenbase.owl: $(SIMPLESEEDPLUS) #$(SRC) $(OTHER_SRC) 
	$(ROBOT) merge --input $(SRC) -I $(UPHENO_REL)  \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000001 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000002 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000003 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000004 \
		reason --reasoner ELK --equivalent-classes-allowed none --exclude-tautologies structural \
		relax \
		remove --axioms equivalent \
		relax \
		filter --term-file $(SIMPLESEEDPLUS) --select "annotations ontology anonymous self" --trim true --signature true \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@

xpo-xenbase.obo: xpo-xenbase.owl
	$(ROBOT) merge -i xpo-xenbase.owl \
		convert --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo