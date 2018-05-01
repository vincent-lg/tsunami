# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'mongo'"""

from pprint import pformat
import time

try:
    from bson.errors import InvalidDocument
    from bson.objectid import ObjectId
except ImportError:
    pass

from abstraits.obase import *
from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.commande.commande import Commande

## Constantes
AIDE = """
Cette commande permet d'interroger la base MongoDB, en admettant que
MongoDB soit utilisé comme méthode de stockage. En entrant cette commande
sans paramètre, la quantité d'objets est affichée dans chaque collection :
il existe une collection par classe héritée de BaseObj (la collection
porte le nom complet de la classe, incluant son chemin).

Il est possible de préciser en paramètre le nom complet de la classe
pour voir la liste des objets enregistrés dans la collection, sous la
forme d'un dictionnaire. Par exemple : %mongo%|ent| secondaires.stat.Stat|ff|.

Il est possible de préciser un ID utilisé par MongoDB pour avoir des
informations sur cet objet. L'ID est constitué de 24 caractères alpha-
numériques. Chaque ID correspond à un unique objet : dans la sauvegarde,
cet unique ID est utilisé pour faire correspondre les références entre
objets : si vous examinez une salle en particulier, par exemple, vous
verrez une référence à sa liste de personnages. Chaque personnage est
représenté par son ID. Le nom de la classe est indiqué pour simplifier la
lecture, mais il n'est pas nécessaire. Pour avoir des informations détaillées
sur un objet, entrez son ID. Par exemple : %mongo%|cmd| 12c48a1200d98f10|ff|.

Enfin, vous pouvez préciser un nombre pour voir les X dernières lignes de
la table d'enregistrement : la table d'enregistrement affiche tous les
objets enregistrés ainsi que le moment où ils sont enregistrés. Si vous
entrez par exemple %mongo%|cmd| 10|ff|, vous verrez les dix dernières
lignes d'enregistrement (les 10 derniers objets enregistrés), ainsi que
leur date d'enregistrement. La table d'enregistrement est perdue au
reboot.
""".strip("\n")

