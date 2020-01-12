Analyse logs nginx
==================

Ce dépôt a pour but de tester différentes solution pour parser des fichiers de logs volumineux (plusieurs Go). Ceci afin de charger un DataFrame Pandas pour faire quelques analyses et visualisations.

Avec des fichiers de taille plus réduite, on aurait pu directement charger le fichier dans pandas avec la fonction read_csv comme le montre l'extrait ci-dessous. Mais, pour des fichiers de plusieurs Giga ça nécessite trop de mémoire.

```python
import pandas as pd

df = pd.read_csv('logs/access.log',
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        usecols=[0, 3, 4, 5, 6, 7, 8, 9],
        names=['ip', 'date', 'request', 'status', 'size', 'referer', 'user_agent', 'rt'],
        na_values='-',
        header=None)
```

Nous cherchons à visualiser le nombre de requêtes (applicatives, fichiers statiques et en erreurs) et le temps de réponse moyen. Nous allons faire une aggrégation des requêtes par tranches de dix minutes et les stocker dans un dictionnaire python qui pourra être chargé dans un DataFrame Pandas.

Installation
------------

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install pip --upgrade
pip install pandas matplotlib
```

Execution
---------

```bash
time python analyse-logs-fullpy.py
time python analyse-logs-regex.py
cd c
make
cd ..
time python analyse-logs-c.py
```

Temps d'executions
-----------------

| Version | Real | User | Sys |
|---------|------|------|-----|
| python seul | 0m59.501s | 0m56.596s | 0m2.996s |
| python regex | 2m3.489s | 2m0.864s | 0m3.208s |
| python + extension C pour le parsing des logs | 0m11.470s | 0m7.168s | 0m3.292s |

Résultat
--------

Le script produit deux images dans `/tmp` représentant le nombre de requêtes et le temps de réponse.

![Nombre de requêtes](out/nb_requests.png)
![Temps de réponse moyen](out/rt_requests.png)
