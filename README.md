# Machine-Learning

# Objectif du projet :

 Nous avons récupéré les données sur le site VandB, un site de vente d'alcool (Bières vins, ... ) et 
 nous nous sommes concentrées sur les données concernant les vins, dans le but de prédire un prix optimal 
 selon les caractéristiques des vins. Et également de générer une application qui permet de 
 fournir les 3 meilleurs vins selon les filtres de l'utilisateur. 

 Les variables récupérées sont les suivantes : 
 
    - Prix : Variable numérique continue 
    - Millésime : l'année du vins, variable catégorielle 
    - Degrés d'alcool : variable numérique
    - Cépage : la variété de vigne qui donne le raison du vin, 
    variable catégorielle 
    - Appélation : variable catégorielle
    - Marque : est le domaine du vin, variable catégorielle
    - couleur : variable catégorielle à quatre modalités
    - type d'agriculture : variable catégorielle à quatre modalités
    - taux de sucre : variable catégorielle à 6 modalitées
    - origine : variable catégorielle   
    - stock : si le vin est en stock ou non, variable catégorielle
    - Carafage : si le vin peut être carafé, variable catégorielle
    - vivacité : variable numérique comprise entre 0 et 100
    - fruité : variable numérique comprise entre 0 et 100
    - épicé boisé : variable numérique comprise entre 0 et 100
    - puissance :variable numérique comprise entre 0 et 100

 Nous avons effectuer le scraping avec selenium sur le site
 de `vandb.fr` .Plusieurs fonctions ont été créées pour 
 récupérer les données de chaque vins.  
 
# Les librairies  : 

## Pour la librairie `lib_scrapping.py` :
Dans le terminal : python -m poetry run python -m ML_Miguel_Diot scrapping

La librairie récupère les données du site et renvoie un json 
avec les données récupérées.

## Pour la librairie `lib_nettoyage.py`:
Dans le terminal : python -m poetry run python -m ML_Miguel_Diot nettoyage

La librairie récupère le json créé lors de l'étape de scrapping pour nettoyer
les données et renvoie un json avec les données nettoyées.

Des dummies sont créer pour les variables catégorielles.

Les variables tels que les degrées, les sulfites, les prix, les couleurs, 
les types d'agricultures, le carafage et les origines sont formatés.

## Pour les librairies `lib_ modeles.py` et `lib_appli_modeles.py`:
Dans le terminal : python -m poetry run python -m ML_Miguel_Diot modele

Dans cette librairie, les variables influançant le prix (notre variable cible)
sont selectionnées par la méthode de la variance. 

La variable cible étant un variable numérique continue,(le prix), 
les modeles tester sont des modèles de régressions.
Les modèles sont : ElasticNet, RandomForest, K plus proche voisins,
Ridge, MLP Regressor, SVR, Regression Gausienne.

Les meilleurs paramètres de chaques modèles sont choisit et les modèles 
font une CV = 4. Un tableau est généré avec le score sur les données test, 
d'entraînement, le score moyen des cross-validation et la dispersion des
scores de cross-validation. 

Le meilleur modèle est sélectionné via le score moyen des cross-validation, 
on prend le plus élevé. 

Les prix rationnels sont ensuite calculés grâce au meilleur modèle
sélectionné pour chaque vin de notre base de données. 

On crée ensuite une nouvelle variable qui correspont à la différence de prix
entre le prix réel et le prix rationnel du vin. C'est cette variable qui 
permet de nous indiquer si le vin est intéressant niveau prix. 


## Pour lancer la librairie `lib_selection.py` : 
Dans le terminal :python -m poetry run python -m ML_MIGUEL_DIOT calcule
         
Permet de donner les 3 meilleurs vins en fonction de la différence de prix 
entre le prix affiché et le prix de prédiction en fonction des caractéristiques
fournit par l'utilisateur via l'application (dans le terminal). 

Il faut renter les caractéristiques souhaités pour les variables :

         - couleur : Rouge, Blance, Rosé, Effervescent, Indifférent
         - prix : la tranche de prix souhaitée 
         - origine : FRANCE, AMERIQUE, EUROPE_HORS_FR, AUSTRALIE, AFRIQUE, Indifférent
         - taux de sucre :  liquoreux, moelleux, demi-sec, sec, brut, Indifférent
         - sulfites : Oui, Non, Indifférent
         - type d'agriculture :  Biologique, Raisonné, Indifférent

Par exemple : 

        >>> "Quelle est la couleur du vin que vous souhaitez ?"
            "Vous avez le choix entre rouge, rosé, blanc, effervescent ou indifférent.
        Dans le terminal : blanc
        >>> "Veuillez entrer le prix minimum :  "
        Dans le terminal : 0
        >>> "Veuillez entrer le prix maximum :  "
        Dans le terminal : 100
        >>> "Veuillez entrer le taux de sucre souhaité."
        "Vous avez le choix entre liquoreux, moelleux, demi-sec, sec, brut ou indifférent.  "
        Dans le terminal : moelleux
        >>> "Veuillez entrer le type d'agriculture (Biologique/raisonné/indifférent) :"
        Dans le terminal : Indifférent
        >>> "Origine du produit (FRANCE, AMERIQUE, EUROPE_HORS_FR, AUSTRALIE, AFRIQUE, indifférent): "
        Dans le terminal : Indifférent  
        >>> Top 1 : C'est un vin du domaine DOMAINE SYLVIE SPIELMANN dont le prix est de : 33.9 €.
            Top 2 : C'est un vin du domaine DOMAINE DU BOIS DE POURQUIE dont le prix est de : 9.5 €.
            Top 3 : C'est un vin du domaine CHÂTEAU DU MONT dont le prix est de : 11.5 €.
            A bientôt ! """
        
# Conclusion et limites :

 Les modèles de prédiction ont des scores assez mauvais (inférieur à 0.5).
 Ces scores peuvent s'expliquer par le nombre de vins disponibles dans notre
 base de données, effectivement elle est constituée de 649 vins (ce qui est peu). 
 
 Il aurait été également intéressant de rajouter une variable "note" qui permet 
 de capter si les consommateurs étaient satisfait ou non de leur vin.
 Une limite supplémentaire existe,
 le scraping à été effectué avec selenium seulement, ce qui n'est pas optimal
 si l'architecture du site change.    
