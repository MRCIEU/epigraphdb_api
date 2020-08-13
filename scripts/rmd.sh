#!/bin/bash

Rscript -e "rmarkdown::render(\"$1\", output_dir='output')"
