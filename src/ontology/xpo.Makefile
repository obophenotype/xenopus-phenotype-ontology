OTHER_SRC = $(PATTERNDIR)/definitions.owl $(PATTERNDIR)/xpo-xrefs.owl

xpo_table.csv:
	robot query --use-graphs true -f csv -i $(SRC) --query ../sparql/xpo_metadata_table.sparql $@