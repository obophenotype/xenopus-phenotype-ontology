xpo_table.csv:
	robot query --use-graphs true -f csv -i $(SRC) --query ../sparql/xpo_metadata_table.sparql $@

#$(PATTERNDIR)/dosdp-patterns: .FORCE
#	echo "external.txt goal skipped until further notice"

UPHENO_REL=https://raw.githubusercontent.com/obophenotype/upheno/master/src/ontology/upheno_materialise_relations.owl
HASPART=http://purl.obolibrary.org/obo/BFO_0000051
xpo_xenbase.obo:
	$(ROBOT) merge -i xpo.owl -I $(UPHENO_REL) \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000001 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000002 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000003 \
		materialize --reasoner ELK --term http://purl.obolibrary.org/obo/UPHENO_9000004 \
		convert --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo