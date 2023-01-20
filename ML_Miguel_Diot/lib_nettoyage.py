"""librairie.
Fonctions qui permettent de nettoyer la base de données."""
import pandas as pd
import numpy as np


def transforme(df):
    """Fonction qui transforme les données en un formatage souhaité. 
    """
    df = pd.read_json("data_scrapping.json")
    # Pour les degrés d'alcool
    df["DEGREE"] = df["DEGREE"].str.replace("ALC. ", "").str.replace(" % VOL.", "")
    # Pour les sulfites
    df["SULFITES"] = (
        df["SULFITES"]
        .str.replace("Oui", "1")
        .str.replace("Contient des sulfites", "1")
        .str.replace("Non", "0")
    )
    # Pour les prix
    df["PRIX"] = df["PRIX"].str.replace(" €", "").str.replace(",", ".")
    # Pour la capacité
    df["CAPACITE"] = df["CAPACITE"].str.replace(" L", "")
    # Pour la couleur:
    df["COULEUR"] = (
        df["COULEUR"]
        .str.replace("BLANC MOELLEUX", "BLANC")
        .str.replace("EFFERVESCENT BLANC", "EFFERVESCENT")
    )
    # Pour le type d'agriculture
    df["TYPE_AGRICULTURE"] = (
        df["TYPE_AGRICULTURE"]
        .str.replace("En conversion bio", "Biologique")
        .str.replace("Biodynamie", "Biologique")
    )
    # Carafage
    df["CARAFAGE"] = (
        df["CARAFAGE"]
        .str.replace("A carafer avant dégustation", "1")
        .str.replace("Ne pas carafer", "0")
    )
    # ORIGINE
    df["ORIGINE"] = (
        df["ORIGINE"]
        .str.replace("ARGENTINE", "AMERIQUE")
        .str.replace("ETATS-UNIS", "AMERIQUE")
        .str.replace("CHILI", "AMERIQUE")
    )
    df["ORIGINE"] = (
        df["ORIGINE"]
        .str.replace("PORTUGAL", "EUROPE_HORS_FR")
        .str.replace("ESPAGNE", "EUROPE_HORS_FR")
        .str.replace("ITALIE", "EUROPE_HORS_FR")
        .str.replace("RÉPUBLIQUE DE MOLDOVA", "EUROPE_HORS_FR")
    )
    #Taux de sucre
    df["TAUX_DE_SUCRE"] = df["TAUX_DE_SUCRE"].replace(
        ["Extra Brut", "Brut", "Sec", "Demi-sec", "Moelleux", "Liquoreux"],
        [0, 1, 2, 3, 4, 5],
    )
    return df


def appelation(df):
    """Fonction qui crée une colonne APPELATION_bis avec
    les cahiers des charges de chaque appélation utilisée pour chaque vin"""
    df = df.assign(APPELATION_bis=" ")
    for i in range(len(df)):
        if "AOP" in df["APPELATION"][i]:
            df["APPELATION_bis"][i] = "AOP"
        elif "AOC" in df["APPELATION"][i]:
            df["APPELATION_bis"][i] = "AOC"
        elif "IGP" in df["APPELATION"][i]:
            df["APPELATION_bis"][i] = "IGP"
        else:
            df["APPELATION_bis"][i] = "Sans appélation"
    return df


def annees(df):
    """Fonction qui crée une colonne millesime_bis qui donne l'indication
    si le vin est millésimé ou non."""
    df = df.assign(millesime_bis=0)
    for i in range(len(df)):
        if df["MILLESIME"][i] == "Non millésimé":
            df["MILLESIME"][i] = np.nan
        else:
            df["MILLESIME"][i] = int(df["MILLESIME"][i])
            df["millesime_bis"][i] = 1
    return df


def dropnan(df):
    """Fonction qui permet d'enlever toutes les données
    manquante."""
    for col in df.columns.to_list():
        df[col].replace(np.nan, np.NaN, inplace=True)
    df.dropna(inplace=True)
    return df


def mise_type(df):
    """Fonction permettant de transformer le type de nos données."""
    df["DEGREE"] = df["DEGREE"].astype(float)
    df["FRUITE"] = df["FRUITE"].astype(int)
    df["VIVACITE"] = df["VIVACITE"].astype(int)
    df["PUISSANCE"] = df["PUISSANCE"].astype(int)
    df["EPICE_BOISE"] = df["EPICE_BOISE"].astype(int)
    df["PRIX"] = df["PRIX"].astype(float)
    df["MILLESIME"] = df["MILLESIME"].astype(int)
    df["CAPACITE"] = df["CAPACITE"].astype(float)
    df["CARAFAGE"] = df["CARAFAGE"].astype(int)
    df["SULFITES"] = df["SULFITES"].astype(int)
    return df


def creation_dummies(variables: list, df):
    """Fonction permettant de créer des dummies aux variables 
    catégorielles."""
    for i in range(len(variables)):
        dummies = pd.get_dummies(df[variables[i]]) 
        df = df.join(dummies)
        del df[variables[i]]
    return df


def data_nettoyer(variables: list, df):
    """Fonction qui permet de générer toutes les fonctions
    concernant le nettoyage. Elle génère un json."""
    data_bis = transforme(df)
    df = appelation(data_bis)
    df = annees(df)
    df = dropnan(df)
    df_bis = mise_type(df)
    df = creation_dummies(variables=variables, df=df_bis)
    df_json = df.to_json("data_nettoye.json")
    return df_json

