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


"""Fichier contenant le paramètre 'éditer' de la commande 'roadmap'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):

    """Commande 'roadmap éditer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "éditer", "edit")
        self.groupe = "administrateur"
        self.schema = "<nombre> <message>"
        self.aide_courte = "édite la feuille de route"
        self.aide_longue = \
            "Cette sous-commande permet d'éditer la feuille de " \
            "route. Elle prend en premier paramètre le numéro de " \
            "l'élément à éditer tel que vous pouvez le voir en " \
            "entrant %roadmap% sans argument. Après ce numéro, " \
            "entrez le texte par lequel vous voulez remplacer cet " \
            "élément. Notez que si cet élément de la feuille de " \
            "route contient un titre (c'est le cas si un signe " \
            "deux points a pu être trouvé lors de l'ajout), cette " \
            "commande ne modifie pas le titre, seulement le texte. " \
            "Par exemple, entrez %roadmap% %roadmap:créer%|cmd| " \
            "exploration : 200 salles ouvrables|ff| pour créer " \
            "l'élément de la feuille de route. Étant donné qu'un " \
            "signe deux points peut être trouvé dans le texte à " \
            "la création, le titre de la feuille de route sera " \
            "\"exploration\" tandis que son texte sera \"200 salles " \
            "ouvrables\". Il vous suffit donc d'écrire %roadmap% " \
            "%roadmap:éditer%|cmd| 1 300 salles ouvrables|ff| pour " \
            "changer le texte de l'élément de la feuille de route. " \
            "Cet élément deviendra donc \"Exploration : 300 salles " \
            "ouvrables\"."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        id = dic_masques["nombre"].nombre
        modif = dic_masques["message"].message
        roadmaps = importeur.information.roadmaps

        if id > len(roadmaps):
            personnage << "|err|Aucun élément ne correspond à l'ID " \
                    "spécifiée.|ff|"
        else:
            id -= 1
            roadmap = roadmaps[id]
            roadmap.mettre_a_jour(modif)
            personnage << "|att|L'élément de feuille de route {} a " \
                    "bien été modifié.|ff|".format(roadmap.no)
            importeur.communication.canaux["info"].envoyer_imp(
                    "La feuille de route vient d'être mise à jour.")
