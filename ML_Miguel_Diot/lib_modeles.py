"""Description. 

Librairie qui permet de déterminer quelles variables ont un impact sur la variable cible.
Et stock les fonctions de chaque modèle utiliser dans la librairie `lib_appli_modele.py`"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, ElasticNet, Lasso, LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler


def selection_variable(data, cible: str):
    """Permet de selectionner les variables qui ont un impact sur la variable
    cible (ici le prix) via les variances."""
    data.dropna(axis=0, inplace=True)  # retire les données manquantes
    liste_col_str = []
    liste_var = data.columns.to_list()
    for i in range(len(liste_var)):  # regarde les colonnes qui sont str
        if (type(data[liste_var[i]][2])) == str or (
            type(data[liste_var[i]][2])
        ) == list:
            liste_col_str.append(liste_var[i])
    data = data.drop(liste_col_str, axis=1)  # enleve les colonne qui sont str
    X = data.drop([cible], axis=1)
    y = data[cible]
    selector = VarianceThreshold(threshold=1.0)
    selector.fit_transform(X)
    selector.get_support()
    return np.array(X.columns)[selector.get_support()], X, y


def linear_regression_model(X_tr, y_tr):
    """Modèle de régression linéaire"""
    lr = LinearRegression()
    lr.fit(X_tr, y_tr)
    return lr


def Elasticnet_model(X_tr, y_tr):
    """Modèle Elastic Net avec les hyperparamètres. """
    en_gs = GridSearchCV(
        ElasticNet(),
        {
            "alpha": [2 ** p for p in range(-3, 6)],
            "l1_ratio": (0.001, 0.01, 0.25, 0.5, 0.75, 1),
        },
    )
    en_gs.fit(X_tr, y_tr)
    return en_gs


def knn_model(X_tr, y_tr):
    """Modèle KNeighborsRegressor avec les hyperparamètres. """
    nb_gs = GridSearchCV(
        KNeighborsRegressor(),
        {"n_neighbors": np.arange(1, 50), "weights": ("uniform", "distance"),},
    )
    nb_gs.fit(X_tr, y_tr)
    return nb_gs


def svr_model(X_tr, y_tr):
    """Modèle SVR avec les hyperparamètres et pipeline. """
    p_svr = Pipeline([("standardscaler", MinMaxScaler()), ("svr", SVR()),])
    svr_gs = GridSearchCV(
        p_svr,
        {
            "svr__kernel": ("linear", "poly,", "rbf"),
            "svr__C": (0.01, 0.1, 0.5, 1.0, 10),
            "svr__epsilon": (0.01, 0.1, 1.0, 10),
        },
    )
    svr_gs.fit(X_tr, y_tr)
    return svr_gs


def mlp_model(X_tr, y_tr):
    """Modèle réseau neuronal avec les hyperparamètres et pipeline. """
    p_mlp = Pipeline([("min_max_scaler", MinMaxScaler()), ("mlp", MLPRegressor()),])
    mlp_gs = GridSearchCV(
        p_mlp,
        {
            "mlp__alpha": 10.0 ** -np.arange(1, 7),
            "mlp__hidden_layer_sizes": ((25,), (50,), (100,), (20, 20)),
            "mlp__solver": ("sgd", "adam"),  #'lbfgs',
            "mlp__max_iter": (25000, 50000),
        },
    )
    mlp_gs.fit(X_tr, y_tr)

    return mlp_gs


def lasso_model(X_tr, y_tr):
    """Modèle Lasso avec les hyperparamètres. """
    la_gs = GridSearchCV(
        Lasso(), {"alpha": [2 ** p for p in range(-9, 6)], "max_iter": (2000, 2500),},
    )
    la_gs.fit(X_tr, y_tr)
    return la_gs


def gaussian_model(X_tr, y_tr):
    """Modèle de régression gaussienne avec les hyperparamètres. """
    gp = GaussianProcessRegressor()
    gp_gs = GridSearchCV(
        gp,
        {
            "alpha": [1e-2, 1e-3],
            # "kernel": [RBF(l) for l in np.logspace(-1, 1, 2)],
            # "kernel": [DotProduct(sigma_0) for sigma_0 in np.logspace(-1, 1, 2)]
        },
    )
    gp_gs.fit(X_tr, y_tr)
    return gp_gs


def random_forest_model(X_tr, y_tr):
    """Modèle de régression de forêt aléatoire avec les hyperparamètres. """
    rfr = RandomForestRegressor()
    RandomForestRegressor_gs = GridSearchCV(
        rfr, {"n_estimators": np.arange(1, 100), "max_features": ("sqrt", "log2"),},
    )
    RandomForestRegressor_gs.fit(X_tr, y_tr)
    return RandomForestRegressor_gs


def ridge_model(X_tr, y_tr):
    """Modèle Ridge avec les hyperparamètres. """
    ridg = Ridge()
    rid_gss = GridSearchCV(ridg, {"alpha": np.arange(0, 30)},)
    rid_gss.fit(X_tr, y_tr)
    return rid_gss
