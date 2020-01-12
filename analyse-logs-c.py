#!/usr/bin/python
# -*- coding: utf-8 -*-

from c import parse
from dfchart.viz import generate_charts

# parse nginx log file
ranges = parse.parse('logs/access.log')

# create dataframe and generate charts
generate_charts(ranges)
