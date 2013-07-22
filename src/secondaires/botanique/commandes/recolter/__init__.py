# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'récolter'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdRecolter(Commande):

    """Commande 'récolter'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "récolter", "harvest")
        self.schema = "(<nombre>) <element_recoltable> depuis/from <vegetal>"
        self.aide_courte = "récolte un végétal"
        self.aide_longue = \
                "Cette commande permet de récolter un végétal dans la " \
                "salle où vous vous trouvez. Vous devez préciser " \
                "le nom de l'élément à récolter (|ent|feuilles|ff|, " \
                "|ent|fruits|ff|, |ent|racines|ff|...) précédé " \
                "optionnellement du nombre à récolter. Vous devez " \
                "indiquer après le mot-clé le nom du végétal à récolter " \
                "en fonction de ceux se trouvant dans la salle. Notez " \
                "que vous pouvez utiliser la notation |ent|X.nom|ff| " \
                "(par exemple |ent|2.pommier|ff| pour récolter le second " \
                "pommier présent dans la salle)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        elt = self.noeud.get_masque("element_recoltable")
        elt.proprietes["vegetal"] = \
                "dic_masques['vegetal'].vegetal"
        vegetal = self.noeud.get_masque("vegetal")
        vegetal.prioritaire = True

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre

        element = dic_masques["element_recoltable"].element
        vegetal = dic_masques["vegetal"].vegetal
        qtt = vegetal.elements.get(element.objet, 0)
        if qtt == 0:
            personnage << "|err|Cet élément récoltable est épuisé.|ff|"
            return

        if qtt < nombre:
            nombre = qtt

        objet = element.objet
        pris = 0
        for i in range(nombre):
            t_o = importeur.objet.creer_objet(objet)
            personnage.ramasser_ou_poser(t_o)

        if pris == 0:
            personnage << "|err|Vous n'avez aucune main de libre.|ff|"
            return

        vegetal.recolter(objet, pris)
        personnage << "Vous récoltez {} depuis {}.".format(
                objet.get_nom(pris), vegetal.nom)
        personnage.salle.envoyer("{{}} récolte {} depuis {}.".format(
                objet.get_nom(pris), vegetal.nom), personnage)
