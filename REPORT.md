# Rapport de calibrage — groupes arbitraires, n = 4

*18 novembre 2026.*

## En bref

- La recherche CEGAR accepte maintenant n'importe quel groupe de permutations (`--group-file`) et sait reprendre un
  lancement (`--state`).
- Le témoin à 23 arêtes de m(4) (fichier OEIS A392185) est vérifié : pas de 2-coloration, **144 automorphismes**,
  orbites de sommets {0,1,2,3}, {4,5,6}, {7,8,9,10}.
- **Deux groupes définis a priori retrouvent 23 en moins d'une seconde**, sans connaître le témoin. Les deux
  contiennent un S₄ qui agit en même temps sur deux blocs de 4 sommets.
- Aucun produit direct S_{b₁} × … × S_{b_k} (sans action diagonale) ne descend sous 27.

## Ce qui a été ajouté

| Fichier | Rôle |
|---|---|
| `search/orbits.py` | lecture des groupes JSON, orbites des n-sous-ensembles (union-find, cache dans `.cache/`), automorphismes d'un hypergraphe, groupes à blocs |
| `search/cegar.py` | options `--group-file` et `--state` ; le cas cyclique passe par le même code |
| `search/calibrate.py` | lance CEGAR sur tous les groupes à blocs pour n et v donnés |
| `groups/*.json` | PSL(2,7) (Fano), groupe d'ordre 144 du témoin, et les deux groupes a priori qui trouvent 23 |
| `constructions/seymour_toft.txt` | le témoin à 23 arêtes |
| `verify/check_pysat.py` | troisième vérificateur : contrôles de forme, puis Glucose avec un autre encodage |

## Tests (dans `make test`)

| Test | Résultat |
|---|---|
| Témoin à 23 arêtes non 2-coloriable | oui |
| Automorphismes du témoin | 144, orbites 4 + 3 + 4 |
| CEGAR, n = 3, v = 7, PSL(2,7) | optimum 7 |
| CEGAR, n = 4, v = 11, groupe d'ordre 144 du témoin | optimum 23 |
| CEGAR, n = 4, v = 11, `blocks_3_4d4` (a priori) | optimum 23 |
| CEGAR, n = 4, v = 11, cyclique (non-régression, lancé à la main, hors `make test`) | 33, comme avant |

## Calibrage : n = 4, v = 11

Groupes testés : toutes les partitions de 11 en au plus 4 blocs, avec S_b sur chaque bloc, plus les variantes
« diagonales » où un seul S_b agit en même temps sur plusieurs blocs de taille b. Dans les noms, `4d4` veut dire
« un seul S₄ pour ces deux blocs de 4 ». Cela fait 39 groupes. Tous les lancements finissent avec le statut
« optimal » : le nombre donné est le minimum exact parmi les hypergraphes invariants sous le groupe.

