# Table de référence : bornes sur m(n)

Bornes supérieures publiées : Aglave, Amarnath, Shannigrahi, Singh, arXiv:1602.00218v4 (Australas. J. Combin. 76 (2020)), table 2, relue en entier le 19/11/2026. Bornes inférieures : Grill–Linzmayer, arXiv:2403.05674v3. Rien de publié pour n ≥ 18.
Colonne « ici » : **non relu, non annoncé**. Voir `REPORT.md` pour le détail et le niveau de certification.

| n | Borne sup. publiée | Construction publiée | Borne inf. | Ici |
|---|---|---|---|---|
| 3 | 7 (exact) | Fano | 7 | |
| 4 | 23 (exact) | Seymour / Toft | 23 (Östergård) | |
| 5 | 51 | Abbott–Hanson : 2⁴ + 5·m(3) | 32 (33 annoncé par Agarwal, non relu) | |
| 6 | 147 | Abbott–Moser : m(2)·m(3)² | 64 | |
| 7 | 421 | Abbott–Hanson : 2⁶ + 7·m(5) | 128 | |
| 8 | 1212 | Aglave et al., multi-cœur k = 5 | 263 | **1163** : produit pondéré, `constructions/wprod1163.txt`, CaDiCaL + DRAT + Glucose |
| 9 | 2401 | Abbott–Moser : m(3)⁴ | 538 | |
| 10 | 7803 | Abbott–Moser : m(2)·m(5)² | | |
| 11 | 25449 | Mathews et al. : 15·2⁸ + 9·m(9) | | **25425** : produit pondéré, vérifié par `verify/check_wprod.py` |
| 12 | 55223 | Abbott–Moser : m(3)⁴·m(4) | | |
| 13 | 200889 | Aglave et al., bloc modifié k = 4 | | **182064** : produit pondéré, vérifié par `verify/check_wprod.py` |
| 14 | 528218 | Aglave et al., multi-cœur k = 5 | | **436178** : produit pondéré, vérifié par `verify/check_wprod.py` |
| 15 | 857157 | Abbott–Moser : m(3)⁵·m(5) | | |
| 16 | 3308499 | Aglave et al., bloc modifié k = 5 | | |
| 17 | 10375782 | Aglave et al., multi-cœur k = 7 | | **10217413** : produit pondéré, vérifié par `verify/check_wprod.py` (10371690 déjà par leur récurrence multi-cœur avec k = 5) |

Source : `results/wprod/chain_h4_o8.txt` (au plus 4 composantes lourdes et 8 sommets isolés). Les bornes pour n = 13, 14, 17 utilisent m(8) ≤ 1163. Balayages plus larges en cours.
