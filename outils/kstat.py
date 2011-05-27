# -*-coding:Utf-8 -*

"""Ce programme permet de scanner un paquet, un programme quelconque et
retourne le nombre de lignes de code, plus quelques statistiques.

On se base sur un chemin passé en premier paramètre.

"""

import os
import sys
import getopt

def scan_fichier(nom_fichier):
    nb_lignes = 0
    nb_lignes_code = 0
    nb_lignes_commentaire = 0
    fichier = open(nom_fichier, 'r', encoding = 'utf-8')
    commentaire = False
    for ligne in fichier:
        ligne = ligne.strip()
        if ligne:
            nb_lignes += 1
            if ligne.startswith("\"\"\""):
                commentaire = True
            if ligne.startswith("#") or commentaire:
                nb_lignes_commentaire += 1
            else:
                nb_lignes_code += 1
            if ligne.endswith("\"\"\""):
                commentaire = False
    print("  {0}: {1} lignes dont {2} de code et {3} de commentaire".format(nom_fichier, nb_lignes, nb_lignes_code, nb_lignes_commentaire))
    return nb_lignes, nb_lignes_code, nb_lignes_commentaire

def scan_dossier(chemin):
    nb_fichiers = 0
    nb_lignes = 0
    nb_lignes_code = 0
    nb_lignes_commentaire = 0
    for contenu in os.listdir(chemin):
        if os.path.isdir(chemin + os.sep + contenu):
            print("Scan du dossier {0}".format(contenu))
            t_fichiers, t_lignes, t_lignes_code, t_lignes_commentaire = \
                scan_dossier(chemin + os.sep + contenu)
            nb_fichiers += t_fichiers
            nb_lignes += t_lignes
            nb_lignes_code += t_lignes_code
            nb_lignes_commentaire += t_lignes_commentaire
        elif os.path.isfile(chemin + os.sep + contenu) and contenu.endswith(".py"):
            t_lignes, t_lignes_code, t_lignes_commentaire = scan_fichier( \
                chemin + os.sep + contenu)
            nb_fichiers += 1
            nb_lignes += t_lignes
            nb_lignes_code += t_lignes_code
            nb_lignes_commentaire += t_lignes_commentaire
    return nb_fichiers, nb_lignes, nb_lignes_code, nb_lignes_commentaire
            
# On extrait le premier paramètre de la ligne de commande si il existe
if len(sys.argv) == 1:
    print("Usage: {0} chemin_du_dossier".format(sys.argv[0]))
    sys.exit(1)

chemin = sys.argv[1]

# Vérification du chemin
if not os.path.exists(chemin):
    print("Le chemin précisé n'existe pas ({0})".format(chemin))
    sys.exit(1)

# Initialisation des variables contenant les informations statistiques
lignes = 0
lignes_code = 0
lignes_commentaire = 0
fichiers = 0

if os.path.isfile(chemin):
    fichiers = 1
    lignes, lignes_code, lignes_commentaire = scan_fichier(chemin)
else:
    fichiers, lignes, lignes_code, lignes_commentaire = scan_dossier(chemin)

print("\n\n\n" + "-" * 80)
print("{0} fichier(s) scanné(s)".format(fichiers))
print("{0} lignes dans le projet, dont {1} lignes de code et {2} de commentaires".format(lignes, lignes_code, lignes_commentaire))
print("Moyenne des lignes par fichier: {0}".format(lignes // fichiers))
print("Taux d'apparition des commentaires: {0}%".format(lignes_commentaire / lignes * 100))
