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


"""Ce fichier contient l'éditeur EdtChambre, détaillé plus bas."""

from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection_objet import SelectionObjet
from primaires.interpreteur.editeur.uniligne import Uniligne

class EdtChambre(Presentation):

    """Ce contexte permet d'éditer une chambre d'auberge."""

    def __init__(self, pere, chambre=None, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, pere, chambre, attribut, False)
        if pere and chambre:
            self.construire(chambre)

    def construire(self, chambre):
        """Construction de l'éditeur"""
        # Numéro
        numero = self.ajouter_choix("numéro", "n", Uniligne, chambre, "numero")
        numero.parent = self
        numero.prompt = "Numéro de la chambre : "
        numero.apercu = "{objet.numero}"
        numero.aide_courte = \
            "Entrez le |ent|numéro|ff| de la chambre ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nNuméro actuel : " \
            "|bc|{objet.numero}|ff|"

        # Prix par jour
        prix = self.ajouter_choix("prix par jour", "p", Entier, chambre,
                "prix_par_jour", 1)
        prix.parent = self
        prix.apercu = "{objet.prix_par_jour}"
        prix.prompt = "Entrez un prix supérieur à 1 :"
        prix.aide_courte = \
            "Entrez le |ent|prix|ff| par jour de la location de la " \
            "chambre.\n\nPrix par jour actuel : {objet.prix_par_jour}"

        # Dependances
        deps = self.ajouter_choix("dépendances", "d", SelectionObjet,
                chambre, "dependances", importeur.salle.salles)
        deps.parent = self
        deps.prompt = "Identifiant de la salle à ajouter ou supprimer : "
        deps.apercu = "{valeur}"
        deps.aide_courte = \
            "Entrez l'|ent|identifiant|ff| d'une dépendance pour l'ajouter " \
            "ou la supprimer.\n\nDépendances actuelles : {valeur}"

