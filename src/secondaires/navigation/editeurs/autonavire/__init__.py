# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Package contenant l'éditeur 'anedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.choix_objet import ChoixObjet
from primaires.interpreteur.editeur.tableau import Tableau
from secondaires.navigation.equipage.postes.hierarchie import ORDRE

class EdtNaedit(Presentation):

    """Classe définissant l'éditeur de modèle de navire automatique."""

    nom = "naedit"

    def __init__(self, personnage, fiche):
        """Constructeur de l'éditeur."""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, fiche)
        if personnage and fiche:
            self.construire(fiche)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, fiche):
        """Construction de l'éditeur"""
        # Modèle
        modele = self.ajouter_choix("modèle de navire", "m", ChoixObjet,
                fiche, "modele", importeur.navigation.modeles)
        modele.parent = self
        modele.prompt = "Clé du modèle de navire : "
        modele.apercu = "{objet.modele}"
        modele.aide_courte = \
            "Entrez la |ent|clé|ff| du modèle de navire ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nModèle actuel : {objet}"

        # Équipage
        matelots = list(importeur.navigation.fiches.keys())
        mnemo_coords = {}
        coords_court = {}
        if fiche.modele:
            for coords, salle in fiche.modele.salles.items():
                mnemo_coords[salle.mnemonic] = coords
                coords_court[coords] = salle.titre_court

        equipage = self.ajouter_choix("équipage", "u", Tableau,
                fiche, "equipage",
                (("poste", ORDRE), ("matelot", matelots),
                ("salle", mnemo_coords), ("min", "entier"),
                ("max", "entier")), {2: coords_court})
        equipage.parent = self
        equipage.apercu = "{taille}"
        equipage.aide_courte = \
            "Vous pouvez configurer ici le tableau de l'équipage " \
            "du navire\nautomatique à créer. Ce tableau comprend " \
            "5 colonnes :\n-   Le nom du poste (capitaine, second, " \
            "maître d'équipage...)\n-   La clé de la fiche de " \
            "mâtelot correspondant au prototype de PNJ\n-   La salle " \
            "où faire apparaître le membre d'équipage\n-   Le nombre " \
            "minimum de mâtelots de ce type à créer\n-   Le nombre " \
            "maximum de mâtelots de ce type à créer\n\nVous pouvez " \
            "ajouter une ligne dans le tableau en entrant :\n" \
            "    |ent|<poste> / <fiche> / <mnémonique> / <min> / " \
            "<max>|ff|\n\nPar exemple :\n    |cmd|rameur / " \
            "pirate_couchant / 1 / 3 / 5|ff|\nPour créer entre 3 et " \
            "5 rameurs modelés sur le prototype de PNJ\n'pirate_couchant', " \
            "devant apparaître en salle de ménmonique '1'\n(probablement " \
            "le pont central).\n\nPour supprimer une information, " \
            "entrez :\n |cmd|/s <nom du poste|ff|\n\nÉquipage " \
            "actuel :\n{valeur}"

        # Pavillon
        pavillon = self.ajouter_choix("pavillon", "p", ChoixObjet,
                fiche, "pavillon", importeur.objet.prototypes)
        pavillon.parent = self
        pavillon.prompt = "Clé du pavillon : "
        pavillon.apercu = "{objet.pavillon}"
        pavillon.aide_courte = \
            "Entrez la |ent|clé|ff| du prototype de pavillon ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nPavillon actuel : {objet}"
