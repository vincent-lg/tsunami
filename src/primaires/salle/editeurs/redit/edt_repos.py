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


"""Ce fichier contient l'éditeur EdtRepos, détaillé plus bas."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag

class EdtRepos(Presentation):
    
    """Ce contexte permet d'éditer la sous-catégorie 'repos' d'un détail.
    
    """
    
    def __init__(self, pere, detail=None, attribut=None):
        """Constructeur de l'éditeur."""
        Presentation.__init__(self, pere, detail, attribut, False)
        if pere and detail:
            self.construire(detail)
    
    def construire(self, detail):
        """Construction de l'éditeur"""
        # Peut s'asseoir
        asseoir = self.ajouter_choix("peut s'asseoir", "as", Flag, detail,
                "peut_asseoir")
        asseoir.parent = self
        
        # Peut s'allonger
        allonger = self.ajouter_choix("peut s'allonger", "al", Flag, detail,
                "peut_allonger")
        allonger.parent = self
        
        # Nombre de places assises
        nb_assises = self.ajouter_choix("nombre de places assises", "n",
                Entier, detail, "nb_places_assises", 1)
        nb_assises.parent = self
        nb_assises.apercu = "{objet.nb_places_assises}"
        nb_assises.prompt = "Entrez le nombre de places assises : "
        nb_assises.aide_courte = \
            "Entrez le |ent|nombre de places assises|ff| du détail ou\n" \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Nombre actuel : {objet.nb_places_assises}"
        
        # Nombre de places allongées
        nb_allongees = self.ajouter_choix("nombre de places allongées", "b",
                Entier, detail, "nb_places_allongees", 1)
        nb_allongees.parent = self
        nb_allongees.apercu = "{objet.nb_places_allongees}"
        nb_allongees.prompt = "Entrez le nombre de places allongées : "
        nb_allongees.aide_courte = \
            "Entrez le |ent|nombre de places allongées|ff| du détail ou\n" \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Nombre actuel : {objet.nb_places_allongees}"
        
        # Connecteur
        connecteur = self.ajouter_choix("connecteur", "c", Uniligne, detail,
                "connecteur")
        connecteur.parent = self
        connecteur.prompt = "Connecteur du détail : "
        connecteur.apercu = "{objet.connecteur}"
        connecteur.aide_courte = \
            "Entrez le |ent|connecteur|ff| du détail ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nLe connecteur fait la " \
            "liaison entre l'action et le titre du détail.\nPar exemple : " \
            "\"Vous vous allongez |att|sur|ff| une table.|ff|\"\n\n" \
            "Connecteur actuel : |bc|{objet.connecteur}|ff|"
        
        # Facteur de récupération quand on s'asseoit
        facteur_as = self.ajouter_choix(
                "facteur de récupération en s'asseyant", "f", Flottant,
                detail, "facteur_asseoir")
        facteur_as.parent = self
        facteur_as.prompt = "Entrez le facteur de récupération : "
        facteur_as.aide_courte = \
            "Entrez le facteur de récupération du détail quand on " \
            "s'asseoit dessus\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nLe facteur doit tourner autour de 1 (1 = une " \
            "récupération normale).\n\nFacteur de récupération actuel : " \
            "{objet.facteur_asseoir}"
        
        # Facteur de récupération quand on s'allonge
        facteur_al = self.ajouter_choix(
                "facteur de récupération en s'allongeant", "u", Flottant,
                detail, "facteur_allonger")
        facteur_al.parent = self
        facteur_al.prompt = "Entrez le facteur de récupération : "
        facteur_al.aide_courte = \
            "Entrez le facteur de récupération du détail quand on " \
            "s'allonge dessus\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nLe facteur doit tourner autour de 1 (1 = une " \
            "récupération normale).\n\nFacteur de récupération actuel : " \
            "{objet.facteur_allonger}"

