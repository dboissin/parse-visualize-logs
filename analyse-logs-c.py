#!/usr/bin/python
# -*- coding: utf-8 -*-

from c import parse
from dfchart.viz import generate_charts
import sys

# parse nginx log file
ranges = parse.parse(sys.argv[1])

# create dataframe and generate charts
generate_charts(ranges)
