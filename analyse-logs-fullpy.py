#!/usr/bin/python
# -*- coding: utf-8 -*-

from dfchart.viz import generate_charts

# parse nginx log file
ranges = {}
with open('logs/access.log') as f:
    line = f.readline()
    while line:
        idx = line.index('[') + 1
        rtidx = line.index('"rt=') + 4
        statusidx = line.index('" ') + 2
        curr_range = line[idx:idx+16]
        if not(curr_range in ranges):
            ranges[curr_range] = { 'upstream_count' : 0, 'upstream_rt_sum' : 0.0, 'static_count' : 0, 'static_rt_sum' : 0.0, 'err_count' : 0, 'err_rt_sum' : 0.0 }
        r = ranges[curr_range]
        if int(line[statusidx:statusidx+3]) > 399:
            prefix_type = 'err'
        else:
            urtidx = line.index('urt="') + 5
            if '-' == line[urtidx:urtidx+1]:
                prefix_type = 'static'
            else:
                prefix_type = 'upstream'
        r[prefix_type + '_count'] += 1
        r[prefix_type + '_rt_sum'] += float(line[rtidx:rtidx+6])
        line = f.readline()

# create dataframe and generate charts
generate_charts(ranges)
