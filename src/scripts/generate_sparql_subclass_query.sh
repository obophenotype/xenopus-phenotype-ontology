#!/bin/sh
BLACKLIST=$1
SPARQL=$2

V=$(sed -e :a -e '$!N; s/\n/> </; ta' $BLACKLIST) 

echo "prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sub WHERE {
    VALUES ?o { <$V> } 
    ?sub rdfs:subClassOf* ?o .
} " > "$SPARQL"