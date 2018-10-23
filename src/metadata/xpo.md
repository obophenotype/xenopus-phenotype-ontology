---
layout: ontology_detail
id: xpo
title: Xenopus Phenotype Ontology
jobs:
  - id: https://travis-ci.org/obophenotype/xenopus-phenotype-ontology
    type: travis-ci
build:
  checkout: git clone https://github.com/obophenotype/xenopus-phenotype-ontology.git
  system: git
  path: "."
contact:
  email: cjmungall@lbl.gov
  label: Chris Mungall
description: Xenopus Phenotype Ontology is an ontology...
domain: stuff
homepage: https://github.com/obophenotype/xenopus-phenotype-ontology
products:
  - id: xpo.owl
  - id: xpo.obo
dependencies:
 - id: iao
 - id: go
 - id: ro
 - id: pato
 - id: bfo
 - id: chebi
 - id: cl
 - id: xao
tracker: https://github.com/obophenotype/xenopus-phenotype-ontology/issues
license:
  url: http://creativecommons.org/licenses/by/3.0/
  label: CC-BY
---

Enter a detailed description of your ontology here
