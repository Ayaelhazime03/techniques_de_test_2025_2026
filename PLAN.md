# PLAN DE TEST – Triangulator (Séance 1)

## Introduction
Le projet consiste à développer un microservice appelé **Triangulator**, qui calcule la triangulation d’un ensemble de points 2D.  
L’objectif de cette première séance est de définir un **plan de tests** permettant de vérifier que l’algorithme fonctionne correctement, est robuste face aux cas limites et reste performant sur différents ensembles de points.

---

## Objectifs des tests
- Vérifier la **justesse de la triangulation** sur des ensembles simples et connus.  
- Tester la **robustesse** de l’algorithme face à des cas limites (points alignés, dupliqués, jeu vide, valeurs extrêmes).  
- Mesurer la **performance** du Triangulator sur des ensembles de points de tailles variables.  
- Suivre une démarche **test-first**, en préparant les tests avant l’implémentation.

---

## Types de tests prévus

### 1. Tests unitaires
**Pourquoi** : Pour s’assurer que l’algorithme renvoie les triangles corrects et respecte la logique mathématique.  
**Comment** : Les `PointSet` sont générés directement dans les tests et la sortie `Triangles` est comparée à la solution attendue.

| Cas de test       | Entrée                     | Résultat attendu             | Objectif                                   |
|------------------|----------------------------|-----------------------------|--------------------------------------------|
| Triangle minimal  | 3 points non alignés       | 1 triangle correct          | Vérifier la triangulation minimale         |
| Points alignés    | 3 points alignés           | Aucun triangle              | Gérer les cas sans triangle                |
| Carré             | 4 points formant un carré  | 2 triangles corrects        | Vérifier triangulation d’un polygone simple |
| Points dupliqués  | Points identiques présents | Triangles corrects ou comportement défini | Robustesse face aux doublons              |
| Jeu vide          | Aucun point                | Aucun triangle              | Robustesse pour entrée vide                |


---

### 2. Tests de performance
**Pourquoi** : L’algorithme peut devenir coûteux pour des ensembles nombreux.  
**Comment** : Mesurer le temps nécessaire pour trianguler des ensembles de tailles croissantes (10, 100, 1000 points).  
**Objectif** : Vérifier que l’algorithme reste rapide et stable.

---

### 3. Tests de robustesse
**Pourquoi** : S’assurer que le Triangulator ne plante jamais et gère correctement tous les cas limites.  
**Comment** : Tester des configurations extrêmes :
- Points avec coordonnées très grandes ou très petites  
- Points alignés ou dupliqués  
- Jeu vide  
**Objectif** : L’algorithme doit renvoyer un résultat cohérent ou lever une erreur contrôlée.

---

## Organisation du projet
- Tous les tests sont **centrés sur le Triangulator**, pas sur le PointSetManager ni la conversion binaire.  
- Structure prévue :


## Conclusion
Ce plan définit les principaux tests pour valider l’algorithme de triangulation avant toute implémentation, conformément à la démarche **test-first**.  




### Annexe — Checklist de la séance 1 (à cocher)

* [ ] `PLAN.md` ajouté (✔)
* [ ] `tests/` créé
* [ ] `tests/fixtures/gen_pointset.py` ajouté
* [ ] Squelettes : `tests/unit/test_binary_format.py`, `tests/unit/test_triangulation_algo.py`
* [ ] Squelettes : `tests/api/test_triag_api.py`
* [ ] `Makefile` minimal ajouté


