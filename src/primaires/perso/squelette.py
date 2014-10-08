# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant la classe Squelette, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents
from .membre import Membre
from .membre import Groupe

class Squelette(BaseObj):

    """Classe représentant un squelette.

    Un squelette est un ensemble de membres.
    Plusieurs personnages peuvent posséder un même squelette. Par exemple,
    deux PNJ humains auront tous deux le squelette d'un humain.
    Les membres, cependant, seront bel et bien distincts d'un personnage
    à un autre. Cela inclut donc que, si vous modifiez un squelette déjà
    utilisé, vous pouvez ajouter des membres ou en retirer, mais que vous
    pouvez difficilement modifier un membre (dire, après coup, que tel
    membre aura tel flag par exemple).

    En bref, si votre squelett'e est utilisé par une race, évitez de trop
    la modifier après coup. Les joueurs de cette race pourront avoir des
    membres différents avant et après la modification.

    """

    groupe = "squelettes"
    sous_rep = "squelettes"
    enregistrer = True
    def __init__(self, cle):
        """Constructeur du squelette"""
        BaseObj.__init__(self)
        self.cle = cle
        self.nom = "un squelette"
        self.description = Description(parent=self)
        self.__membres = []
        self.__groupes = {}

        # Liste des personnages dont l'équipement dérive de ce squelette
        self.personnages = []
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __getitem__(self, item):
        item = supprimer_accents(item).lower()
        return self.__membres[item]

    def __setitem__(self, item, valeur):
        raise TypeError("vous ne pouvez ajouter ainsi {} au squelette " \
                "{}. Utilisez la méthode ajouter_membre".format(item,
                self.cle))

    def __str__(self):
        return self.cle

    @property
    def membres(self):
        """Retourne une copie du dicitonnaire des membres"""
        return list(self.__membres)

    @property
    def groupes(self):
        """Retourne un dictionnaire déréférencé des groupes."""
        return dict(self.__groupes)

    @property
    def presentation_indentee(self):
        """Retourne une présentation indentée des membres"""
        membres = [membre.nom for membre in self.__membres]
        if not membres:
            membres = ["Aucun membre."]

        return "\n   " + "\n   ".join(membres)

    @property
    def probabilite_atteint(self):
        """Retourne la probabilité totale d'atteindre les membres du squelette."""
        return sum(membre.probabilite_atteint for membre in self.__membres)

    def ajouter_membre(self, nom, *args, **kwargs):
        """Construit le membre via son nom et l'ajoute au dictionnaire.

        Les paramètres *args et **kwargs sont transmis au constructeur de
        Membre.

        """
        if len(nom) < 3:
            raise ValueError("ce nom de membre est invalide.")

        membre = Membre(nom, *args, parent=self, **kwargs)
        self.__membres.append(membre)

        for personnage in self.personnages:
            personnage.equipement.ajouter_membre(membre)

        return membre

    def supprimer_membre(self, nom):
        """Supprime le membre du dictionnaire."""
        nom = supprimer_accents(nom).lower()
        noms = [(supprimer_accents(membre.nom).lower(), i) for i, membre in \
                enumerate(self.__membres)]
        noms = dict(noms)

        if nom not in noms.keys():
            raise KeyError("le membre {} n'existe pas dans ce " \
                    "squelette".format(nom))

        del self.__membres[noms[nom]]

        for personnage in self.personnages:
            personnage.equipement.supprimer_membre(nom)

    def get_membre(self, nom):
        """Retourne le membre si il le trouve grâce à son nom."""
        nom = supprimer_accents(nom).lower()
        noms = [(supprimer_accents(membre.nom).lower(), i) for i, membre in \
                enumerate(self.__membres)]
        noms = dict(noms)

        if nom not in noms.keys():
            raise KeyError("le membre {} n'existe pas dans ce " \
                    "squelette".format(nom))

        return self.__membres[noms[nom]]

    def a_membre(self, nom):
        """Retourne True si le squelette possède le membre nom, False sinon"""
        try:
            membre = self.get_membre(nom)
            res = True
        except KeyError:
            res = False

        return res

    def changer_flag_membre(self, nom, flags):
        """Change les flags du membre nom.
        Répercute ces modifications dans les autres membres dérivés.

        """
        membre = self.get_membre(nom)
        membre.flags = flags

        for personnage in self.personnages:
            equipement = personnage.equipement
            a_membre = equipement.get_membre(nom)
            a_membre.flags = flags

    def renommer_membre(self, nom, nouveau_nom, article=None):
        """Renomme le membre nom.

        Répercute ces modifications dans les autres membres dérivés.

        """
        membre = self.get_membre(nom)
        membre.nom = nouveau_nom
        if article:
            membre.article = article
        else:
            membre.recalculer_article()
            article = membre.article

        for personnage in self.personnages:
            equipement = personnage.equipement
            a_membre = equipement.get_membre(nom)
            a_membre.nom = nouveau_nom
            a_membre.article = article

    def remonter_membre(self, nom_membre):
        """Remonte un membre dans la liste des membres."""
        membre = self.get_membre(nom_membre)
        indice = self.__membres.index(membre)
        if indice != 0: # ne fait rien si le membre est déjà tout en haut
            membre = self.__membres.pop(indice)
            self.__membres.insert(indice - 1, membre)

            # On transmet aux équipement construits sur ce squelette
            for personnage in self.personnages:
                equipement = personnage.equipement
                equipement.remonter_membre(nom_membre)

    def descendre_membre(self, nom_membre):
        """Descend un membre dans la liste des membres."""
        membre = self.get_membre(nom_membre)
        indice = self.__membres.index(membre)
        if indice != len(self.__membres) - 1: # si le membre n'est pas en bas
            membre = self.__membres.pop(indice)
            self.__membres.insert(indice + 1, membre)

            # On transmet aux équipement construits sur ce squelette
            for personnage in self.personnages:
                equipement = personnage.equipement
                equipement.descendre_membre(nom_membre)

    def changer_probabilite_atteint_membre(self, nom, probabilite):
        """Change la probabilité d'être atteint en combat du membre nom.

        Répercute ces modifications dans les autres membres dérivés.

        """
        membre = self.get_membre(nom)
        membre.probabilite_atteint = probabilite

        for personnage in self.personnages:
            equipement = personnage.equipement
            a_membre = equipement.get_membre(nom)
            a_membre.probabilite_atteint = probabilite

    def get_groupe_membre(self, membre):
        """Retourne le groupe du membre si existe, sinon None.

        L'objet attendu est un membre, aps un nom de membre.

        """
        try:
            return self.groupes[membre.groupe]
        except KeyError:
            return None

    def changer_groupe_membre(self, nom_membre, nom_groupe):
        """Change le groupe du membre."""
        membre = self.get_membre(nom_membre)
        membre.groupe = nom_groupe
        if nom_groupe and self.get_groupe_membre(membre) is None:
            self.groupes[nom_groupe] = Groupe(nom_groupe)

        for personnage in self.personnages:
            equipement = personnage.equipement
            a_membre = equipement.get_membre(nom_membre)
            a_membre.groupe = nom_groupe

    def alterne_groupe_dissociable(self, nom_groupe):
        """Change le flag dissociable du groupe si existe."""
        if nom_groupe not in self.groupes:
            raise KeyError("le groupe {} n'existe pas.".format(nom_groupe))

        groupe = self.groupes[nom_groupe]
        groupe.dissociable = not groupe.dissociable