class CmdMongo(Commande):

    """Commande 'mongo'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "mongo", "mongo")
        self.nom_categorie = "info"
        self.groupe = "administrateur"
        self.schema = "(<texte_libre>)"
        self.aide_courte = "interroge MongoDB"
        self.aide_longue = AIDE

    def peut_executer(self, personnage):
        """Ne peut exécuter si le mode n'es tpas Mongo."""
        return importeur.supenr.mode == "mongo"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["texte_libre"]:
            texte = dic_masques["texte_libre"].texte

            if len(texte) < 3 and texte.isdigit():
                nb = int(texte)
                self.afficher_table(personnage, nb)
            elif texte in classes_base:
                self.afficher_collection(personnage, texte)
            elif texte.lower() in importeur.__dict__:
                self.afficher_module(personnage, texte.lower())
            elif len(texte) == 24:
                self.afficher_objet(personnage, texte.lower())
            else:
                personnage << "|err|Impossible de trouver l'information " \
                        "'{}'.|ff|".format(texte)
        else:
            self.afficher_resume(personnage)

    def afficher_table(self, personnage, nb):
        """Affiche la table des enregistrements."""
        mtn = time.time()
        if nb < 1 or nb > 100:
            personnage << "|err|Le nombre entré est invalide, " \
                    "trop grand ou trop petit.|ff|"
            return

        # Affichage du tableau
        tableau = Tableau("Table d'enregistrement")
        tableau.ajouter_colonne("Il y a")
        tableau.ajouter_colonne("Classe")
        tableau.ajouter_colonne("Objet")

        for temps, classe, _id in importeur.supenr.mongo_table[-nb:]:
            temps = round((mtn - temps), 3)
            temps = str(temps).replace(".", ",") + "s"
            tableau.ajouter_ligne(temps, classe, str(_id))

        personnage << tableau.afficher()

    def afficher_module(self, personnage, nom):
        """Affiche les classes du module indiqué."""
        mtn = time.time()
        classes = [classe for classe in importeur.supenr.mongo_objets if \
                classe.split(".")[1] == nom]
        classes.sort()
        if classes:
            tableau = Tableau("Collections du module {}".format(nom))
            tableau.ajouter_colonne("Collection")
            tableau.ajouter_colonne("Objets", DROITE)
            tableau.ajouter_colonne("Enregistrement")
            for classe in classes:
                objets = []
                o_classe = classes_base[classe]
                noms_classe = []
                for nom, cls in classes_base.items():
                    if issubclass(cls, o_classe):
                        noms_classe.append(nom)
                        objets.extend(list(importeur.supenr.mongo_objets.get(
                                nom, {}).values()))
                objets = len(objets)
                print(noms_classe)
                dernieres = [l for l in importeur.supenr.mongo_table if \
                        l[1] in noms_classe]
                if dernieres:
                    derniere = dernieres[-1]
                    temps = derniere[0]
                    temps = round((mtn - temps), 3)
                    temps = "{} secondes".format(str(temps).replace(".", ","))
                else:
                    temps = "inconnu"

                tableau.ajouter_ligne(classe, objets, temps)

            personnage << tableau.afficher()
        else:
            personnage << "Il n'y a aucun objet enregistré dans ce module."

    def afficher_collection(self, personnage, nom):
        """Affiche la collection indiquée."""
        tableau = Tableau("Détail de la collection {}".format(nom))
        tableau.ajouter_colonne("Collection")
        tableau.ajouter_colonne("Objet")
        tableau.ajouter_colonne("Champs", DROITE)
        objets = []
        noms_objet = []
        o_classe = classes_base[nom]
        for nom, cls in classes_base.items():
            if issubclass(cls, o_classe):
                for _id, objet in importeur.supenr.mongo_objets.get(
                        nom, {}).items():
                    if objet.e_existe:
                        noms_objet.append((nom, str(_id), len(
                                objet.__dict__)))

        noms_objet.sort()
        for nom, _id, attributs in noms_objet:
            tableau.ajouter_ligne(nom, _id, attributs)

        personnage << tableau.afficher()

    def afficher_objet(self, personnage, _id):
        """Affiche l'objet dont l'ID (str) est passée en argument."""
        mtn = time.time()
        _id = ObjectId(_id)
        objet = None
        for objets in importeur.supenr.mongo_objets.values():
            objet = objets.get(_id)
            if objet is not None:
                classe = importeur.supenr.qualname(type(objet))
                break

        if objet is None:
            personnage << "|err|L'objet d'ID {} ne peut être " \
                    "trouvé.|ff|".format(repr(_id))
            return

        attributs = importeur.supenr.mongo_db[classe].find_one(_id)

        # Affichage général
        msg = "Informations sur l'objet '{}' de type {} :".format(
                str(_id), classe)
        msg += "\n  Nombre d'attributs : {}".format(len(attributs))

        # Affichage des dernières lignes de modification
        lignes = [l for l in importeur.supenr.mongo_table if \
                str(l[2]) == str(_id)]
        if lignes:
            lignes = lignes[-5:]
            msg += "\n  Enregistrements récemts :"
            for temps, classe, _id in reversed(lignes):
                temps = round((mtn - temps), 3)
                temps = str(temps).replace(".", ",")
                msg += "\n    Il y a {} secondes".format(temps)
        else:
            msg += "\n  Cet objet n'a pas encore été enregistré."

        # Affichage des attributs
        lignes = pformat(attributs, 4, 70).split("\n")
        msg += "\n  Attributs :"
        for ligne in lignes:
            msg += "\n    " + ligne.replace("{", "{{").replace(
                    "}", "}}")
        personnage << msg

    def afficher_resume(self, personnage):
        """Affiche le résumé par groupe de module."""
        noms = list(importeur.__dict__.keys())
        noms.sort()
        tableau = Tableau("Collections par module")
        tableau.ajouter_colonne("Module")
        tableau.ajouter_colonne("Collections", DROITE)
        for nom in noms:
            classes = [classe for classe in importeur.supenr.mongo_objets if \
                    classe.split(".")[1] == nom]
            tableau.ajouter_ligne(nom, len(classes))

        personnage << tableau.afficher()
