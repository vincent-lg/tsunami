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


"""Fichier contenant la classe EdtPresentation, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript
from .edt_noms import EdtNoms
from .supprimer import NSupprimer

class EdtPresentation(Presentation):
    
    """Classe définissant l'éditeur d'objet 'oedit'.
    
    """
    
    def __init__(self, personnage, prototype, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, prototype)
        if personnage and prototype:
            self.construire(prototype)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, prototype):
        """Construction de l'éditeur"""
        # Noms
        noms = self.ajouter_choix("noms", "n", EdtNoms, prototype)
        noms.parent = self
        noms.apercu = "{objet.nom_singulier}"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                prototype)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de l'objet {}".format(prototype).ljust(
            76) + "|ff||\n" + self.opts.separateur
        
        # Extensions
        for extension in prototype._extensions_editeur:
            rac, ligne, editeur, objet, attr, sup = extension
            env = self.ajouter_choix(ligne, rac, editeur, objet, attr, *sup)
            env.parent = self
        
        # Prix
        prix = self.ajouter_choix("prix", "p", Uniligne, prototype, "prix")
        prix.parent = self
        prix.apercu = "{objet.prix}"
        prix.prompt = "Entrez un prix supérieur à 1 :"
        prix.aide_courte = \
            "Entrez la valeur de l'objet.\n\nValeur actuelle : {objet.prix}"
        
        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                prototype.script)
        scripts.parent = self
        
        # Suppression
        suppression = self.ajouter_choix("supprimer", "sup", NSupprimer, \
                prototype)
        suppression.parent = self
        suppression.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le prototype d'objet {} ?".format(prototype.cle)
        suppression.action = "objet.supprimer_prototype"
        suppression.confirme = "Le prototype d'objet {} a bien été " \
                "supprimé.".format(prototype.cle)
        
        # Travail sur les enveloppes
        # On appelle la méthode 'travailler_enveloppes' du prototype
        # Cette méthode peut travailler sur les enveloppes de la présentation
        # (écrire une aide courte, un aperçu...)
        enveloppes = {}
        for rac, nom in self.raccourcis.items():
            enveloppe = self.choix[nom]
            enveloppes[rac] = enveloppe
        
        prototype.travailler_enveloppes(enveloppes)
        
        if prototype.sans_prix:
            self.supprimer_choix("prix")
