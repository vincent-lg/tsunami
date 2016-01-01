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
# ARE DISCLAIMED. IN NO Eguilde SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'guilde' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from secondaires.crafting.commandes.guilde.creer import PrmCreer
from secondaires.crafting.commandes.guilde.editer import PrmEditer
from secondaires.crafting.commandes.guilde.liste import PrmListe
from secondaires.crafting.commandes.guilde.membres import PrmMembres
from secondaires.crafting.commandes.guilde.promouvoir import PrmPromouvoir
from secondaires.crafting.commandes.guilde.quitter import PrmQuitter
from secondaires.crafting.commandes.guilde.rejoindre import PrmRejoindre

class CmdGuilde(Commande):

    """Commande 'guilde'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "guilde", "guild")
        self.nom_categorie = "batisseur"
        self.groupe = "administrateur"
        self.aide_courte = "manipulation des guildes"
        self.aide_longue = \
            "Cette commande permet de créer, éditer et supprimer " \
            "les guildes, ainsi que faire d'autres opérations, soit " \
            "pour avoir des informations sur un élément du crafting " \
            "(par exemple des informations sur certaines matières " \
            "premières), soit pour effectuer certaines actions."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmMembres())
        self.ajouter_parametre(PrmPromouvoir())
        self.ajouter_parametre(PrmQuitter())
        self.ajouter_parametre(PrmRejoindre())
