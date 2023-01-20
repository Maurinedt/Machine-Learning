"""Description. 

Librairie qui détermine le meilleur modèle pour générer 
ensuite la base de données finale avec les prédictions sur le prix 
des vins. """

from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from rich.table import Table
from rich import print
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, ElasticNet, Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler

from .lib_modeles import (
    selection_variable,
    Elasticnet_model,
    knn_model,
    ridge_model,
    random_forest_model,
    gaussian_model,
    lasso_model,
    mlp_model,
)


def selection_model(data, cible):
    """selectionne le meilleur modèle"""
    liste_var, X, y = selection_variable(data, cible)
    X = X[liste_var]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y)
    modeles = [
        Elasticnet_model(X_tr, y_tr),
        knn_model(X_tr, y_tr),
        ridge_model(X_tr, y_tr),
        random_forest_model(X_tr, y_tr),
        gaussian_model(X_tr, y_tr),
        lasso_model(X_tr, y_tr),
        # mlp_model(X_tr, y_tr),  #Fait tourner le code pendant plus de 2heures.
    ]

    tableau = Table(
        "modèle",
        "score_train",
        "score_test",
        "moyenne cross validation",
        "dispersion cross validation",
        title="Synthèse des modèles",
    )
    scores_cv = []
    scores_test = []
    i = 0
    nom_modele = [
        "Elastic Net",
        "Regression KNN",
        "Ridge",
        "Random Forest",
        "Gaussian",
        "Lasso",
        "Reseau neuronal",
    ]
    for modele in modeles:
        scores = cross_val_score(modele, X_tr, y_tr, cv=4)
        tableau.add_row(
            nom_modele[i],
            str(modele.score(X_tr, y_tr)),
            str(modele.score(X_te, y_te)),
            str(scores.mean()),
            str(scores.std()),
        )
        scores_cv.append(scores.mean())
        scores_test.append(modele.score(X_te, y_te))
        i = i + 1
    temp = max(scores_cv)
    res = [i for i, j in enumerate(scores_cv) if j == temp]
    if temp > scores_test[int(res[0])]:
        type_fitt = "sur-apprentissage"
    else:
        type_fitt = "sous-apprentisage"
    return (
        print(
            f"Le meilleur modèle est {str(nom_modele[int(res[0])])} avec un score de {round(temp, 3)}"
        ),  # mais nous pouvons observer un {type_fitt}."),
        X_tr,
        X_te,
        y_tr,
        y_te,
        nom_modele[int(res[0])],
        modeles[int(res[0])],
        print(tableau),
    )


def graph_elastic_net(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre alpha qui varie pour le modèle elastic net"""
    train_scores, test_scores = list(), list()
    k = np.arange(0, 2 ** 50)
    for i in np.arange(1, 50):
        model = ElasticNet(alpha=2 ** i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_knn_regressor(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre nombre de voisins qui varie pour le modèle knn regressor"""
    train_scores, test_scores = list(), list()
    k = np.arange(1, 50)
    for i in np.arange(1, 50):
        model = KNeighborsRegressor(n_neighbors=i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_ridge(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre alpha qui varie pour le modèle Ridge"""
    train_scores, test_scores = list(), list()
    k = np.arange(1, 50)
    for i in np.arange(1, 50):
        model = Ridge(alpha=i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_random_forest(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre nombre d'estimateur qui varie pour le modèle random forest"""
    train_scores, test_scores = list(), list()
    k = np.arange(1, 100, 5)
    for i in np.arange(1, 100, 5):
        model = RandomForestRegressor(n_estimators=i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_gaussian(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre alpha qui varie pour le modèle gaussien"""
    train_scores, test_scores = list(), list()
    k = np.arange(0, 30)
    for i in np.arange(0, 30):
        model = GaussianProcessRegressor(alpha=i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_lasso(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre alpha qui varie pour le modèle Lasso"""
    train_scores, test_scores = list(), list()
    k = np.arange(0, 10, 0.1)
    for i in np.arange(0, 10, 0.1):
        model = Lasso(alpha=2 ** i)
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graph_reseau_neu(X_tr, y_tr, X_te, y_te):
    """Permet de générer les scores sur les données test et d'entrainement
    avec le paramètre alpha qui varie pour le modèle réseau neuronal"""
    train_scores, test_scores = list(), list()
    k = np.arange(0, 10, 0.1)
    for i in np.arange(0, 10, 0.1):
        model = Pipeline(
            [
                ("min_max_scaler", MinMaxScaler()),
                ("mlp", MLPRegressor(alpha=10.0 ** i)),
            ]
        )
        model.fit(X_tr, y_tr)
        train_acc = cross_val_score(model, X_tr, y_tr, cv=4)
        train_acc = train_acc.mean()
        train_scores.append(train_acc)
        test_acc = model.score(X_te, y_te)
        test_scores.append(test_acc)
    return train_scores, test_scores, k


def graphique_meilleur_modele(data, cible):
    """¨Fournit le graphique qui permet d'observer les scores
    du test et train"""
    liste_elem = selection_model(data, cible)
    X_tr, X_te, y_tr, y_te, meilleur_modele, modele = (
        liste_elem[1],
        liste_elem[2],
        liste_elem[3],
        liste_elem[4],
        liste_elem[5],
        liste_elem[6],
    )
    train_scores, test_scores = list(), list()
    if str(meilleur_modele) == "Elastic Net":
        train_scores, test_scores, k = graph_elastic_net(X_tr, y_tr, X_te, y_te)
    elif str(meilleur_modele) == "Regression KNN":
        train_scores, test_scores, k = graph_knn_regressor(X_tr, y_tr, X_te, y_te)
    elif str(meilleur_modele) == "Ridge":
        train_scores, test_scores, k = graph_ridge(X_tr, y_tr, X_te, y_te)
    elif str(meilleur_modele) == "Random Forest":
        train_scores, test_scores, k = graph_random_forest(X_tr, y_tr, X_te, y_te)
    elif str(meilleur_modele) == "Gaussian":
        train_scores, test_scores, k = graph_gaussian(X_tr, y_tr, X_te, y_te)
    elif str(meilleur_modele) == "Lasso":
        train_scores, test_scores, k = graph_lasso(X_tr, y_tr, X_te, y_te)
    else:
        train_scores, test_scores, k = graph_reseau_neu(X_tr, y_tr, X_te, y_te)
    plt.plot(k, train_scores, "-o", label="Train")
    plt.plot(k, test_scores, "-o", label="Test")
    plt.ylabel("Scores")
    plt.title(
        "Graphiques des scores train et test selon un paramètre du meilleur modèle."
    )
    plt.legend()
    plt.show()
    return modele


def prix(data):
    """Permet de calculer les prédictions de prix de chaque vins de notre BDD.
    Et permet également de calculer la différence de prix entre le prix réel et le 
    prix rationnel."""
    nb_gs = graphique_meilleur_modele(data, cible="PRIX")
    data = data.assign(Prix_ratio=np.nan)
    data = data.assign(diff_prix=np.nan)
    for i in range(len(data)):
        try:
            x = np.array(
                [
                    data["DEGREE"][i],
                    data["FRUITE"][i],
                    data["VIVACITE"][i],
                    data["PUISSANCE"][i],
                    data["EPICE_BOISE"][i],
                    data["MILLESIME"][i],
                ]
            ).reshape(1, 6)
            data["Prix_ratio"][i] = float(nb_gs.predict(x))
            data["diff_prix"][i] = float(data["PRIX"][i]) - data["Prix_ratio"][i]
        except KeyError:
            next
    data = data.to_json("data_avec_prix.json")
    return data
