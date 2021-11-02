Cette partie se fera en utilisant influxdb quand base de donnée et a l'aide de query flux

1. Afficher un graphique temporel
	![ChAg](./1.png)
	fonction conseillées:
		filter
		truncateTimeColumn
	1.1 un peu de couleur
		![](./2.png)
		![](./3.png)
		![](./4.png)
	
2. Variables
	Pour eviter de devoir créer un graphe pour chaque parametre dans notre cas pour chaque etat de la vache ou pour chaque parametre raw, grafana propose des variables.
	Ces variables permettes a l'utilisateur de customiser son dashboard.
	![](./query_variable_raw)
	
	2.1 Query Variables
		A l'aide de requetes influxdb vous pouvez creer des variables.
		Ca peut etre utile pour recuperer toute les cow_id ou event_id
		
	2.2 Query dependencies
		Vous pouvez utiliser vos variables pour faire de nouvelles requetes 
		![](./query_dependencies)