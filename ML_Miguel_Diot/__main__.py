"""Description.
Application ligne de commande.
Vous pouvez lancer via le terminal : le scraping, le nettoyage, la sélection du meilleur modèle,
et l'application qui filtre les caractéristiques en fonction du consommateur.
"""
from serde.json import to_json, from_json
import typer
import pandas as pd
from rich import print
from .data import Donnees
from .lib_selections import resultat
from .lib_Scraping import recuperation_scrapping
from .lib_appli_modele import prix
from .lib_nettoyage import data_nettoyer

application = typer.Typer()


@application.command()
def scraping():
    """Fonction qui lance le scrapping avec ttes les fonctions
    de la librarie lib_scraping et génère un fichier json.
    Exemple : 
        Dans le terminal : python -m poetry run python -m ML_Miguel_Diot scraping"""
    url = "https://vandb.fr/113469/bouteille/"
    recuperation_scrapping(url)


@application.command()
def nettoyage():
    """Fonction qui lance le nettoyage avec ttes les fonctions
    de la librarie lib_nettoyage et génère un json.
    Exemple : 
        Dans le terminal : python -m poetry run python -m ML_Miguel_Diot nettoyage"""
    with open("data_scrapping.json") as mon_fichier:
        code = mon_fichier.read()
        data1 = pd.read_json(code)
    data_nettoyer(
        variables=["COULEUR", "TYPE_AGRICULTURE", "APPELATION_bis", "ORIGINE"], df=data1
    )


@application.command()
def modele():
    """Fonction qui lance le modèle avec ttes les fonctions
    de la librarie lib_modele et génère un json avec les prédictions du prix pour chaque
    vin.
    Exemple : 
        Dans le terminal : python -m poetry run python -m ML_Miguel_Diot modele"""
    with open("data_nettoye.json") as mon_fichier:
        code = mon_fichier.read()
        data1 = pd.read_json(code)
    prix(data1)


@application.command()
def exemple():
    """Fonction qui demande les caractéristiques souhaitées de l'utilisateur
    et les stockent dans un json.
    Exemple : 
        Dans le terminal : python -m poetry run python -m ML_Miguel_Diot exemple
        >>> "Quelle est la couleur du vin que vous souhaitez ?"
            "Vous avez le choix entre rouge, rosé, blanc, effervescent ou indifférent.
        Dans le terminal : Rouge
        >>> "Veuillez entrer le prix minimum :  "
        Dans le terminal : 10
        >>> "Veuillez entrer le prix maximum :  "
        Dans le terminal : 50
        >>> "Veuillez entrer le taux de sucre souhaité."
        "Vous avez le choix entre liquoreux, moelleux, demi-sec, sec, brut ou indifférent.  "
        Dans le terminal : Indifférent
        >>> "Veuillez entrer la présence de sulfites. \n"
            "Vous avez le choix entre Oui, Non, indifférent."
        Dans le terminal : Indifférent
        >>> "Veuillez entrer le type d'agriculture (Biologique/raisonné/indifférent) :"
        Dans le terminal : Indifférent
        >>> "Origine du produit (FRANCE, AMERIQUE, EUROPE_HORS_FR, AUSTRALIE, AFRIQUE, indifférent): "
        Dans le terminal : Indifférent            
    """
    q_couleur = str(
        input(
            "Quelle est la couleur du vin que vous souhaitez ? \n"
            "Vous avez le choix entre rouge, rosé, blanc, effervescent ou indifférent. "
        )
    )
    q_prix_bas = int(input("Veuillez entrer le prix minimum :  "))
    q_prix_haut = int(input("Veuillez entrer le prix maximum :  "))
    q_taux_de_sucre = str(
        input(
            "Veuillez entrer le taux de sucre souhaité.\n"
            "Vous avez le choix entre liquoreux, moelleux, demi-sec, sec, brut ou indifférent.  "
        )
    )
    q_sulfites = str(
        input(
            "Veuillez entrer la présence de sulfites. \n"
            "Vous avez le choix entre Oui, Non, indifférent."
        )
    )
    q_type_agriculture = str(
        input(
            "Veuillez entrer le type d'agriculture (Biologique/raisonné/indifférent) :  "
        )
    )
    q_origine = str(
        input(
            "Origine du produit (FRANCE, AMERIQUE, EUROPE_HORS_FR, AUSTRALIE, AFRIQUE, indifférent): "
        )
    )

    # On ajoute maintenant les infos entrées dans notre class Donnees
    # On met à la forme que l'on souhaite
    exemple = Donnees(
        couleur=q_couleur.capitalize(),
        prix_bis=[q_prix_bas, q_prix_haut],
        taux_de_sucre=q_taux_de_sucre.capitalize(),
        sulfites=q_sulfites.capitalize(),
        type_agriculture=q_type_agriculture.capitalize(),
        origine=q_origine.capitalize(),
    )
    code = to_json(exemple)

    with open("donnee_conso.json", "w") as fichier:
        fichier.write(code)


@application.command()
def calcule():
    """Fonction qui fournit les 3 meilleurs vins avec les données entrées par l'utilisateur.
    Permet de lancer toute l'application.
    Exemple :  
        Dans le terminal : python -m poetry run python -m ML_Miguel_Diot calcule
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
    exemple()
    with open("donnee_conso.json", "r") as fichier:
        code = fichier.read()
    donnees = from_json(Donnees, code)

    with open("data_avec_prix.json") as mon_fichier:
        code = mon_fichier.read()
        data2 = pd.read_json(code)

    solution = resultat(
        prix_bis=donnees.prix_bis,
        couleur=donnees.couleur,
        origine=donnees.origine,
        taux_de_sucre=donnees.taux_de_sucre,
        sulfites=donnees.sulfites,
        type_agriculture=donnees.type_agriculture,
        data=data2,
    )
    print(solution)


if __name__ == "__main__":
    application()

