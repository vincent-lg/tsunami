# -*-coding:Utf-8 -*

"""Ce programme permet de scanner un paquet, un programme quelconque et
retourne le nombre de lignes de code, plus quelques statistiques.

On se base sur un chemin passé en premier paramètre.

"""

import os
import re
import sys
import getopt

# Constantes
RE_CLASSES = re.compile(r"^class [A-Za-z_][A-Za-z0-9_]*")

class Stats:
    
    """Classe conservant les statistiques globales ou d'un élément."""
    
    def __init__(self, nom):
        self.nom = nom
        self.lignes = 0
        self.lignes_code = 0
        self.lignes_commentaire = 0
        self.fichiers = 0
        self.classes = 0
    
    def copier(self, autre):
        self.lignes += autre.lignes
        self.lignes_code += autre.lignes_code
        self.lignes_commentaire += autre.lignes_commentaire
        self.fichiers += autre.fichiers
        self.classes += autre.classes

def scan_fichier(nom_fichier):
    stats = Stats(nom_fichier)
    stats.fichiers = 1
    fichier = open(nom_fichier, 'r', encoding = 'utf-8')
    lignes = fichier.readlines()[29:]
    commentaire = False
    for ligne in lignes:
        if RE_CLASSES.search(ligne):
            stats.classes += 1
        ligne = ligne.strip()
        if ligne:
            stats.lignes += 1
            if ligne.startswith("\"\"\""):
                commentaire = True
            if ligne.startswith("#") or commentaire:
                stats.lignes_commentaire += 1
            else:
                stats.lignes_code += 1
            if ligne.endswith("\"\"\""):
                commentaire = False
    print("  {0}: {1} lignes dont {2} de code et {3} de commentaire".format(nom_fichier, stats.lignes, stats.lignes_code, stats.lignes_commentaire))
    return stats

def scan_dossier(chemin):
    stats = Stats(chemin)
    for contenu in os.listdir(chemin):
        if os.path.isdir(chemin + os.sep + contenu):
            print("Scan du dossier {0}".format(contenu))
            stats.copier(scan_dossier(chemin + os.sep + contenu))
        elif os.path.isfile(chemin + os.sep + contenu) and contenu.endswith(".py"):
            stats.copier(scan_fichier(chemin + os.sep + contenu))
    return stats
            
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
if os.path.isfile(chemin):
    stats = scan_fichier(chemin)
else:
    stats = scan_dossier(chemin)

print("\n\n\n" + "-" * 80)
print("{0} fichier(s) scanné(s)".format(stats.fichiers))
print("{0} lignes dans le projet, dont {1} lignes de code et {2} de commentaires".format(stats.lignes, stats.lignes_code, stats.lignes_commentaire))
print("{} classes trouvées.".format(stats.classes))
print("Moyenne des lignes par fichier: {0}".format(stats.lignes // stats.fichiers))
print("Taux d'apparition des commentaires: {0}%".format(round(stats.lignes_commentaire / stats.lignes * 100), 3))