| groupe | ordre | minimum invariant | itérations | secondes |
|---|---|---|---|---|
| `blocks_1_2_4d4` | 48 | 23 | 1 | 0.1 |
| `blocks_3_4d4` | 144 | 23 | 1 | 0.0 |
| `blocks_2_3d3_3` | 72 | 25 | 2 | 0.1 |
| `blocks_2_3d3d3` | 12 | 25 | 3 | 0.5 |
| `blocks_2_3_3_3` | 432 | 27 | 1 | 0.1 |
| `blocks_1_3d3_4` | 144 | 29 | 1 | 0.1 |
| `blocks_2_2_3_4` | 576 | 29 | 1 | 0.2 |
| `blocks_2d2_3_4` | 288 | 29 | 1 | 0.1 |
| `blocks_1_3_3_4` | 864 | 33 | 3 | 0.3 |
| `blocks_1_1_2_7` | 10080 | 35 | 1 | 0.1 |
| `blocks_1_1_3_6` | 4320 | 35 | 1 | 0.1 |
| `blocks_1_1_4_5` | 2880 | 35 | 1 | 0.1 |
| `blocks_1_2_2_6` | 2880 | 35 | 1 | 0.1 |
| `blocks_1_2_3_5` | 1440 | 35 | 1 | 0.2 |
| `blocks_1_2_4_4` | 1152 | 35 | 4 | 0.3 |
| `blocks_1_2d2_6` | 1440 | 35 | 1 | 0.1 |
| `blocks_1_3_7` | 30240 | 35 | 1 | 0.1 |
| `blocks_1_4_6` | 17280 | 35 | 1 | 0.1 |
| `blocks_1_5d5` | 120 | 35 | 1 | 0.0 |
| `blocks_2_2_2_5` | 960 | 35 | 1 | 0.2 |
| `blocks_2_2_7` | 20160 | 35 | 1 | 0.1 |
| `blocks_2_4_5` | 5760 | 35 | 1 | 0.1 |
| `blocks_2d2_2_5` | 480 | 35 | 1 | 0.2 |
| `blocks_2d2_7` | 10080 | 35 | 1 | 0.1 |
| `blocks_2d2d2_5` | 240 | 35 | 1 | 0.1 |
| `blocks_3_3_5` | 4320 | 35 | 1 | 0.1 |
| `blocks_3_4_4` | 3456 | 35 | 3 | 0.2 |
| `blocks_3d3_5` | 720 | 35 | 1 | 0.1 |
| `blocks_4_7` | 120960 | 35 | 1 | 0.1 |
| `blocks_1_5_5` | 14400 | 55 | 2 | 0.1 |
| `blocks_2_3_6` | 8640 | 55 | 2 | 0.1 |
| `blocks_1_1_1_8` | 40320 | 70 | 2 | 0.1 |
| `blocks_1_2_8` | 80640 | 70 | 2 | 0.1 |
| `blocks_3_8` | 241920 | 70 | 1 | 0.1 |
| `blocks_5_6` | 86400 | 75 | 2 | 0.1 |
| `blocks_1_1_9` | 362880 | 126 | 2 | 0.1 |
| `blocks_2_9` | 725760 | 126 | 1 | 0.1 |
| `blocks_1_10` | 3628800 | 210 | 2 | 0.1 |
| `blocks_11` | 39916800 | 330 | 1 | 0.1 |

**Les deux groupes qui trouvent 23 :**
- `blocks_3_4d4` : S₃ sur un bloc de 3, S₄ en diagonale sur deux blocs de 4 (ordre 144). C'est, à renumérotation
  près, le groupe du témoin.
- `blocks_1_2_4d4` : un sommet fixe, S₂ sur un bloc de 2, S₄ en diagonale sur deux blocs de 4 (ordre 48). C'est un
  sous-groupe du précédent.

Les deux hypergraphes trouvés ont 144 automorphismes et des orbites de tailles 3, 4 et 4. D'après Östergård, le
témoin est le seul à au plus 11 sommets : ce sont donc des copies renumérotées du témoin (l'isomorphisme explicite
n'a pas été calculé).

## Certification

Les trois hypergraphes à 23 arêtes produits (groupe du témoin, `blocks_3_4d4`, `blocks_1_2_4d4`) passent les trois
contrôles : force brute en C, CaDiCaL avec preuve DRAT vérifiée par drat-trim, et Glucose avec un autre encodage.
Les certificats sont dans `results/calibrage_n4/`.

## Lecture pour n = 5

1. **L'action diagonale est l'ingrédient qui compte.** Sans elle, le meilleur produit direct donne 27
   (`blocks_2_3_3_3`). Avec elle, on a 23 et 25.
2. Le critère de réussite du plan est atteint : une famille définie a priori retrouve 23, et en moins d'une
   seconde. La famille à transposer est « un S_b diagonal sur deux blocs de taille b, plus un petit bloc central ».
3. Pour n = 5, les candidats naturels sont donc les partitions de v avec deux (ou trois) blocs égaux en action
   diagonale, v de 11 à 25. `calibrate.py --n 5 --v …` les énumère déjà.
4. Les optima à 35 sont le 4-hypergraphe complet sur 7 sommets : le groupe est alors trop gros pour laisser
   autre chose.

## Limites

- Pour un groupe de plus de 500 éléments, les images des colorations sont prises sur 500 éléments proches de
  l'identité, pas sur tout le groupe. Le résultat reste exact, la convergence peut seulement être plus lente.
- Variantes non testées : échange de deux blocs égaux, A_b ou groupes cycliques par bloc, partitions en 5 blocs
  ou plus.
- Le workflow GitHub Actions `search.yml` ne prend pas encore de fichier de groupe.
- La mise à jour OEIS (piste 0) n'est pas faite.
