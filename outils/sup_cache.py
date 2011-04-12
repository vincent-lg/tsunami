#!/usr/bin/python3.2
# -*-coding:Utf-8 -*

"""Ce programme permet de supprimer les fichiers caches du répertoire parent.
Son mode d'exécution est simple :
-   On prend comme point de départ le répertoire parent ".."
-   On parcourt toute l'arborescence
-   Dans chaque répertoire visité, on supprime le dossier "__pycache__"

"""

import os

def sup_cache(nom_rep):
    """Supprime le répertoire "nom_rep" si il existe"""
    rep = os.getcwd() + os.sep + nom_rep
    if os.path.isdir(rep):
        vider_dossier(rep)
        os.rmdir(rep)

def vider_dossier(rep):
    """Vide le dossier de tous ses fichiers.
    Le dossier ne doit aps contenir de répertoires.
    
    """
    liste_fichiers = os.listdir(rep)
    for nom_fichier in liste_fichiers:
        os.remove(rep + os.sep + nom_fichier)

def sup_cache_rec(nom_rep):
    """Appel récursivement sup_cache"""
    print("On supprime", os.getcwd())
    sup_cache(nom_rep)
    noms_fichiers = os.listdir(os.getcwd())
    rep_courant = os.getcwd()
    for nom_fichier in noms_fichiers:
        rep = rep_courant + os.sep + nom_fichier
        if os.path.isdir(rep):
            os.chdir(rep)
            sup_cache_rec(nom_rep)

nom_rep = "__pycache__"
os.chdir("..")
sup_cache_rec(nom_rep)
