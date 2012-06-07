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


"""Package contenant l'éditeur 'shedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_carte import EdtCarte

class EdtShedit(Presentation):
    
    """Classe définissant l'éditeur de salle 'shedit'.
    
    """
    
    nom = "shedit"
    
    def __init__(self, personnage, modele):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, modele)
        if personnage and modele:
            self.construire(modele)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, modele):
        """Construction de l'éditeur"""
        # nom
        nom = self.ajouter_choix("nom", "n", Uniligne, modele, "nom")
        nom.parent = self
        nom.prompt = "Nom du navire : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du navire ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nNom actuel : |bc|{objet.nom}|ff|"
        
        # Poids max
        poids_max = self.ajouter_choix("poids maximum", "p", Entier, modele, "poids_max", 1)
        poids_max.parent = self
        poids_max.apercu = "{objet.poids_max} kg"
        poids_max.prompt = "Poids maximum avant de sombrer (en kg) : "
        poids_max.aide_courte = \
            "Entrez |ent|le poids maximum|ff| du navire avant qu'il ne " \
            "sombre ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max} kg"
        
        # Carte
        carte = self.ajouter_choix("carte", "c", EdtCarte, modele)
        carte.parent = self
