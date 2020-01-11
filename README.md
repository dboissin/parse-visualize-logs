Analyse logs nginx
==================

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
```

Temps d'executions
-----------------

| Version | Real | User | Sys |
|---------|------|------|-----|
| python seul | 1m15.348s | 1m12.640s | 0m3.372s |
| python regex | 2m30.206s | 2m26.880s | 0m3.552s |

Résultat
--------

Le script produit deux images dans `/tmp` représentant le nombre de requêtes et le temps de réponse.

![Nombre de requêtes](out/nb_requests.png)
![Temps de réponse moyen](out/rt_requests.png)
