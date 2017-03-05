# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant la classe Bonus, détaillée plus bas."""

from datetime import datetime, timedelta

from abstraits.obase import BaseObj

class Bonus(BaseObj):

    """Classe représentant le dictionnaire de bonus/malus temporaires.

    Cette classe est organisée en dictionnaires à plusieurs niveaux.
    Le premier niveau représente l'information affectée (un personnage,
    une salle, un objet) avec, en valeur, une liste ou un dictionnaire.

    Si il s'agit d'une liste, elle contient des tuples (valeur,
    durée de vie). La durée de vie est une datetime.datetime. Si c'est
    un dictionnaire, les clés sont des chaînes et les valeurs d'autres
    listes ou d'autres dictionnaires.

    Par exemple :
        bonus = {
            personnage1: {
                "temperature": [
                    (20, datetime.now()),
                    (-30, datetime.now()),
                ],
            },
            ...
        }
    """

    enregistrer = True

    def __init__(self):
        BaseObj.__init__(self)
        self.bonus = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def get(self, *args, precision=0):
        """Retourne la liste de bonus actifs.

        Les paramètres sont les cases des modificateurs, dans l'ordre. Par exemple :
        >>> bonus = importeur.bonus.get(personnage1, "temperature")
        >>> # bonus est maintenant un entier/flottant (0 si aucun modificateur)

        """
        element = self.bonus
        bonus = 0
        for arg in args:
            element = element.get(arg, {})

        # element contient soit un dictionnaire vide, soit une liste
        if not element:
            element = []

        mtn = datetime.now()
        for modification, duree_de_vie in element:
            if not duree_de_vie or duree_de_vie >= mtn:
                bonus += modification

        if precision == None:
            return bonus
        elif precision == 0:
            return int(round(bonus))
        else:
            return round(bonus, precision)

    def ajouter(self, informations, valeur, duree):
        """Ajoute un bonus/malus temporaire ou permanent.

        Paramètres :
            informations : la liste des informations du bonus ;
            valeur : la valeur du bonus (un nombre entier ou flottant) ;
            duree : la durée de vie en secondes du bonus/malus 9[1]).

        Si la durée est 0, alors le bonus est permanent. Il n'est
        pas nécessaire de retenir plus d'un bonus/malus permanent
        par liste d'adresse, une seule valeur fluctuante sera modifiée.

        """
        if len(informations) < 2:
            raise ValueError("la liste des informations doit être au " \
                    "moins de longueur 2")

        if any(not isinstance(e, str) for e in informations[1:]):
            raise ValueError("l'une des informations après le premier " \
                    "indice n'est pas une chaîne, valeur invalide")

        dictionnaire = self.bonus
        for information in informations[:-1]:
            if information not in dictionnaire:
                dictionnaire[information] = {}

            dictionnaire = dictionnaire[information]

            # Dernière information, doit contenir une liste
        derniere = informations[-1]
        if derniere not in dictionnaire:
            dictionnaire[derniere] = []

        liste = dictionnaire[derniere]

        # Ajoute l'information dans la liste
        if duree != 0:
            mtn = datetime.now()
            delta = timedelta(seconds=duree)
            duree_de_vie = mtn + delta
            liste.append((valeur, duree_de_vie))
        else:
            # Fait la somme des bonus/malus permanents actuels
            permanent = sum(val for val, dur in liste if dur == 0)
            permanent += valeur
            liste[:] = [(v, d) for v, d in liste if d != 0]
            liste.append((permanent, 0))

    def nettoyer(self, dictionnaire=None):
        """Nettoie les mémoires expirées ou presque expirées."""
        dictionnaire = dictionnaire or self.bonus
        for cle, valeur in tuple(dictionnaire.items()):
            if isinstance(valeur, list):
                if valeur:
                    self.nettoyer_liste(valeur)
                else:
                    del dictionnaire[cle]
            elif isinstance(valeur, dict):
                if valeur:
                    self.nettoyer(valeur)
                else:
                    del dictionnaire[cle]

    def nettoyer_liste(self, liste):
        """Nettoyage de la liste passée en argument.

        Cette méthode ne devrait pas être appelée en dehors de la
        classe Bonus.

        """
        mtn = datetime.now()
        for valeur, duree in list(liste):
            if duree == 0:
                continue

            if mtn >= duree:
                liste.remove((valeur, duree))
            elif (mtn - duree).seconds < 60:
                secondes = (mtn - duree).seconds
                importeur.diffact.ajouter_action("u", secondes,
                        self.retirer_valeur, liste, valeur, duree)

    def retirer_valeur(self, liste, valeur, duree):
        """Retire la valeur de la liste.

        Cette méthode ne devrait pas être applée hors de la classe
        Bonus.

        """
        if (valeur, duree) in liste:
            liste.remove((valeur, duree))
