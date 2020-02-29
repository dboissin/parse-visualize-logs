#!/usr/bin/python
# -*- coding: utf-8 -*-

from rust.parse_logs.target.release import libparse
from dfchart.viz import generate_charts
import sys

# parse nginx log file
ranges = libparse.parse(sys.argv[1])

# create dataframe and generate charts
generate_charts(ranges)
