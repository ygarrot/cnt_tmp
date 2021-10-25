# EDA (Exploratory Data Analysis)
	souvent associe a Statistique utilisant un graphique

	Techniques:
		1. Tracer les donées brutes:
			data traces, histograms, bihistograms, probability plots, lag plots, block plots, and Youden plots.

		2. Tracer des statistiques simples:
			 mean plots, standard deviation plots, box plots

		3. Positioner les tracer de sortes a reconaitre des patternes,
			pour cela on peut afficher plusieurs tracer par page (pour pouvoir facilement les comparer).

EDA vs analyse Bayesienne vs Analyse classique

	For classical analysis, the sequence is
		Problem => Data => Model => Analysis => Conclusions
	For EDA, the sequence is
		Problem => Data => Analysis => Model => Conclusions
	For Bayesian, the sequence is
		Problem => Data => Model => Prior Distribution => Analysis => Conclusions

Pour l'analyse classique, la collecte de données est suivit de l'application d'un model

Pour l'EDA la collecte de données est suivit d'une analyse pour savoir quel model utiliser


Model

Classique:

## Traitement de la donnée

Les techniques d'estimation classiques ont la particularité de prendre toutes les données et de les cartographier en quelques nombres ("estimations").
L'avantage est que ces quelques chiffres se concentrent sur des caractéristiques importantes (localisation, variation, etc.) de la population.
Le vice est que se concentrer sur ces quelques caractéristiques peut filtrer d'autres caractéristiques (asymétrie, longueur de queue, autocorrélation, etc.) de la même population.
En ce sens, il y a une perte d'information due à ce processus de "filtrage".

L'approche EDA, en revanche, utilise souvent (et montre) toutes les données disponibles. En ce sens, il n'y a pas de perte d'informations correspondante.

[[Hypotheses]]

La "bonne nouvelle" de l'approche classique est que les tests basés sur des techniques classiques sont généralement très sensibles -
c'est-à-dire que si un véritable changement d'emplacement, disons, s'est produit, de tels tests ont souvent le pouvoir de détecter un tel changement et de conclure qu'un tel changement est "statistiquement significatif".

La « mauvaise nouvelle » est que les tests classiques dépendent d'hypothèses sous-jacentes (par exemple, la normalité), et donc la validité des conclusions des tests devient dépendante de la validité des hypothèses sous-jacentes.
Pire encore, les hypothèses sous-jacentes exactes peuvent être inconnues de l'analyste, ou si elles sont connues, non testées.
Ainsi, la validité des conclusions scientifiques devient intrinsèquement liée à la validité des hypothèses sous-jacentes.
En pratique, si de telles hypothèses sont inconnues ou non testées, la validité des conclusions scientifiques devient suspecte.

