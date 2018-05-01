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


"""Package contenant l'éditeur 'nledit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_envoyer import EdtEnvoyer

class EdtNledit(Presentation):
    
    """Classe définissant l'éditeur de news letter 'nledit'."""
    
    nom = "nledit"
    def __init__(self, personnage, newsletter, attribut=None):
        """Constructeur de l'éditeur."""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, newsletter, attribut)
        if personnage and newsletter:
            self.construire(newsletter)
    
    def __getnewargs__(self):
        return (None, None)
    
    def accueil(self):
        """Message d'accueil du contexte."""
        msg = Presentation.accueil(self)
        lignes = msg.split("\n")
        lignes.insert(-2, " [-] Statut : " + self.objet.statut)
        return "\n".join(lignes)
    
    def construire(self, newsletter):
        """Construction de l'éditeur"""
        # Titre
        sujet = self.ajouter_choix("sujet", "s", Uniligne, newsletter, "sujet")
        sujet.parent = self
        sujet.prompt = "Nouveau sujet : "
        sujet.apercu = "{objet.sujet}"
        sujet.aide_courte = \
            "Entrez le |ent|sujet|ff| de la News Letter ou " \
            "|cmd|/|ff| pour revenir\n" \
            "à la fenêtre parente.\n" \
            "Sujet actuel : {objet.sujet}"
        
        # Contenu
        contenu = self.ajouter_choix("contenu", "c", Description,
                newsletter, "contenu")
        contenu.parent = self
        contenu.apercu = "{objet.contenu.paragraphes_indentes}"
        contenu.aide_courte = \
            "| |tit|" + "Contenu de la News Letter".ljust(76) + "|ff||\n" + \
            self.opts.separateur
        
        # Envoyer
        envoyer = self.ajouter_choix("envoyer", "env", EdtEnvoyer, newsletter)
        envoyer.parent = self
