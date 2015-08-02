# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'créer' de la commande 'roadmap'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'roadmap créer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "créer", "create")
        self.groupe = "administrateur"
        self.schema = "<message>"
        self.aide_courte = "étend la feuille de route"
        self.aide_longue = \
            "Cette sous-commande permet de créer un nouvel élément " \
            "à ajouter à la feuille de route. Cet élément portera " \
            "le numéro actuellement disponible. Vous devez préciser " \
            "dans le texte le titre, un signe deux points et le " \
            "texte. Par exemple |ent|exploration : 150 salles " \
            "ouvrables|ff|. Si cette syntaxe n'est pas respectée, " \
            "l'annonce aura un titre sans texte, ce qui veut dire " \
            "que vous devrez répéter le texte complet à chaque modification."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        texte = dic_masques["message"].message
        try:
            roadmap = importeur.information.creer_roadmap(texte)
        except ValueError as err:
            personnage << "|err|" + str(err) + "|ff|"
            return

        personnage << "|att|L'élément de feuille de route {} a bien " \
                "été ajouté.|ff|".format(roadmap.no)
        importeur.communication.canaux["info"].envoyer_imp(
                "La feuille de route vient d'être mise à jour.")
