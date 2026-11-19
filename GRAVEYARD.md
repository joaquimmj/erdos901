# Pistes mortes

À lire avant de lancer un calcul. Une ligne par piste : ce qui a été essayé, le résultat, la preuve.
« Infaisable » veut dire : prouvé par l'ILP (HiGHS seul, sans certificat indépendant).

| Piste | Résultat | Preuve |
|---|---|---|
| n = 5, ≤ 50 arêtes, groupe complet du 51 et ses 24 sous-groupes | infaisable | `REPORT.md` |
| n = 5, ≤ 50, 220 groupes à blocs, v = 11 à 14 | infaisable | `REPORT.md` |
| n = 5, ≤ 50, 47 groupes classiques sur 48 (Frobenius, PSL), v = 11 à 21 | infaisable | `results/classical_n5/` |
| n = 5, ≤ 50, symétrie de Fano + 8 à 11 sommets libres | infaisable ; minimum exactement 51 avec 10 sommets libres | `results/classical_n5/` |
| n = 5, joints base Fano (paires), \|W\| ≤ 11 | optimum 51 à \|W\| = 10 ; infaisable ≤ 50 à \|W\| = 11 | `results/join/` |
| n = 5, joints base triangle (triples), \|W\| = 9 à 11 | infaisable ≤ 50 | `results/join/` |
| n = 5, joints mixtes paires + triples, \|W\| = 9, 10 | infaisable ≤ 50 | `REPORT.md` |
| n = 5, recherche locale à 50 arêtes, 88 recherches de 5 h 30, v = 13 à 20 | aucun 50 ; à v = 17 on retombe sur « le 51 moins une arête » (325 colorations propres) | branche `results`, `anneal_44473660998/` |
| n = 5, recherche locale compilée à 50 arêtes, v = 17 et 21, 2 h | 2 172 et 27 837 colorations propres | `results/night_local/fast/` |
| n = 6, recherche locale à 146 arêtes depuis le produit à 147 | aucun progrès depuis 1 600 colorations propres en 1 h | `results/night_local/fast/` |
| n = 6, joints, toutes les formes testées | infaisable ≤ 146 | `results/join/` |
| n = 7, joints base Fano (r = 4), \|W\| = 10 à 13 | infaisable ≤ 420 | `results/join/` |
| Solveur exact générique (OR-Tools CP-SAT) pour m(n, v) | borne 1 pour m(4, 8) après 300 s ; supprimé | historique git |
| `search/lns.py` pour n = 5 | timeouts | `REPORT.md` |
| Maître ILP de CEGAR à faible symétrie | 4 itérations en 25 min ; ne passe pas à l'échelle | `REPORT.md` |
| Joints à un seul cœur (lot `batch` 44531901519) : n = 5 (\|W\| = 12), n = 6, n = 7 (\|W\| ≤ 13 en paires, r = 4, 5), n = 8 (r = 2 à 6) | tous infaisables sous le record, sauf 5 cas sans réponse dans le temps imparti (n5 w13, n6 r3 w13, n7 r2 w14/15, n8 r2 w14/15) | branche `results`, `batch_44531901519/SUMMARY.md` |
| Fano + 11 sommets libres, n = 5, ≤ 50 (CEGAR) | infaisable ; + 12 et + 13 : pas de réponse en 5 h 15 | idem |
