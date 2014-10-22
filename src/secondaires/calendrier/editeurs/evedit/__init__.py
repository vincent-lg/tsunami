# -*-coding:Utf-8 -*

# Copyright (c) 2012 AYDIN Ali-Kémal
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
# pereIBILITY OF SUCH DAMAGE.


"""Package contenant l'éditeur 'evedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne

from .supprimer import NSupprimer
from .edt_date import EdtDate
from .edt_responsables import EdtResponsables


class EdtEvedit(Presentation):

    """Classe définissant l'éditeur d'évènement 'evedit'
    
    """
    
    nom = "evedit"
    
    def __init__(self, personnage, evenement):
        """Cinstructeur de l'éditeur"""
        self.personnage = personnage
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, evenement)
        
        if personnage and evenement:
            self.construire(evenement)
            
    def __getnewargs__(self):
        return (None, None)
            
    def construire(self, evenement):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, evenement,
                "titre")
        titre.parent = self
        titre.prompt = "Titre de l'évènement : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre de l'évènement|ff| ou |cmd|/|ff| " \
            "pour revenir à la fenêtre mère.\n\n" \
            "Titre actuelle : |tit|{objet.titre}|ff|\n"
        
        # Description
        description = self.ajouter_choix("description", "d", Description,
                        evenement)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de l'évènement : {}".format(
            evenement.id).ljust(76) + "|ff||\n" + self.opts.separateur
        
        # Date
        date = self.ajouter_choix("date", "a", EdtDate, evenement)
        date.parent = self
        date.prompt = "Date de l'évènement : "
        date.apercu = "{objet.str_date}"
        
        # Responsables
        responsable = self.ajouter_choix("responsables", "r",
                EdtResponsables, evenement)
        responsable.parent = self
        responsable.aide_courte = \
            "Entrez |cmd|/a <nom_responsable>|ff| pour ajouter un " \
            "responsable et\n|cmd|/s <nom_responsable>|ff| pour en " \
            "enlever un.\nUtilisez |cmd|/|ff| pour revenir à " \
            "la fenêtre parente."
        
        # Supprimer
        sup = self.ajouter_choix("supprimer", "sup", NSupprimer,
                evenement)
        sup.parent = self
        sup.aide_courte = "Souhaitez-vous réellement supprimer " \
                "l'évènement {} et ses informations ?".format(evenement.id)
