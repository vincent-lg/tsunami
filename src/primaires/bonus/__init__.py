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


"""Fichier contenant le module primaire bonus."""

from abstraits.module import *
from primaires.bonus.bonus import Bonus

class Module(BaseModule):

    """Classe utilisée pour gérer les bonus/malus temporaires.

    Ces bonus peuvent affecter un personnage, une salle ou un objet,
    voire d'autres informations. Ils sont conçus pour être organisés
    en dictionnaires à plusieurs niveaux, avoir un modificateur (un
    entier positif ou négatif) et une durée de vie. Les informations
    usuelles doivent tenir compte de ces modificateurs.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "bonus", "primaire")
        self.bonus = None

    def init(self):
        """Initialisation du module."""
        self.bonus = self.importeur.supenr.charger_unique(Bonus)
        if self.bonus is None:
            self.bonus = Bonus()

        BaseModule.init(self)

    def preparer(self):
        """Préparation du module."""
        self.nettoyer()

    def get(self, *args):
        """Récupère la valeur d'un bonus.

        Cette méthode a la même signature que Bonus.get (elle redirige
        dessus d'ailleurs).

        """
        return self.bonus.get(*args)

    def ajouter(self, informations, valeur, duree):
        """Ajoute un bonus/malus temporaire.

        Paramètres :
            informations : la liste des informations du bonus ;
            valeur : la valeur du bonus (un nombre entier ou flottant) ;
            duree : la durée de vie en secondes du bonus/malus.

        """
        self.bonus.ajouter(informations, valeur, duree)

    def nettoyer(self):
        """Nettoyage cyclique des bonus temporaires."""
        importeur.diffact.ajouter_action("bonus", 60, self.nettoyer)
        self.bonus.nettoyer()
