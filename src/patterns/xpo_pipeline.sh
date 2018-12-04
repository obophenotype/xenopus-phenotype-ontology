#!/bin/sh
# Wrapper script to execute the XPO pipeline

make -B reserved_iris.txt
make -B auto_patterns
make -B pattern_iris