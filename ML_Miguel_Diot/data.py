"""Description.
Classe Permettant de représenter les données nécessaires"""

from serde import serde


@serde
# donne le type de chaque élément dans la class
class Donnees:
    couleur: str
    prix_bis: list[float]
    taux_de_sucre: str
    sulfites: str
    type_agriculture: str
    origine: str


def __post_init__(self):
    """La fonction permet de vérifier que les caractéristiques entrées correspondent aux choix possibles.
        Exemple : Dans le terminal : python -m poetry run python -m ML_Miguel_Diot calcul
        >>> "Quelle est la couleur du vin que vous souhaitez ?"
            "Vous avez le choix entre rouge, rosé, blanc, effervescent ou indifférent.
        Dans le terminal : vert
        >>> ValueError: Veuillez entrer uniquement les choix possibles pour la couleur
        >>> "Veuillez entrer le prix minimum :  "
        Dans le terminal : -10
        >>> "Veuillez entrer le prix maximum :  "
        Dans le terminal : 50
        >>> ValueError : "Le prix ne peut pas être négatif"
        >>> "Veuillez entrer le taux de sucre souhaité."
        "Vous avez le choix entre liquoreux, moelleux, demi-sec, sec, brut ou indifférent.  "
        Dans le terminal : très sucré
        >>> ValueError: Veuillez entrer uniquement les choix possibles pour le taux de sucre
        >>> "Veuillez entrer la présence de sulfites. \n"
            "Vous avez le choix entre Oui, Non, indifférent."
        Dans le terminal : Non merci
        >>> ValueError: Veuillez entrer uniquement les choix possibles pour le sulfites
        >>> "Veuillez entrer le type d'agriculture (Biologique/raisonné/indifférent) :"
        Dans le terminal : bionique
        >>> ValueError: Veuillez entrer uniquement les choix possibles pour le type d'agriculture
        >>> "Origine du produit (FRANCE, AMERIQUE, EUROPE_HORS_FR, AUSTRALIE, AFRIQUE, indifférent): "
        Dans le terminal : espagne    
        >>> ValueError: Veuillez entrer uniquement les choix possibles pour l'origine"""
    if (self.couleur).upper() not in [
        "BLANC",
        "ROSÉ",
        "EFFERVESCENT",
        "ROUGE",
        "INDIFFÉRENT",
    ]:
        raise ValueError(
            "Veuillez entrer uniquement les choix possibles pour la couleur"
        )
    for elem in self.prix_bis:
        if elem < 0:
            raise ValueError("Le prix ne peut pas être négatif")
    if (self.taux_de_sucre).upper() not in [
        "LIQUOREUX",
        "MOELLEUX",
        "DEMI-SEC",
        "SEC",
        "BRUT",
        "INDIFFÉRENT",
    ]:
        raise ValueError(
            "Veuillez entrer uniquement les choix possibles pour le taux de sucre"
        )
    if (self.sulfites).upper() not in [
        "OUI",
        "NON",
        "INDIFFÉRENT",
    ]:
        raise ValueError(
            "Veuillez entrer uniquement les choix possibles pour les sulfites"
        )
    if (self.type_agriculture).upper() not in [
        "BIOLOGIQUE",
        "RAISONNÉ",
        "INDIFFÉRENT",
    ]:
        raise ValueError(
            "Veuillez entrer uniquement les choix possibles pour le type d'agriculture"
        )
    if (self.origine).upper() not in [
        "FRANCE",
        "AMERIQUE",
        "EUROPE_HORS_FR",
        "AUSTRALIE",
        "AFRIQUE",
        "INDIFFÉRENT",
    ]:
        raise ValueError(
            "Veuillez entrer uniquement les choix possibles pour l'origine"
        )

