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
cd c
make
cd ..
time python analyse-logs-c.py
```

Temps d'executions
-----------------

| Version | Real | User | Sys |
|---------|------|------|-----|
| python seul | 1m15.348s | 1m12.640s | 0m3.372s |
| python regex | 2m30.206s | 2m26.880s | 0m3.552s |
| python + extension C pour le parsing des logs | 0m12.630s | 0m7.448s | 0m3.100s |

Résultat
--------

Le script produit deux images dans `/tmp` représentant le nombre de requêtes et le temps de réponse.

![Nombre de requêtes](out/nb_requests.png)
![Temps de réponse moyen](out/rt_requests.png)
