# PROMPT CLAUDE CODE — Erdős #901 (Property B) : battre les bornes supérieures de m(6), m(7), m(5)

> À coller tel quel dans Claude Code, lancé dans un dossier vide `~/erdos901/` sur mon Mac.
> Langue de travail : français pour les rapports, anglais pour le code, les commentaires et la note mathématique finale.

---

## 0. Qui je suis, ce que je veux, règles non négociables

Je suis Joaquim, étudiant à Paris. J'ai un Mac, pas de GPU, et beaucoup de temps d'IA. Je veux une **avancée réelle et vérifiable** sur le problème d'Erdős #901 : **la première amélioration d'une borne supérieure de m(n) pour un petit n**. Cette amélioration doit venir avec un certificat que n'importe qui peut revérifier.

Règles strictes :

1. **Rien n'est « trouvé » sans certificat vérifié par deux vérificateurs indépendants** (voir §6). Pas d'heuristique, pas de « très probablement non 2-colorable ».
2. **Vérification de nouveauté obligatoire avant tout** (Phase 0). Si quelqu'un a déjà amélioré la borne visée, tu t'arrêtes et tu me le dis avec les sources.
3. **Tu ne publies jamais rien toi-même.** Pas de post sur erdosproblems.com, pas d'issue GitHub publique, pas de soumission OEIS, pas d'arXiv, pas d'e-mail. Tu prépares des **brouillons** dans `drafts/` et tu attends que je les valide.
4. **Git : commits sous mon nom uniquement.** Aucune ligne `Co-Authored-By: Claude`, aucune mention de Claude dans les messages de commit. Dépôt local d'abord ; je décide du push.
5. **Matériel public : ne nomme jamais mon université.** Écris seulement « Paris » pour l'affiliation. Mon e-mail n'apparaît nulle part.
6. **Honnêteté sur les échecs.** Un résultat négatif propre est utile et publiable, par exemple « aucune construction Z_v-invariante sur ≤ v sommets avec ≤ E arêtes ». Ne le maquille jamais en succès.
7. **Économie de ressources.**
   - Lance les jobs longs avec `caffeinate -i` et `nice`, et en arrière-plan avec checkpoint sur disque.
   - Laisse 1 à 2 cœurs libres.
   - Ne remplis jamais le disque (limite tes logs).

---

## 1. Le problème

