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


"""Fichier contenant la classe CommandeDynamique détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.interpreteur.commande.commande import Commande

class CommandeDynamique(BaseObj):

    """Classe décrivant les commandes dynamiques.

    Une commande dynamique est une commande de l'univers, mais
    au lieu d'être définie statiquement (comme le sont la plupart
    des commandes usuelles, regarder/look, prendre/get, manger/eat...),
    elles peuvent être manipulées par des éditeurs et ajoutées ou
    retirées par des immortels.

    Ces commandes doivent être, pour le joueur les utilisant, aussi proche
    des commandes statiques que possible.

    L'ajout d'une commande dynamique permet l'ajout d'un nouvel
    évènement dans les objets scriptables qui sera appelé pour interragir
    avec l'élément observé désigné par le joueur. Par exemple, si
    le joueur entre :
        push mur
    Que la commande pousser/push est une commande dynamique et que 'mur'
    est un détail visible dans la salle du joueur, l'évènement
    'pousser' de ce détail sera appelé avec certains paramètres.

    """

    enregistrer = True

    def __init__(self, nom_francais, nom_anglais):
        """Constructeur d'une commande dynamique."""
        BaseObj.__init__(self)
        self.nom_francais = nom_francais
        self.nom_anglais = nom_anglais
        self.commande = None # commande statique liée
        self._nom_categorie = "divers"
        self._aide_courte = "à renseigner..."
        self.aide_longue = Description(parent=self, scriptable=False,
                callback="maj")
        self.aide_courte_evt = "Un personnage fait quelque chose"
        self.aide_longue_evt = Description(parent=self, scriptable=False)
        self.latence = 0
        self.message_erreur = "Vous ne pouvez faire cela."
        self.message_attente = ""
        self._construire()

    def __getnewargs__(self):
        return ("", "")

    def __repr__(self):
        return "<Commande dynamique '{}/{}'>".format(
                self.nom_francais, self.nom_anglais)

    def __str__(self):
        return self.nom_francais + "/" + self.nom_anglais

    def __getstate__(self):
        dico_attr = self.__dict__.copy()
        if "commande" in dico_attr:
            del dico_attr["commande"]

        return dico_attr

    def _get_aide_courte(self):
        return self._aide_courte
    def _set_aide_courte(self, aide):
        if len(aide) > 70:
            aide = aide[:70]
        self._aide_courte = aide
        self.maj()
    aide_courte = property(_get_aide_courte, _set_aide_courte)

    def _get_nom_categorie(self):
        return self._nom_categorie
    def _set_nom_categorie(self, categorie):
        self._nom_categorie = nom_categorie
        self.maj()
    nom_categorie = property(_get_nom_categorie, _set_nom_categorie)

    def ajouter(self):
        """Ajoute la commande dans l'interpréteur.

        Il est préférable de faire cela après l'insertion des commandes
        statiques dans l'interpréteur, c'est-à-dire durant la phase de
        préparation du module.

        """
        commande = Commande(self.nom_francais, self.nom_anglais)
        commande.nom_categorie = self.nom_categorie
        commande.aide_courte = self.aide_courte
        commande.aide_longue = str(self.aide_longue)
        commande.schema = "<element_observable>"
        commande.interpreter = self.interpreter
        importeur.interpreteur.ajouter_commande(commande)
        self.commande = commande
        return commande

    def interpreter(self, personnage, dic_masques):
        """Méthode outre-passant l'interprétation de la commande statique.

        Quand la commande statique ajoutée est exécutée, c'est cette
        méthode qui est appelée (voir la méthode ajouter pour voir le
        cheminement). Les paramètres de cette méthode sont les mêmes
        que Commande.interpreter, à ceci près que le self est la commande
        dynamique, pas la commande statique qui se trouve derrière.

        """
        element = dic_masques["element_observable"].element
        if not hasattr(element, "script"):
            personnage << self.message_erreur
            return

        script = element.script
        try:
            evt = script[self.nom_francais]
        except KeyError:
            personnage << self.message_erreur
        else:
            script[self.nom_francais].executer(personnage=personnage, element=element)

    def maj(self):
        """Mise à jour de la commande dynamique."""
        print("Mise à jour.")
        if self.commande:
            self.commande.nom_categorie = self.nom_categorie
            self.commande.aide_courte = self._aide_courte
            self.commande.aide_longue = str(self.aide_longue)

