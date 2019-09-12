xpo_table.csv:
	robot query --use-graphs true -f csv -i $(SRC) --query ../sparql/xpo_metadata_table.sparql $@

#$(PATTERNDIR)/dosdp-patterns: .FORCE
#	echo "external.txt goal skipped until further notice"