Un hypergraphe n-uniforme H = (V, E) a la **propriété B** (on dit qu'il est 2-colorable) s'il existe une coloration rouge/bleu de V telle qu'aucune arête ne soit monochromatique.

**m(n)** est le nombre minimal d'arêtes d'un hypergraphe n-uniforme **sans** propriété B, c'est-à-dire non 2-colorable (3-chromatique).

Valeurs connues :

- m(1) = 1, m(2) = 3 (le triangle), m(3) = 7 (le plan de Fano).
- m(4) = 23 : la borne supérieure vient de Seymour (1974) et Toft (1975), avec une construction sur 11 sommets. L'égalité a été prouvée par Östergård (2014), par recherche exhaustive.

Bornes pour les petits n (**à revérifier en Phase 0**) :

| n | borne inf. | borne sup. | origine probable de la borne sup. |
|---|-----------|-----------|-----------------------------------|
| 5 | 33 (2026, non relu) | **51** | Abbott–Hanson : m(5) ≤ 2⁴ + 5·m(3) = 16 + 35 |
| 6 | ? | **147** | produit d'Abbott–Moser : m(ab) ≤ m(a)·m(b)^a avec a=2, b=3 → 3·7² |
| 7 | ? | **421** | à déterminer en Phase 0 |
| 8 | ? | 1212 (?) | Aglave–Amarnath–Shannigrahi–Singh, ou Mathews–Panda–Shannigrahi (1269 avant) |
| 9 | ? | 2401 (?) | produit : m(3)·m(3)³ = 7⁴ |

Asymptotiquement, on sait que 2ⁿ·√(n/log n) ≪ m(n) ≪ n²·2ⁿ (Radhakrishnan–Srinivasan pour la borne inférieure, Erdős 1964 pour la borne supérieure).

**Pourquoi m(6) est la cible n°1.** Si la Phase 0 confirme que 147 vient du simple produit d'Abbott–Moser, cette borne n'a jamais été optimisée par ordinateur. Une construction générique de ce type est presque toujours battable par une recherche ciblée : c'est arrivé pour m(4), m(8), m(13), m(14), etc.

**Pourquoi m(5) ≤ 50 est le pari ambitieux.** Personne n'a battu 51 en environ 55 ans. Un article le désigne comme « le premier problème ouvert intéressant », et 51 est peut-être la vraie valeur.

**Pourquoi la borne inférieure de m(5) est INTERDITE.** Au moins deux équipes viennent d'arriver à m(5) ≥ 33 : Sumit Kumar Jha en septembre 2026, et le dépôt GitHub `AyushAg1002/property-b-m5-lower33`. Un troisième résultat identique ne vaut rien. Tu peux les lire pour t'inspirer des méthodes, mais tu ne travailles pas dessus.

---

## 2. Phase 0 — Vérification de nouveauté EN DIRECT (obligatoire, avant tout code de recherche)

Produis `reports/phase0.md`. Pour chaque source, note l'URL, la date de consultation et ce que tu y as trouvé.

1. **erdosproblems.com/901** : la page du problème **et** le fil de discussion / forum associé, en entier.
   - Note le statut, les bornes citées et tous les commentaires de 2025-2026.
   - Repère toute mention d'amélioration de m(5), m(6), m(7), etc.
   - Si le site bloque ton outil de fetch, essaie le navigateur. En dernier recours, dis-moi de coller la page.
2. **Le dépôt `teorth/erdosproblems`** (clone frais) : l'entrée YAML de #901, son statut et ses notes.
3. **Le wiki teorth** des contributions IA aux problèmes d'Erdős : cherche 901 et « Property B ».
4. **google-deepmind/formal-conjectures** : l'issue #2363 et tout fichier Lean sur m(n). Vérifie s'il y a des `sorry` ou des bornes formalisées.
5. **arXiv** (recherche de texte intégral, 2023 → aujourd'hui) avec ces requêtes : « property B », « non-2-colorable uniform hypergraph », « 3-chromatic hypergraph few edges », « m(5) ≤ », « m(6) ≤ 147 ».
   - Lis les articles 2403.05674, 1602.00218 et tout article de 2025-2026 qui cite Aglave et al.
   - Lis l'article de Jha (septembre 2026) : regarde quelles bornes supérieures il cite comme état de l'art.
6. **OEIS A392185** et toute séquence liée : regarde si les commentaires mentionnent m(6) ou m(7).
7. **GitHub** : recherche de dépôts et de code sur « property B hypergraph », « m(5) hypergraph », « non-2-colorable », « 147 hypergraph », « Abbott Hanson ».
   - **Exclus** les comptes de génération en masse : vibemathing, jaredwilder, AItoBit, Ghuffy1, peilinliu66-dev, Paulee314, et méfie-toi de KitaKen1 et veljjanoski.
   - Lis le README de AyushAg1002 pour l'état de l'art qu'il cite.
8. **AlphaEvolve** (arXiv 2511.02864, Georgiev, Gómez-Serrano, Tao, Wagner) : parcours la liste des 67 problèmes et l'annexe. Est-ce que Property B ou la 2-colorabilité d'hypergraphes en fait partie ? Fais pareil pour FunSearch et les travaux OpenEvolve/ShinkaEvolve de 2025-2026.
9. **Reconstitue le tableau exact des bornes supérieures pour n = 5..10** avec la construction de chacune. Retrouve en particulier d'où vient m(7) ≤ 421, à partir de la table d'Aglave et al. (Australas. J. Combin. 76 (2020) 73–86).

**Décision à la fin de la Phase 0** (écris-la noir sur blanc) :

- Si une borne visée a déjà été améliorée → STOP sur cette cible. Rapporte, puis passe à la suivante dans l'ordre m(6) → m(7) → m(9) → m(5) → m(8).
- Si tout est libre → GO, et tu me montres le rapport **avant** de lancer les calculs longs (plus de 2 h).

---

## 3. Fondations mathématiques à implémenter et à comprendre

### 3.1 La reformulation clé : un problème de couverture

H est non 2-colorable **si et seulement si**, pour **toute** partition (R, B) de V, il existe une arête e ⊆ R ou e ⊆ B. On peut donc voir le problème ainsi :

- l'univers est l'ensemble des 2-colorations de V, soit 2^(|V|−1) colorations à symétrie rouge/bleu près ;
- chaque n-ensemble e « couvre » les colorations où il est monochromatique ;
- m(n) sur v sommets est le **nombre minimum de n-ensembles qui couvrent toutes les colorations** : c'est un set cover géant.

Cette reformulation permet une approche **CEGAR** (counterexample-guided), décrite en §4.2, qui génère les colorations de façon paresseuse au lieu de les énumérer toutes.

### 3.2 Remarques de structure à exploiter (prouve-les ou vérifie-les avant de t'en servir)

- **Colorations déséquilibrées.** Si une classe de couleur contient au plus n−1 sommets, aucune arête n'y tient. Il faut donc que toute partie de taille ≥ v−n+1 contienne une arête. C'est une condition de type Turán : le complément des arêtes ne doit contenir aucun (v−n+1)-ensemble indépendant.
- **Sommets nécessaires.** Avec v ≤ 2n−2 sommets, il existe une coloration où chaque classe a ≤ n−1 sommets, donc il faut v ≥ 2n−1. Avec v = 2n−1, il faut toutes les arêtes possibles, soit C(2n−1, n), ce qui est énorme. Les bonnes constructions ont un nombre intermédiaire de sommets : 7 pour n=3, 11 pour n=4, et pour m(5) = 51 le nombre de sommets est **à reconstruire**.
- **Les designs sur exactement 2n points échouent souvent.** Exemple : S(5,6,12) a 132 blocs, mais il est 2-colorable. Le complément d'un bloc est un bloc, donc il suffit de colorer un 6-ensemble non-bloc et son complément. Sers-t'en comme test unitaire du vérificateur : il doit trouver cette coloration.
- **Criticité.** Une construction minimale est arête-critique : retirer n'importe quelle arête la rend 2-colorable. Lovász : deux arêtes s'intersectent en un seul sommet. Utilise ces conditions comme filtres rapides.
- **Constructions récursives connues** (implémente-les toutes et reproduis la table) :
  - le produit d'Abbott–Moser, m(ab) ≤ m(a)·m(b)^a : remplace chaque sommet d'un hypergraphe a-uniforme par une copie d'un hypergraphe b-uniforme ; écris la construction exacte et vérifie-la ;
  - Abbott–Hanson : m(n) ≤ 2^(n−1) + n·m(n−2) pour n impair, et une variante pour n pair ;
  - la récurrence d'Aglave et al. : m(n) ≤ 2^(n−1) + C(n, n/2)/2 + n·m(n−2) pour n pair, et la version fondée sur un hypergraphe A (n−2)-uniforme non 2-colorable quelconque, m(n) ≤ m_A(n) ;
  - les constructions de Mathews–Panda–Shannigrahi pour m(8), m(13), etc.

**Premier livrable de code** : `constructions/` doit reproduire exactement les bornes de la table pour n = 3..9. Chaque hypergraphe est exporté en fichier, vérifié non 2-colorable, et son nombre d'arêtes est égal à la borne publiée. Tant que ce n'est pas fait, aucune recherche nouvelle.

---

## 4. Stratégies de recherche (dans cet ordre, mesure tout)

### 4.1 Amélioration locale des constructions connues (rapide, à faire en premier)

Pars de la construction à 147 arêtes pour m(6), puis de celle à 421 pour m(7) :

- **Réduction gloutonne** : retire une arête et teste la 2-colorabilité. Si la construction reste non 2-colorable, garde le retrait. Essaie tous les ordres, ou des ordres aléatoires répétés.
- **Mouvements locaux** : remplace un sommet d'une arête par un autre, fusionne deux sommets, retire un sommet et réparé les arêtes.
- **Recherche locale / recuit simulé**, avec pour objectif de minimiser le nombre de colorations propres survivantes. Le calcul se fait en C, par énumération en bitmask si v ≤ 30, sinon par comptage #SAT approximatif ou par l'échantillonnage de colorations « difficiles ».
- Réutilise les colorations témoins : à chaque échec, la coloration propre trouvée par le solveur dit **quelle arête ajouter ou modifier**.

### 4.2 CEGAR exact avec symétrie (le cœur du projet)

Pour v sommets donnés et un groupe G agissant sur V (Z_v cyclique, Z_p ⋊ Z_k affine, produits, PSL(2,q), groupes de designs connus) :

1. Les variables de décision sont les G-orbites de n-ensembles, sélectionnées ou non. Le coût est la somme des tailles des orbites choisies.
2. Lance un solveur maître (MaxSAT ou ILP, c'est-à-dire PySAT RC2, OR-Tools CP-SAT ou HiGHS) qui choisit des orbites de coût minimal couvrant toutes les colorations **connues**.
3. L'oracle, un solveur SAT (CaDiCaL ou kissat via PySAT), cherche une 2-coloration propre de l'hypergraphe proposé.
   - Si UNSAT → l'hypergraphe est non 2-colorable. On a un candidat ; on certifie (§6) et on resserre la borne de coût.
   - Si SAT → on ajoute la coloration, **et toute son orbite sous G**, comme contrainte « au moins une orbite choisie la rend monochromatique », puis on recommence.
4. Itère avec une borne de coût décroissante : cherche une construction de coût < 147 (ou < record actuel).

Paramètres à balayer, à consigner dans `runs/`, avec pour chaque essai le temps, le nombre d'itérations CEGAR et le résultat :

- pour n=6 : v de 11 à environ 30, avec différents groupes ;
- pour n=5 : v de 9 à environ 26, avec la cible ≤ 50 arêtes ;
- pour n=7 : v de 13 à environ 35, avec la cible < 421.

Commence par les v et les groupes qui donnent le moins d'orbites. Deux sanity checks avant toute recherche nouvelle : **retrouver m(3) = 7** sur 7 sommets avec Z_7, et **retrouver m(4) ≤ 23** sur 11 sommets.

### 4.3 Bibliothèque de candidats structurés

Teste systématiquement, en vérifiant la non-2-colorabilité puis en essayant la réduction de §4.1 :

- designs et t-designs connus de taille de bloc 5, 6 ou 7 (Steiner, quasi-symétriques, designs de Witt et leurs dérivés/résidus) ;
- hypergraphes de type Paley ou résidus quadratiques ;
- hypergraphes cycliques à différences ;
- unions de copies décalées de Fano et de Seymour ;
- « blow-ups » partiels du produit d'Abbott–Moser.

Avant tout calcul, note pour chaque famille une raison mathématique de penser qu'elle peut marcher.

### 4.4 Nouvelles récurrences (optionnel, si 4.1 à 4.3 donnent quelque chose)

Si tu trouves m(6) ≤ X avec X < 147, recalcule toutes les bornes dérivées par les récurrences connues : m(8), m(12), m(18), m(36), etc. Chaque amélioration dérivée est un résultat de plus, à lister séparément.

### 4.5 Évolution guidée par LLM (seulement si 4.2 cale)

Une boucle de style AlphaEvolve ou FunSearch. Tu écris des générateurs Python d'hypergraphes paramétrés, avec pour score le nombre d'arêtes si la construction est non 2-colorable, et sinon une pénalité égale au nombre de colorations survivantes. Ensuite tu itères sur le code des générateurs. Garde un journal des meilleures idées.

---

## 5. Outils (Mac, CPU uniquement)

- Python 3.11+ avec `python-sat` (CaDiCaL, kissat, RC2), `ortools`, `numpy`, `networkx` et `sympy`.
- En C, `cc -O3 -march=native` pour l'énumérateur bitmask.
- `drat-trim` et `cake_lpr` (vérifié formellement) pour les preuves UNSAT.
- `kissat` ou `cadical` en binaire, compilés depuis les sources, pour produire les preuves DRAT/LRAT.
- Optionnel : `nauty`/`traces` pour les groupes d'automorphismes et la déduplication par isomorphisme.

Arborescence :

```
erdos901/
  reports/      phase0.md, journal.md (une entrée datée par session), final.md
  constructions/ reproduction des bornes connues (n=3..9)
  search/       local.py, cegar.py, candidates.py, evolve.py
  verify/       check_bruteforce.c, check_sat.py, make_cnf.py, README.md
  certs/        <n>_<edges>_<v>/ : edges.txt, H.cnf, proof.drat|lrat, check logs, sha256
  runs/         logs de runs (rotation, taille max)
  drafts/       note.tex, erdosproblems_comment.md, oeis_comment.md (BROUILLONS)
```

---

## 6. Certification (exigence absolue avant de me dire « trouvé »)

Pour tout candidat H (n-uniforme, v sommets, E arêtes) :

1. **Format.** `edges.txt` contient une arête par ligne, avec les sommets de 0 à v−1. Vérifie l'uniformité, l'absence de doublons et E < record.
2. **Vérificateur A, force brute en C.** Il énumère les 2^(v−1) colorations (le sommet 0 est fixé rouge), chaque arête étant un masque de bits. Il doit trouver qu'aucune coloration n'est propre. C'est faisable jusqu'à v ≈ 34 sur un Mac, en multithread.
3. **Vérificateur B, SAT plus preuve.**
   - On génère la CNF : une variable par sommet, et deux clauses par arête (« au moins un rouge » et « au moins un bleu »), plus x₀ = vrai.
   - On résout avec kissat ou CaDiCaL, ce qui doit donner UNSAT avec une preuve DRAT ou LRAT.
   - On valide la preuve avec `drat-trim` **et** `cake_lpr`.
4. Les deux vérificateurs doivent être écrits **indépendamment** du code de recherche, sans import partagé. `make_cnf.py` doit faire moins de 40 lignes, lisibles par un humain.
5. **Tests négatifs.** On retire chaque arête à tour de rôle et on vérifie que le vérificateur trouve alors une coloration propre. C'est le test de criticité ; il n'est pas obligatoire pour la borne, mais on le documente.
6. **Tests de sanity** des vérificateurs : Fano (non 2-colorable), Fano moins une arête (2-colorable), S(5,6,12) (2-colorable) et la construction m(4) = 23.
7. Calcule le `sha256` de chaque fichier et écris un `certs/.../README.md` qui permet de tout revérifier en 3 commandes.
8. Calcule le groupe d'automorphismes et une description humaine de la construction (« Z_v-orbites de … »). Une construction explicable vaut beaucoup plus qu'une liste opaque.

Ce n'est qu'après ces étapes que tu m'écris un rapport : **« NOUVELLE BORNE : m(n) ≤ X (record précédent Y, source Z) »**, accompagné des commandes de vérification.

---

## 7. Planning et points de contrôle

- **Session 1** : Phase 0 complète, puis rapport, et tu attends mon GO.
- **Session 2** :
  - vérificateurs A et B avec leurs tests de sanity ;
  - reproduction des constructions de la table (§3.2) ;
  - retrouver m(3) et m(4) par CEGAR.
- **Sessions 3 et plus** :
  - §4.1 sur m(6) puis m(7) ;
  - §4.2 en balayage ;
  - un résumé dans `journal.md` à la fin de chaque session : ce qui a été tenté, les meilleurs scores, l'espace couvert et la suite.
- **Critère d'abandon d'une stratégie** : environ 24 h de calcul sans progrès du meilleur score. Tu le documentes et tu passes à la suivante.
- Toutes les **2 à 3 heures** de travail autonome, tu me fais un point de 5 lignes maximum. Je veux des données, pas de blabla.

---

## 8. Si on trouve : livrables (tous en brouillon)

1. `drafts/note.tex` : une note de 4 à 8 pages en anglais, du type « An improved upper bound for m(6) in Property B ». Elle contient :
   - l'énoncé, l'historique avec les citations exactes, et la construction ;
   - une preuve **lisible par un humain** si possible ; sinon, la description du certificat ;
   - la reproductibilité.
   - Auteur : Joaquim Manji-Jung, Paris. Pas d'université, pas d'e-mail.
2. `drafts/erdosproblems_comment.md` : un commentaire court et factuel pour le fil #901, avec la borne, le lien vers le dépôt et les commandes de vérification.
3. `drafts/oeis_comment.md` : une proposition de commentaire pour A392185.
4. Le dépôt GitHub public, prêt mais **non poussé**. Il contient `certs/`, `verify/` et le README, avec des commits sous mon nom uniquement.
5. Une liste des personnes à qui l'envoyer pour relecture (auteurs d'Aglave et al., Östergård), avec un **brouillon** d'e-mail. Je valide et j'envoie moi-même.

## 9. Si on ne trouve pas

`reports/final.md` doit contenir :

- l'espace exactement couvert (v, groupes, bornes de coût), avec les résultats « aucune construction G-invariante sur v sommets avec ≤ E arêtes », chacun certifié par la terminaison de la boucle CEGAR (preuve UNSAT du maître si possible) ;
- les meilleures constructions trouvées, même si elles ne battent pas le record ;
- les leçons tirées et les pistes restantes.

Ce rapport doit être assez propre pour un commentaire sur erdosproblems.com, en brouillon.

---

## 10. Références (à lire et à citer exactement après vérification)

- P. Erdős, On a combinatorial problem I (1963) et II (1964), Acta Math. Hungar.
- H. L. Abbott, L. Moser, On a combinatorial problem of Erdős and Hajnal (1964).
- H. L. Abbott, D. Hanson, On a combinatorial problem of Erdős, Canad. Math. Bull. (1969).
- P. D. Seymour (1974), B. Toft (1975) : m(4) ≤ 23.
- P. R. J. Östergård, On the minimum size of 4-uniform hypergraphs without property B, Discrete Appl. Math. 163 (2014) 199–204.
- J. Radhakrishnan, A. Srinivasan, Improved bounds and algorithms for hypergraph 2-coloring (2000).
- H. Gebauer, On the construction of 3-chromatic hypergraphs with few edges, JCTA (2013).
- J. Mathews, M. K. Panda, S. Shannigrahi, On the construction of non-2-colorable uniform hypergraphs, Discrete Appl. Math. (2015).
- S. Aglave, V. A. Amarnath, S. Shannigrahi, S. Singh, Improved bounds for uniform hypergraphs without property B, Australas. J. Combin. 76 (2020) 73–86 (arXiv 1602.00218).
- arXiv 2403.05674, Improved lower bounds for property B (m(5) ≥ 32).
- S. K. Jha (sept. 2026) et le dépôt GitHub AyushAg1002/property-b-m5-lower33 (m(5) ≥ 33) : uniquement pour l'état de l'art et les méthodes.
- erdosproblems.com/901 ; google-deepmind/formal-conjectures issue #2363 ; OEIS A392185.
- B. Georgiev, J. Gómez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale (arXiv 2511.02864) : pour vérifier que le problème n'y figure pas, et pour la méthode d'évolution.

---

**Première action :** lance la Phase 0, écris `reports/phase0.md`, puis arrête-toi et montre-moi le tableau des bornes reconstitué et la décision GO/STOP pour chaque cible.
