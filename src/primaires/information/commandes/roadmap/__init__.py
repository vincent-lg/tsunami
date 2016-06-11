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


"""Package contenant la commande 'roadmap'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .editer import PrmEditer
from .supprimer import PrmSupprimer

class CmdRoadmap(Commande):

    """Commande 'roadmap'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "roadmap", "roadmap")
        self.nom_categorie = "info"
        self.aide_courte = "affiche la feuille de route"
        self.aide_longue = \
            "Cette commande permet d'afficher la feuille de route " \
            "actuelle. Cette feuille de route affiche les améliorations " \
            "sur lesquelles les immortels travaillent mais qui ne " \
            "sont pas encore visibles par les joueurs. Cette feuille " \
            "de route est mise à jour régulièrement et permet de " \
            "suivre l'avancement du travail accompli par les " \
            "bâtisseurs. Pour chaque élément de la feuille de route, " \
            "vous le verrez précédé d'un astérisque (*) coloré en " \
            "rouge pour vous indiquer que cette information a été " \
            "mise à jour depuis la dernière fois que vous avez " \
            "consulté cette feuille de route."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmSupprimer())

    def erreur_validation(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        roadmaps = importeur.information.roadmaps
        if roadmaps:
            msg = "Feuille de route :"
            for roadmap in roadmaps:
                msg += "\n"
                if personnage.est_immortel():
                    msg += " {:>2}".format(roadmap.no)
                elif personnage in roadmap.joueurs_ayant_lu:
                    msg += "   "
                else:
                    msg += " |rg|*|ff| "
                    roadmap.joueurs_ayant_lu.append(personnage)

                msg += " " + roadmap.titre.capitalize()
                if roadmap.texte:
                    msg += " : " + roadmap.texte
        else:
            msg = "|att|La feuille de route actuelle est vide.|ff|"

        return msg
