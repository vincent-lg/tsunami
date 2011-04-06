# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant l'éditeur 'redit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_coords import EdtCoords
from .edt_zone import EdtZone
from .edt_mnemonic import EdtMnemonic
from .edt_sorties import EdtSorties

class EdtRedit(Presentation):
    
    """Classe définissant l'éditeur de salle 'redit'.
    
    """
    
    nom = "redit"
    
    def __init__(self, personnage, salle):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, salle)
        if personnage and salle:
            self.construire(salle)
    
    def __getinitargs__(self):
        return (None, None)
    
    def construire(self, salle):
        """Construction de l'éditeur"""
        # Coordonnées
        coords = self.ajouter_choix("coordonnées", "c", EdtCoords, salle)
        coords.parent = self
        coords.prompt = "Nouvelles coordonnées : "
        coords.apercu = "{objet.coords}"
        coords.aide_courte = \
            "Entrez les |ent|coordonnées|ff| de la salle ou |cmd|/|ff| pour " \
            "revenir à la fenêtre mère.\n" \
            "Les coordonnées permettent de repérer géographiquement une " \
            "salle dans\n" \
            "l'espace, selon les axes usuels |rgc|x|ff|, |vrc|y|ff| et " \
            "|blc|z|ff|.\n\n" \
            "Vous avez plusieurs possibilités d'édition :\n" \
            "- |cmd|INV|ff| : passe les coordonnées en invalide. Cela " \
            "signifie que la salle n'a\n" \
            "        plus aucun lien géographique avec les autres les " \
            "autres (elle peut\n" \
            "        naturellement avoir des sorties pointant vers d'autres " \
            "salles) ;\n" \
            "- |cmd|<x>.<y>.<z>|ff| : les trois coordonnées, négatives ou " \
            "positives, séparées\n" \
            "                par des points (par exemple, -1.2.0).\n" \
            "- |cmd|/h|ff| : déplace la salle vers le haut. De même, " \
            "|cmd|/s|ff|, |cmd|/so|ff|, |cmd|/o|ff|, |cmd|/no|ff|, " \
            "|cmd|/n|ff|, |cmd|/ne|ff|, |cmd|\n|ff|" \
            "       |cmd|/e|ff|, |cmd|/se|ff| et |cmd|/b|ff| déplacent la " \
            "salle dans n'importe quelle direction,\n" \
            "       si les coordonnées d'arrivée ne sont pas déjà " \
            "utilisées.\n\n" \
            "Coordonnées actuelles : |bc|{objet.coords}|ff|"
        """Entrez les |ent|coordonnées|ff| de la salle ou |cmd|/|ff| pour " \
            "revenir à la fenêtre mère.\n\n" \
            "Vous avez deux possibilités pour entrer les coordonnées " \
            "d'une salle :\n" \
            " |cmd|INV|ff| : passe les coordonnées en invalide. Cela " \
            "signifie que la salle\n" \
            "       n'a plus aucun lien géographique avec les autres " \
            "les autres (elle peut\n" \
            "       naturellement avoir des sorties pointant vers " \
            "d'autres salles) ;\n" \
            " |cmd|<x>.<y>.<z>|ff| : les trois coordonnées, négatives " \
            "ou positives, séparées\n               par des points.\n\n" \
            "Exemple : |cmd|0.0.0|ff|\n\n" \
            "Vous pouvez également utiliser des options pour déplacer " \
            "une salle. Par\n" \
            "exemple, |cmd|/h|ff| déplacera la salle vers le haut si aucune " \
            "salle n'a déjà ces\n" \
            "coordonnées dans l'univers.\n" \
            "Les alias sont |cmd|s|ff|, |cmd|se|ff|, |cmd|o|ff|, " \
            "|cmd|no|ff|, |cmd|n|ff|, |cmd|ne|ff|, |cmd|e|ff|, " \
            "|cmd|se|ff|, |cmd|b|ff| et |cmd|h|ff|.\n\n" \
            "Coordonnées actuelle : {objet.coords}"""

        # Zone
        zone = self.ajouter_choix("zone", "z", EdtZone, salle)
        zone.parent = self
        zone.prompt = "Nom de la zone : "
        zone.apercu = "{objet.zone}"
        zone.aide_courte = \
            "Entrez la |ent|zone|ff| de la salle ou |cmd|/|ff| pour revenir " \
            "à la fenêtre mère.\n" \
            "La nom de la zone peut comporter lettres non accentuées, " \
            "chiffres et\n" \
            "undescores (le signe |ent|_|ff|).\n" \
            "|att|Le couple 'zone:mnémonic' doit être unique et différent " \
            "pour chaque salle !|ff|\n\n" \
            "Zone actuelle : |bc|{objet.zone}|ff|"

        # Mnémonic
        mnemonic = self.ajouter_choix("mnemonic", "m", EdtMnemonic, salle)
        mnemonic.parent = self
        mnemonic.prompt = "Nom du mnémonic : "
        mnemonic.apercu = "{objet.mnemonic}"
        mnemonic.aide_courte = \
            "Entrez le |ent|mnémonic|ff| de la salle ou |cmd|/|ff| pour " \
            "revenir à la fenêtre mère.\n" \
            "Le mnémonic peut comporter lettres non accentuées, chiffres et\n" \
            "undescores (le signe |ent|_|ff|).\n" \
            "|att|Le couple 'zone:mnémonic' doit être unique et différent " \
            "pour chaque salle !|ff|\n\n" \
            "Mnémonic actuel : |bc|{objet.mnemonic}|ff|"
        
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, salle, "titre")
        titre.parent = self
        titre.prompt = "Titre de la salle : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| de la salle ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        # Titre
        description = self.ajouter_choix("description", "d", Description, \
                salle.description)
        description.parent = self
        description.apercu = "{objet.paragraphes_indentes}"
        description.aide_courte = \
            "Description de la salle {}".format(salle)
        
        # Sorties
        sorties = self.ajouter_choix("sorties", "s", EdtSorties, salle,
                "sorties")
        sorties.parent = self
        sorties.aide_courte = \
            "Entrez le |ent|nom d'une sortie|ff| pour l'éditer ou " \
            "|cmd|/|ff| pour revenir à la fenêtre parente."
