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

---

# Suite — attaque de m(5) ≤ 51 (état au 18 novembre 2026)

## En bref

- Le 51 d'Abbott–Hanson est reproduit et **il est arête-critique** : pas de gain par simple suppression.
- **Aucune construction sous 51 n'a été trouvée.**
- Les groupes à blocs qui marchent pour n = 4 ne donnent rien pour n = 5 sur 11 à 14 sommets, mais pour une
  raison presque arithmétique : leurs orbites d'arêtes sont trop grosses pour tenir sous 51.
- m(5, 10) = 126.

## Le 51

Construction (`hg.abbott_hanson`, fichier `constructions/aht51.txt`) : les 7 sommets de Fano, plus 5 paires
(aᵢ, bᵢ). Arêtes : chaque droite de Fano avec chaque paire (35 arêtes), et les 16 transversales des paires qui
prennent un nombre pair de aᵢ. La description est reconstruite à partir de la preuve, pas recopiée d'Aglave et al. ;
la non-2-colorabilité est vérifiée par calcul.

| Propriété | Valeur |
|---|---|
| Sommets, arêtes | 17, 51 |
| 2-coloriable | non |
| Arête-critique | oui (51 arêtes sur 51) |
| Automorphismes | 322 560 = 168 × 1 920 |
| Orbites de sommets | les 7 de Fano ; les 10 des paires |
| Orbites d'arêtes | 35 et 16 |

## Recherches n = 5, cible ≤ 50 arêtes

| Recherche | Résultat |
|---|---|
| v = 17, groupe complet du 51 | optimum 51 : rien de mieux avec toute cette symétrie |
| v = 17, 24 sous-groupes du groupe du 51 (ordres 35 à 322 560) | tous infaisables sous 51 |
| v = 11 à 14, groupes à blocs et variantes diagonales (220 groupes) | tous infaisables sous 51 |

Ces « infaisable » sont des preuves : le maître ILP est infaisable, donc aucun hypergraphe invariant sous le
groupe n'a 50 arêtes ou moins. Elles ne sont pas triviales pour tous les groupes. Tailles d'orbites des
5-sous-ensembles, sur un échantillon :

| groupe | orbites | taille médiane | orbites de taille ≤ 50 |
|---|---|---|---|
| groupe complet du 51 (v = 17) | 16 | 160 | 4 |
| Z₇ × Z₅ dans le groupe du 51 | 224 | 35 | 224 |
| groupe des paires seul, ordre 1 920 | 193 | 10 | 156 |
| `blocks_3_3_4d4` (v = 14) | 66 | 18 | 54 |
| `blocks_2_4d4d4` (v = 14) | 119 | 12 | 119 |

Pour les groupes à blocs, beaucoup de petites orbites étaient disponibles et le résultat reste négatif. **La
famille qui retrouve 23 pour n = 4 ne se transpose donc pas telle quelle à n = 5 sur 11 à 14 sommets.**

### Recherches à faible symétrie : non concluantes

Le conteneur de calcul a redémarré pendant ces lancements. Ce qui a pu être relevé :

| Recherche (v = 17, cible ≤ 50) | Budget | Résultat |
|---|---|---|
| Z₂ (un double échange de paires), 4 030 orbites | 25 min | 4 itérations, dernier coût du maître 40, non conclu |
| Z₂², 2 612 orbites | 25 min | 4 itérations, dernier coût du maître 45, non conclu |
| Z₂⁴, 1 718 orbites | 25 min | 4 itérations, aucune solution du maître à la fin |
| Z₇, Z₅, Z₃ (trois variantes), Z₃ × Z₃ | — | perdus au redémarrage, non relancés |
| LNS depuis le 51, voisinages de 2 sommets (26 ou 27 arêtes libérées), 170 s chacun | 3 voisinages | 3 timeouts |
| LNS, voisinages de 2 à 3 sommets, 400 s chacun | 1 h prévue | perdu au redémarrage |

