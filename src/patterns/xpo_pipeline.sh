#!/bin/sh
# Wrapper script to execute the XPO pipeline
# TODO make sure that all patterns in external.txt are properly downloaded by now.
sh run.sh make -B reserved_iris.txt
sh run.sh make -B auto_patterns
sh run.sh make -B pattern_iris
