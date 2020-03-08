#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

def generate_charts(ranges):
    # create pandas dataframe
    df = pd.DataFrame(ranges).transpose()

    # datetime from string date
    df['datetime'] = pd.to_datetime(df.index, format='%d/%b/%Y:%H:%M', utc=False)

    # calculate means values
    df['static_rt_mean'] = df['static_rt_sum'] / df['static_count']
    df['upstream_rt_mean'] = df['upstream_rt_sum'] / df['upstream_count']
    df['err_rt_mean'] = df['err_rt_sum'] / df['err_count']

    # prevent deprecation warning for implicit date convertion
    register_matplotlib_converters()

    # création du graphique du nombre de requêtes
    fig, ax = plt.subplots(figsize=(15,7))
    ax.set_title("Nombre de requêtes par minute")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Nombre requêtes")

    fig.autofmt_xdate()

    ax.stackplot(df['datetime'], df['upstream_count'], df['static_count'], df['err_count'], labels=('Apps','Statics','Erreurs'))

    plt.legend(loc=2)
    fig.savefig('/tmp/nb_requests.png')

    # création du graphique de la moyenne des temps de réponses
    fig, ax = plt.subplots(figsize=(15,5))
    ax.set_title("Temps de réponse moyen par minute")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Temps de réponse (en secondes)")

    fig.autofmt_xdate()

    ax.plot(df['datetime'], df['upstream_rt_mean'], label='Apps')
    ax.plot(df['datetime'], df['static_rt_mean'], label='Statics')
    ax.plot(df['datetime'], df['err_rt_mean'], label='Erreurs')

    plt.legend(loc=2)
    fig.savefig('/tmp/rt_requests.png')

def clean_zero(v):
    if v == 0:
        return np.nan
    return v

def generate_charts_by_prefix(ranges):
    # create pandas dataframe
    df = pd.DataFrame(ranges).transpose()

    # datetime from string date
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%b/%Y:%H:%M', utc=False)

    df['static_count'] = df['static_count'].apply(clean_zero)
    df['upstream_count'] = df['upstream_count'].apply(clean_zero)
    df['err_count'] = df['err_count'].apply(clean_zero)

    # calculate means values

    df['static_rt_mean'] = df['static_rt_sum'] / df['static_count']
    df['upstream_rt_mean'] = df['upstream_rt_sum'] / df['upstream_count']
    df['err_rt_mean'] = df['err_rt_sum'] / df['err_count']

    # prevent deprecation warning for implicit date convertion
    register_matplotlib_converters()

    df.pivot(index='datetime', columns='prefix', values=['static_rt_mean','upstream_rt_mean','err_rt_mean','static_count','upstream_count','err_count']).plot(figsize=(15,7)).get_figure().savefig('/tmp/output.png')

    # création du graphique du nombre de requêtes
    fig, ax = plt.subplots(figsize=(15,7))
    ax.set_title("Nombre de requêtes par minute")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Nombre requêtes")

    fig.autofmt_xdate()

    ax.stackplot(df['datetime'], df['upstream_count'], df['static_count'], df['err_count'], labels=('Apps','Statics','Erreurs'))

    plt.legend(loc=2)
    fig.savefig('/tmp/nb_requests_prefix.png')

    # création du graphique de la moyenne des temps de réponses
    fig, ax = plt.subplots(figsize=(15,5))
    ax.set_title("Temps de réponse moyen par minute")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Temps de réponse (en secondes)")

    fig.autofmt_xdate()

    ax.plot(df['datetime'], df['upstream_rt_mean'], label='Apps')
    ax.plot(df['datetime'], df['static_rt_mean'], label='Statics')
    ax.plot(df['datetime'], df['err_rt_mean'], label='Erreurs')

    plt.legend(loc=2)
    fig.savefig('/tmp/rt_requests_prefix.png')
