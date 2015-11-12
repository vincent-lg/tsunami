# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant la classe Partie, détaillée plus bas."""

from abstraits.obase import BaseObj

class Partie(BaseObj):

    """Classe représentant une partie.

    Une partie est un état figé d'un jeu.

    """

    enregistrer = True
    
    def __init__(self, objet, jeu, plateau):
        """Constructeur de la partie."""
        BaseObj.__init__(self)
        self.objet = objet
        self.jeu = jeu
        self.plateau = plateau
        self.__joueurs = []
        self.observateurs = []
        self.tour = None
        self.sens = 1
        self.en_cours = False
        self.nb_tours = 0
        self.finie = False

    def __getnewargs__(self):
        return (None, None, None)

    @property
    def personnage(self):
        """Retourne le premier joueur."""
        return self.__joueurs[0]

    @property
    def joueurs(self):
        """Retourne une liste déréférencée des joueurs."""
        return list(self.__joueurs)

    def ajouter_joueur(self, personnage):
        """Ajoute le personnage comme joueur."""
        if self.jeu.nb_joueurs_max > len(self.__joueurs):
            self.__joueurs.append(personnage)
            if self.tour is None:
                self.tour = personnage

            return True

        return False

    def retirer_joueur(self, personnage):
        """Retire le joueur de la partie."""
        if "jeu" in personnage.etats:
            personnage.etats.retirer("jeu")
        if personnage in self.__joueurs:
            self.__joueurs.remove(personnage)

            if self.tour is personnage:
                self.changer_tour()

    def changer_tour(self):
        """Change de tour."""
        try:
            i = self.joueurs.index(self.tour)
        except ValueError:
            i = 0

        if self.sens > 0:
            i += 1
        else:
            i -= 1
        if self.__joueurs:
            i = i % len(self.__joueurs)

        if self.__joueurs:
            self.tour = self.__joueurs[i]
        else:
            self.tour = None

        if i == 0:
            self.nb_tours += 1

    def afficher(self, personnage):
        return self.plateau.afficher(personnage, self.jeu, self)

    def afficher_tous(self):
        """Affiche la partie à tous les participants."""
        for p in self.__joueurs:
            p << self.afficher(p, self.jeu, self)

    def envoyer(self, message, *joueurs, **kw_joueurs):
        """Envoie le message à tous les joueurs de la partie.

        Sauf ceux dans joueurs et kw_joueurs qui sont les exceptions.

        """
        for joueur in self.joueurs + self.observateurs:
            if joueur not in joueurs and joueur not in kw_joueurs.values():
                joueur.envoyer(message, *joueurs, **kw_joueurs)

    def terminer(self):
        """Termine la partie."""
        self.finie = True
        self.envoyer("La partie est finie !")

    def detruire(self):
        """Destruction de la partie."""
        self.objet.partie = None
        BaseObj.detruire(self)
