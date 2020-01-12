#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_charts(ranges):
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
