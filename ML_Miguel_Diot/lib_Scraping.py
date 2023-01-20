"""Librarie. 
Regroupe les fonctions qui permettent d'effectuer le scrapping sur le site vandb.fr.
"""
from selenium import webdriver
import numpy as np
import time
import json
from selenium.webdriver.common.by import By

from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)


def recuperation_page(url):
    """Récupère la page web, puis permet de générer la liste
    complète des vins et ainsi récupérer les liens href pour accéder
    aux caractéristiques."""
    browser = webdriver.Chrome()
    browser.get(url)
    try:
        accept_cookies = browser.find_element(By.ID, "axeptio_btn_acceptAll")
        browser.execute_script("arguments[0].click();", accept_cookies)
    except NoSuchElementException:
        next
    for i in range(1, 20):
        try:
            accept_cookies = browser.find_element(By.ID, "axeptio_btn_acceptAll")
            browser.execute_script("arguments[0].click();", accept_cookies)
        except NoSuchElementException:
            next
        try:
            nxt = browser.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/div/div[2]/div/div[5]/a'
            )
            time.sleep(6)
            nxt.click()
            i = i + 1
        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:
            pass
        except ElementClickInterceptedException:
            next

    elems = browser.find_elements(By.CSS_SELECTOR, ".product-visual [href]")
    links = [elem.get_attribute("href") for elem in elems]
    return links


def carac(lienbis):
    """Permet de récupérer le stock, la couleur, l'origine, l'appélation, 
    la capacité, le degrée, la marque et le prix"""
    # LE STOCK
    try:
        le_stock = lienbis.find_element(
            By.XPATH,
            './/*[@id="content"]/div[2]/div[3]/article/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/span',
        ).text
    except NoSuchElementException:
        le_stock == ""
    if le_stock == "":
        le_stock = "Disponible uniquement en magasin"
    # LA COULEUR
    try:
        la_couleur = lienbis.find_element(
            By.XPATH,
            ".//*[@id='content']/div[2]/div[3]/article/div[2]/div/div[2]/div[2]/div/div[1]/div/span[1]/div/div/div",
        ).text
    except NoSuchElementException:
        la_couleur = ""
    # L'ORIGNE
    l_origine = lienbis.find_element(By.CLASS_NAME, "origin").text
    # L'APPELATION
    try:
        l_appelation = lienbis.find_element(
            By.XPATH,
            ".//*[@id='content']/div[2]/div[3]/article/div[2]/div/div[2]/div[2]/div/div[1]/div/span[2]/div/div/div",
        ).text
    except NoSuchElementException:
        l_appelation = ""
    if l_appelation == "SANS IG":
        l_appelation = "Sans appélation"
    if l_origine == l_appelation:
        l_appelation = "Sans appélation"
    # CAPACITE, DEGREE, MARQUE ET PRIX
    la_capacity = lienbis.find_element(By.CLASS_NAME, "capacity").text
    le_degree = lienbis.find_element(By.CLASS_NAME, "degree").text
    le_brand = lienbis.find_element(By.CLASS_NAME, "brand").text
    le_prix = lienbis.find_element(By.XPATH, "(//span[@class='price-value'])[2]").text

    dict_cara = {
        "DEGREE": le_degree,
        "MARQUE": le_brand,
        "CAPACITE": la_capacity,
        "ORIGINE": l_origine,
        "APPELATION": l_appelation,
        "COULEUR": la_couleur,
        "STOCK": le_stock,
        "PRIX": le_prix,
    }
    return dict_cara


def carac_gout(lienbis):
    """Permet de récupérer les données concernant le goût c'est à dire
    la puissance, le fruité, la vivacité et l'épicée-boisé."""
    mesure = lienbis.find_elements(By.CSS_SELECTOR, ".measurement-bar [style]")
    caracte = [mesures.get_attribute("style") for mesures in mesure]
    le_fruite = caracte[0].replace("width: ", "").replace("%;", "")
    la_vivacite = caracte[1].replace("width: ", "").replace("%;", "")
    la_puissance = caracte[2].replace("width: ", "").replace("%;", "")
    epice_boise = caracte[3].replace("width: ", "").replace("%;", "")

    dict_gout = {
        "FRUITE": le_fruite,
        "VIVACITE": la_vivacite,
        "PUISSANCE": la_puissance,
        "EPICE_BOISE": epice_boise,
    }
    return dict_gout


def carac_tec(lienbis):
    """Permet de récupérer les données tels que la présence de sulfites, 
    le millésime, le carafage, cépage, le taux de sucre et le type d'agriculte."""
    donnees_techniques = lienbis.find_element(
        By.CLASS_NAME, "product-technical-data-ctn"
    )
    dtech = donnees_techniques.text.split("\n")
    dict_tr = {}
    for i in range(0, len(dtech)):
        if dtech[i] == "SULFITES":
            dict_tr.update({"SULFITES": dtech[i + 1]})
        if dtech[i] == "MILLÉSIME":
            dict_tr.update({"MILLESIME": dtech[i + 1]})
        if dtech[i] == "CARAFAGE":
            dict_tr.update({"CARAFAGE": dtech[i + 1]})
        if dtech[i] == "CÉPAGE":
            dict_tr.update(
                {"CEPAGE": dtech[i + 1 :]}
            )  # cépage est toujours le dernier élement des Données techniques
        if dtech[i] == "TAUX DE SUCRE":
            dict_tr.update({"TAUX_DE_SUCRE": dtech[i + 1]})
        if dtech[i] == "TYPE AGRICULTURE":
            dict_tr.update({"TYPE_AGRICULTURE": dtech[i + 1]})

    if "SULFITES" not in dict_tr:
        dict_tr.update({"SULFITES": np.nan})
    if "MILLESIME" not in dict_tr:
        dict_tr.update({"MILLESIME": np.nan})
    if "CARAFAGE" not in dict_tr:
        dict_tr.update({"CARAFAGE": np.nan})
    if "CEPAGE" not in dict_tr:
        dict_tr.update({"CEPAGE": np.nan})
    if "TAUX_DE_SUCRE" not in dict_tr:
        dict_tr.update({"TAUX_DE_SUCRE": np.nan})
    if "TYPE_AGRICULTURE" not in dict_tr:
        dict_tr.update({"TYPE_AGRICULTURE": np.nan})

    return dict_tr


def recup_caracs(links):
    """permet de réunir les dictionnaires généres par les fonctions carac, 
    carac_gout et carac_tech. Et crée un json avec ces données."""
    item_dic = []
    lienbis = webdriver.Chrome()
    for i in range(len(links) - 1):
        lienbis.get(links[i])
        dict_cara = carac(lienbis)
        dict_gout = carac_gout(lienbis)
        dict_tr = carac_tec(lienbis)

        ##Fusion de tous les dictionnaires
        dict_cara.update(dict_gout)
        dict_cara.update(dict_tr)
        dict_finale = dict_cara
        item_dic.append(dict_finale)
    with open("data_scrapping.json", "w") as fp:
        json.dump(item_dic, fp)


def recuperation_scrapping(url):
    """fonction qui permet d'effectuer le scrapping et le json 
    en appelant les fonctions recuperation_page et recup_caracs."""
    page = recuperation_page(url)
    recup_caracs(page)
