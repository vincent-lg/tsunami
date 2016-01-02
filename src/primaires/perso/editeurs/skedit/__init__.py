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


"""Package contenant l'éditeur 'skedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.supprimer import Supprimer
from .edt_membres import EdtMembres

class EdtSkedit(Presentation):
    
    """Classe définissant l'éditeur de squelette 'skedit'.
    
    """
    
    nom = "skedit"
    
    def __init__(self, personnage, squelette):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, squelette)
        if personnage and squelette:
            self.construire(squelette)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, squelette):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, squelette, "nom")
        nom.parent = self
        nom.prompt = "Nom du squelette : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du squelette ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nNom actuel : |bc|{objet.nom}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                squelette)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du squelette {}".format(
            squelette.cle).ljust(75) + \
            "|ff||\n" + self.opts.separateur
        
        # Membres
        membres = self.ajouter_choix("membres", "m", EdtMembres, squelette)
        membres.parent = self
        membres.apercu = "{objet.presentation_indentee}"
        membres.aide_courte = \
            "Entrez le |ent|nom d'un membre|ff| pour le créer ou l'éditer, " \
            "ou |cmd|/|ff| pour revenir à\n" \
            "la fenêtre parente.\n" \
            "Option :\n" \
            " - |ent|/d <membre>|ff| : supprime le membre indiqué\n\n"
        
        # Suppression
        suppression = self.ajouter_choix("supprimer", "sup", Supprimer, \
                squelette)
        suppression.parent = self
        suppression.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le squelette {} ?".format(squelette.cle)
        suppression.action = "perso.supprimer_squelette"
        suppression.confirme = "Le squelette {} a bien été supprimé.".format(
                squelette.cle)
