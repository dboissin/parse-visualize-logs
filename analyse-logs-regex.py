#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from dfchart.viz import generate_charts
from gzip import open as gzopen
import sys

pattern = re.compile(".*?\[([A-Za-z0-9\/:+\s]+)\]\s\"(.*?)\"\s([0-9]+)\s[0-9]+\s\".*?\"\s\".*?\"rt=([0-9]+\.[0-9]+)\s.*?urt=\"([0-9\.\-,\s]+)\"")

def parse_lines(f, ranges):
    line = f.readline()
    while line:
        m = pattern.match(line)
        if m:
            curr_range = m.group(1)[0:17]
            if not(curr_range in ranges):
                ranges[curr_range] = { 'upstream_count' : 0, 'upstream_rt_sum' : 0.0, 'static_count' : 0, 'static_rt_sum' : 0.0, 'err_count' : 0, 'err_rt_sum' : 0.0 }
            r = ranges[curr_range]
            if int(m.group(3)) > 399:
                prefix_type = 'err'
            else:
                if '-' == m.group(5):
                    prefix_type = 'static'
                else:
                    prefix_type = 'upstream'
            r[prefix_type + '_count'] += 1
            r[prefix_type + '_rt_sum'] += float(m.group(4))
        else:
            print("pattern doesn't match : %s" % line)
        line = f.readline()

def parse_file(path):
    ranges = {}
    if '.gz' in path:
         with gzopen(path, 'rt') as f:
             parse_lines(f, ranges)
    else:
        with open(path) as f:
            parse_lines(f, ranges)
    return ranges


# parse nginx log file
ranges = parse_file(sys.argv[1])

# create dataframe and generate charts
generate_charts(ranges)
