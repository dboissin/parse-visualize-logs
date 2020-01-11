#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


pattern = re.compile(".*?\[([A-Za-z0-9\/:+\s]+)\]\s\"(.*?)\"\s([0-9]+)\s[0-9]+\s\".*?\"\s\".*?\"rt=([0-9]+\.[0-9]+)\s.*?urt=\"([0-9\.\-,\s]+)\"")

# parse nginx log file
ranges = {}
with open('logs/access.log') as f:
    line = f.readline()
    while line:
        m = pattern.match(line)
        if m:
            curr_range = m.group(1)[0:16]
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

# create pandas dataframe
df = pd.DataFrame(ranges).transpose()

# calculate means values
df['static_rt_mean'] = df['static_rt_sum'] / df['static_count']
df['upstream_rt_mean'] = df['upstream_rt_sum'] / df['upstream_count']
df['err_rt_mean'] = df['err_rt_sum'] / df['err_count']


df2 = df.reset_index()

# création du graphique du nombre de requêtes
fig, ax = plt.subplots(figsize=(15,7))
ax.set_title("Nombre de requêtes groupées par plages de 10 minutes")
ax.set_xlabel("Heure")
ax.set_ylabel("Nombre requêtes")
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

ax.stackplot(df2['index'], df2['upstream_count'], df2['static_count'], df2['err_count'], labels=('Apps','Statics','Erreurs'))

plt.legend(loc=2)
fig.savefig('/tmp/nb_requests.png')

# création du graphique de la moyenne des temps de réponses
fig, ax = plt.subplots(figsize=(15,5))
ax.set_title("Temps de réponse moyen par plages de 10 minutes")
ax.set_xlabel("Heure")
ax.set_ylabel("Temps de réponse (en secondes)")
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

ax.plot(df2['index'], df2['upstream_rt_mean'], label='Apps')
ax.plot(df2['index'], df2['static_rt_mean'], label='Statics')
ax.plot(df2['index'], df2['err_rt_mean'], label='Erreurs')

plt.legend(loc=2)
fig.savefig('/tmp/rt_requests.png')