Aucune de ces lignes ne prouve quoi que ce soit. Le blocage est le maître ILP : avec peu de symétrie il a des
milliers de variables et chaque résolution atteint sa limite de temps (4 itérations en 25 minutes, là où il en
faudrait des centaines). **Sous cette forme, CEGAR à faible symétrie et LNS ne sont pas praticables pour n = 5** ;
plus de minutes sur GitHub Actions ne suffiront pas sans changer le maître (par exemple une heuristique de
couverture à la place de la résolution exacte, qui ne servirait qu'à la fin).

## m(5, v) exact

- **m(5, 10) = 126.** Borne inférieure : chacune des 126 bipartitions 5 + 5 impose de prendre une de ses deux
  moitiés. Borne supérieure : hypergraphe à 126 arêtes trouvé par CEGAR sans symétrie, certifié par les trois
  contrôles (`results/m5_v10/`). Grill–Linzmayer ne donnent pas cette valeur, mais l'argument est élémentaire :
  ne pas la présenter comme nouvelle sans vérifier.
- m(5, 11) : pas de convergence en 4 minutes sans cassage de symétrie (dernier coût du maître 63, non optimal).
  La valeur est de toute façon connue d'après de Vries : la borne C₆/2 = 66 est atteinte exactement quand un
  système de Steiner existe, et S(4, 5, 11) existe. Donc m(5, 11) = 66 (déduction de ma part, non recalculée).

## Outils ajoutés

- `search/cegar.py` : `--fixed` (arêtes imposées) et `--touch` (nouvelles arêtes limitées à celles qui touchent
  des sommets donnés).
- `search/lns.py` : recherche locale à grand voisinage. On libère les arêtes qui touchent 2 à 4 sommets tirés au
  hasard, et CEGAR cherche un remplacement strictement plus petit.
- `search.yml` : entrées `group_files` (liste de fichiers de groupe) et `state_from` (reprise d'un lancement).
  **Non testé sur GitHub.**

## Non fait

- `search/exact_mnv.py` avec cassage de symétrie et preuve DRAT d'infaisabilité à k − 1 arêtes.
- AGL(1, p) et PSL(2, q) : non testés.
- Groupes à blocs pour v = 15 à 25 : non lancés.

## Littérature (recherche du 18 novembre 2026)

- Grill–Linzmayer, arXiv:2403.05674 v3, Théorème 1 : m(5) ≥ 32, m(6) ≥ 64, m(7) ≥ 128, m(8) ≥ 263, m(9) ≥ 538.
  Les chiffres du plan sont confirmés. Leur tableau donne toujours 51 et 147 comme meilleures bornes supérieures.
- Aucun article trouvé qui améliore m(5) ≤ 51 ou m(6) ≤ 147.
- **À vérifier :** une fiche ResearchGate récente s'intitule « A new lower bound for property B: m(5) ≥ 33 ».
  La page n'a pas pu être lue d'ici (auteurs, date et contenu inconnus). Si c'est confirmé, la mise à jour OEIS
  doit citer 33 et non 32.
  Seconde recherche (19 nov. 2026) : un dépôt GitHub `AyushAg1002/property-b-m5-lower33` annonce un certificat exact
  pour m(5) ≥ 33, non relu par des pairs, non vérifié ici. Toujours aucune source sous 51.
- La recherche s'est limitée à deux requêtes web : ce n'est pas une revue complète.

---

# Recherche locale directe (19 novembre 2026)

`search/anneal.py` abandonne le maître ILP. L'état est un ensemble de K arêtes ; le coût est le nombre exact de
2-colorations propres (toutes les 2^(v−1) colorations sont suivies). À chaque pas on prend une coloration propre au
hasard, on ajoute une arête qui la tue, et on retire l'arête la moins utile.

| Essai | Résultat |
|---|---|
| n = 3, v = 7, K = 7 | trouvé, immédiat |
| n = 4, v = 11, K = 23, départ aléatoire, sans symétrie | **trouvé en 2,5 s** (deux graines sur deux), certifié par les trois contrôles |
| n = 5, v = 17, K = 51, départ aléatoire, 2 graines × 280 s | 1 trouvé ; l'autre bloqué vers 2 100 colorations propres |
| n = 5, v = 17, K = 50, départ = le 51 moins une arête, 250 s | non trouvé ; 448 colorations propres au départ, 325 au mieux |

C'est la première méthode du repo qui retrouve 23 sans symétrie ni indice. Pour n = 5 elle retrouve aussi un
hypergraphe à 51 arêtes depuis un départ aléatoire (non comparé au 51 connu), mais rien à 50 en quelques minutes.

**Campagne longue lancée le 19 novembre** (workflow `anneal.yml`, déclenché par une branche `run/...`) : n = 5,
K = 50, v = 13 à 20, 20 machines × 4 graines, environ 5 h 30 chacune. Quatre machines partent du 51. Tout succès
est certifié et écrit sur la branche `results`.

## Campagne de nuit du 19 nov. 2026 (n = 5, 50 arêtes)

Run GitHub Actions `44473660998` : 88 recherches de 5 h 30 (v = 13 à 20), plus 12 recherches locales de 2 h.
**Aucun hypergraphe à 50 arêtes trouvé.** Détail : branche `results`, `anneal_44473660998/SUMMARY.md`
(copie dans `results/night_local/`).

| v | Départ | Meilleur nombre de 2-colorations propres restantes |
|---|---|---|
| 13 | aléatoire | 261 |
| 14 | aléatoire | 375 (281 en local) |
| 15 | aléatoire | 353 ; 369 atteint par 6 graines sur 8 |
| 16 | aléatoire | 673 |
| 17 | aléatoire | 325, atteint par 5 graines sur 8 |
| 17 | le 51 moins une arête | 325, jamais amélioré (8 graines) |
| 18, 19 | le 51 moins une arête | 650, 1300 (= 325 × 2, × 4 : sommets libres) |
| 18, 19, 20 | aléatoire | environ 4 000, 7 700, 14 400 |

Observation : à v = 17, la recherche partie du hasard retombe sur le 51 connu privé d'une arête.
Vérifié sur une graine locale (`state_n5_v17_K50_s200.txt`) : une seule arête complète l'état en un
hypergraphe non 2-coloriable à 51 arêtes, 15-régulier, avec 322 560 automorphismes et des orbites de
sommets 10 + 7, comme la construction d'Abbott–Hanson–Toft. L'isomorphisme n'est pas prouvé formellement
(mêmes invariants seulement).

Lecture (interprétation, pas un résultat) : le 51 est un attracteur très fort de cette recherche à v = 17,
et « 51 moins une arête » un minimum local dont elle ne sort pas. Cela ne dit rien sur l'existence d'un 50
d'une autre forme : la recherche n'est pas exhaustive. À v = 15, l'état à 412 colorations testé n'est
complétable par aucune arête unique ; les états à 369 de la campagne n'ont pas pu être examinés
(artefacts non téléchargeables d'ici).
