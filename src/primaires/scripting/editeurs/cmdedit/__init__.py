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


"""Package contenant l'éditeur 'cmdedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.description import Description
from .edt_messages import EdtMessages

class EdtCmdedit(Presentation):
    
    """Classe définissant l'éditeur de commande 'cmdedit'.
    
    """
    
    nom = "cmdedit"
    
    def __init__(self, personnage, commande):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, commande)
        if personnage and commande:
            self.construire(commande)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, commande):
        """Construction de l'éditeur"""
        commande = self.objet
        
        # Aide courte
        synopsys = self.ajouter_choix("synopsys", "s", Uniligne, commande,
                "aide_courte")
        synopsys.parent = self
        synopsys.prompt = "Synopsys de la commande : "
        synopsys.apercu = "{objet.aide_courte}"
        synopsys.aide_courte = \
            "Entrez le |ent|synopsys|ff| de la commande ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Synopsys actuel : |bc|{objet.aide_courte}|ff|"
        
        # Aide longue
        aide_longue = self.ajouter_choix("aide longue", "g", Description, \
                commande, "aide_longue")
        aide_longue.parent = self
        aide_longue.apercu = "{objet.aide_longue.paragraphes_indentes}"
        aide_longue.aide_courte = \
            "| |tit|" + "Aide longue de la commande {}".format(
            commande).ljust(76) + "|ff||\n" + self.opts.separateur
        
        # Aide courte evt
        aide_courte = self.ajouter_choix("aide de l'évènement", "a", Uniligne,
                commande, "aide_courte_evt")
        aide_courte.parent = self
        aide_courte.prompt = "Aide courte de l'vènement : "
        aide_courte.apercu = "{objet.aide_courte_evt}"
        aide_courte.aide_courte = \
            "Entrez l'|ent|aide courte|ff| de l'évènement ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Aide courte actuelle : |bc|{objet.aide_courte_evt}|ff|"
        
        # Aide longue evt
        aide_longue_evt = self.ajouter_choix("aide longue de l'évènement",
                "u", Description, commande, "aide_longue_evt")
        aide_longue_evt.parent = self
        aide_longue_evt.apercu = "{objet.aide_longue_evt.paragraphes_indentes}"
        aide_longue_evt.aide_courte = \
            "| |tit|" + "Aide longue de l'évènement de la commande {}".format(
                    commande).ljust(76) + "|ff||\n" + self.opts.separateur
        
        # Latence
        latence = self.ajouter_choix("latence", "l", Entier, commande,
                "latence")
        latence.parent = self
        latence.apercu = "{objet.latence}"
        latence.prompt = "Latence de la commande : "
        latence.aide_courte = \
            "Entrez la |ent|latence|ff| de la commande ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "La latence est un nombre de secondes avant que la " \
            "commande n'exécute\n" \
            "le script concerné. Certaines commandes doivent " \
            "s'exécuter instantanément\n" \
            "(ont une latence de |ent|0|ff| dans ce cas).\n\n" \
            "Si la commande a une latence non nulle, le message " \
            "d'attente est envoyé.\n" \
            "Ce message est configurable dans l'éditeur. " \
            "Notez que si la latence est\n" \
            "nulle, ce message n'est de toute façon pas envoyé.\n\n" \
            "Latence actuelle : {objet.latence}"

        
        # Messages
        messages = self.ajouter_choix("messages", "m", EdtMessages, commande)
        messages.parent = self

