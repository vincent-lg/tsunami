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


"""Ce fichier définit le contexte-éditeur 'edt_repos'."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import format_nb

class EdtRepos(Editeur):
    
    """Ce contexte permet d'éditer la sous-catégorie 'repos' d'un détail.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("s", self.opt_asseoir)
        self.ajouter_option("l", self.opt_allonger)
        self.ajouter_option("c", self.opt_connecteur)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        detail = self.objet
        msg = "| |tit|" + "Edition du détail '{}'".format(detail).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += format_nb(detail.nb_places_assises,
                "{nb} place{s} assise{s} ", fem=True)
        msg += "(récupération : {}).\n".format(detail.facteur_asseoir)
        msg += format_nb(detail.nb_places_allongees,
                "{nb} place{s} allongée{s} ", fem=True)
        msg += "(récupération : {}).\n".format(detail.facteur_allonger)
        msg += "Connecteur : |ent|" + detail.connecteur + "|ff|\n"
        
        return msg
    
    def opt_asseoir(self, arguments):
        """Option asseoir.
        Syntaxe : /s <nb> (<facteur>)
        
        """
        detail = self.objet
        if not arguments:
            self.pere << "|err|Précisez au moins un nombre de places.|ff|"
            return
        nb_places = facteur = 0
        try:
            nb_places, facteur = arguments.split(" ")
        except ValueError:
            try:
                nb_places = int(arguments.split(" ")[0])
                assert nb_places >= 0
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez un nombre valide et positif.|ff|"
                return
        try:
            nb_places = int(nb_places)
            facteur = float(facteur)
        except ValueError:
            self.pere << "|err|Précisez des nombres valides.|ff|"
            return
        if nb_places:
            detail.peut_asseoir = True
            detail.nb_places_assises = nb_places
        else:
            detail.peut_asseoir = False
            detail.nb_places_assises = 0
        if facteur:
            detail.facteur_asseoir = facteur
        self.actualiser()
    
    def opt_allonger(self, arguments):
        """Option allonger.
        Syntaxe : /l <nb> (<facteur>)
        
        """
        detail = self.objet
        if not arguments:
            self.pere << "|err|Précisez au moins un nombre de places.|ff|"
            return
        nb_places = facteur = 0
        try:
            nb_places, facteur = arguments.split(" ")
        except ValueError:
            try:
                nb_places = int(arguments.split(" ")[0])
                assert nb_places >= 0
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez un nombre valide et positif.|ff|"
                return
        try:
            nb_places = int(nb_places)
            facteur = float(facteur)
        except ValueError:
            self.pere << "|err|Précisez des nombres valides.|ff|"
            return
        if nb_places:
            detail.peut_allonger = True
            detail.nb_places_allongees = nb_places
        else:
            detail.peut_allonger = False
            detail.nb_places_allongees = 0
        if facteur:
            detail.facteur_allonger = facteur
        self.actualiser()
    
    def opt_connecteur(self, arguments):
        """Option connecteur.
        Syntaxe : /c <connecteur>
        
        """
        detail = self.objet
        if not arguments:
            self.pere << "|err|Précisez un connecteur.|ff|"
            return
        detail.connecteur = arguments
        self.actualiser()
