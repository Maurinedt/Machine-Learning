"""Description. 

Librarie permettant de donner les 3 premiers meilleurs vins
selon les caractéristiques entrées par l'utilisateur."""

from rich import print

import pandas as pd


def selections_carac(couleur, prix_bis, origine, data):
    """Selection des données via la couleur, le prix (correspond à [prix_bas, prix_haut])
    et l'origine. Ces données sont fournies par l'utilisateur."""
    if couleur == "Indifférent":
        data = data
    else:
        data = data[data[couleur.upper()] == 1]
    if origine == "Indifférent":
        data = data
    else:
        data = data[data[origine.upper()] == 1]
    data3 = data.loc[
        (data["PRIX"] >= float(prix_bis[0])) & (data["PRIX"] <= float(prix_bis[1]))
    ]
    return data3


def selection_carac_tech(
    couleur, prix_bis, origine, taux_de_sucre, sulfites, type_agriculture, data
):
    """Selection des données via la couleur,
    le prix, l'origine, le taux de sucre, le type 
    d'agriculture et la présence ou non de sulfites. Ces données sont fournies par 
    l'utilisateur"""
    data = selections_carac(couleur, prix_bis, origine, data=data)
    if type_agriculture == "Indifférent":
        data1 = data
    else:
        data1 = data[data[type_agriculture] == 1]
    if sulfites == "Oui":
        data2 = data1[data1["SULFITES"] == 1]
    elif sulfites == "Indifférent":
        data2 = data1
    else:
        data2 = data1[data1["SULFITES"] == 0]
    if taux_de_sucre == "Liquoreux":
        data_final = data2[data2["TAUX_DE_SUCRE"] == 5]
    elif taux_de_sucre == "Moelleux":
        data_final = data2[data2["TAUX_DE_SUCRE"] == 4]
    elif taux_de_sucre == "Demi-sec":
        data_final = data2[data2["TAUX_DE_SUCRE"] == 3]
    elif taux_de_sucre == "Sec":
        data_final = data2[data2["TAUX_DE_SUCRE"] == 2]
    elif taux_de_sucre == "indifférent":
        data_final = data2
    else:
        data_final = data2[data2["TAUX_DE_SUCRE"] == 1]
    return data_final


def resultat(
    couleur, prix_bis, origine, taux_de_sucre, sulfites, type_agriculture, data
):
    """Nous fournit dans le terminal les 3 meilleurs vins selon les caractéritiques 
    entrées par l'utilisateur.
    Si aucun vin ne correspond à la recherche, le message 
    'aucun vin ne correspond à votre recherche' s'affichera dans le terminal"""
    data_bis = selections_carac(couleur, prix_bis, origine, data=data)
    data_selec_final = selection_carac_tech(
        couleur,
        prix_bis,
        origine,
        taux_de_sucre,
        sulfites,
        type_agriculture,
        data=data_bis,
    )
    if len(data_selec_final) == 0:
        return f"Aucun vin correspondant à votre recherche"
    else:
        data = data_selec_final.sort_values(by="diff_prix").head(3)
        data = pd.DataFrame(data)
        for i in range(len(data)):
            marque = data["MARQUE"]
            marque_liste = marque.tolist()
            prix = data["PRIX"]
            prix_liste = prix.tolist()
            print(
                f"Top {i+1} : C'est un vin du domaine {marque_liste[i]} dont le prix est de : {prix_liste[i]} €."
            )
    return f"A bientôt !"
