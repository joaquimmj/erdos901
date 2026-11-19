# Plan du jour

Plan complet : `erdos901_plan_complet.md` (19/11/2026). Cap : bornes supérieures de m(n) pour 7 ≤ n ≤ 20 par joints exacts (axe A), puis m(5, v) (axe B).

| Tâche | État |
|---|---|
| A1 table de référence `RECORDS.md` (Aglave et al., Grill–Linzmayer) | en cours |
| A2 `join.py` : base donnée par son seul nombre d'arêtes, donc utilisable pour tout n | à faire |
| A3 balayage n = 7, 8 (`batch` 44531901519) | en cours |
| B1 m(5, v), v = 10 à 18 (`mnv` 44524361427) + descentes rapides locales | en cours |
| B2 campagne compilée v = 14 à 22 (`anneal` 44547585180) | en file d'attente |
| E-mail à Linzmayer et Grill | brouillon dans `drafts/`, **non envoyé** |

Critère d'arrêt n = 5 : si la campagne compilée ne descend pas sous 200 colorations propres à 50 arêtes, arrêter.
