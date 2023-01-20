"""Description.

Test automatiques de data.
"""
from ML_Miguel_Diot.data import Donnees
import pytest


def test_donnees():
    """La valeur de retour est “True” si essai est une instance de 
    classe.
    La valeur de retour est “False” si essai n’est pas une instance de 
    classe."""
    essai = Donnees(
        couleur="Blanc",
        prix_bis=[0, 100],
        taux_de_sucre="Indifférent",
        sulfites="Oui",
        type_agriculture="Indifférent",
        origine="France",
    )
    isinstance(essai, Donnees)


def test_donnees_problematiques():
    with pytest.raises(ValueError):
        Donnees(
            couleur="Blanc",
            prix_bis=[-10, 100],
            taux_de_sucre="Indifférent",
            sulfites="Oui",
            type_agriculture="Indifférent",
            origine="France",
        )
