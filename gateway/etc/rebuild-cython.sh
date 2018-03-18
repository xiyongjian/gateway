#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    find -E gateway tests -regex '.*\.(c|so)' -exec rm {} +
else
    find gateway tests -regex '.*\.\(c\|so\)' -exec rm {} +
fi
python setup.py build_ext --inplace
