#!/usr/bin/python
# -*- coding: utf-8 -*-

from go import parse
from dfchart.viz import generate_charts
from dfchart.viz import generate_charts_by_prefix
import pandas as pd
import sys

# parse nginx log file
ranges = parse.parse(sys.argv[1])

# create dataframe and generate charts
#generate_charts(ranges)
generate_charts_by_prefix(ranges)
