# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier définit le contexte-éditeur EdtPoissons."""

from primaires.interpreteur.editeur import Editeur

class EdtPoissons(Editeur):
    
    """Contexte-éditeur d'édition des poissons du banc.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        banc = self.objet
        msg = "| |tit|" + "Edition des poissons disponibles dans le " \
                "banc {}".format(banc).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte + "\n"
        msg += "Poissons ddéfinis :"
        
        # Parcours des poissons
        poissons = sorted([(poisson, proba) for poisson, proba in \
                banc.poissons.items()], key=lambda e: e[1], reverse=True)
        proba_max = sum(b for a, b in poissons)
        lignes = []
        for poisson, proba in poissons:
            lignes.append("{:<20} : {:>3} / {:>3} ({:>3}%)".format(
                    poisson.cle, proba, proba_max, int(
                    proba / proba_max * 100)))
        
        if poissons:
             msg += "\n\n  " + "\n  ".join(lignes)
        else:
            msg += "\n\n  Aucun"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        banc = self.objet
        try:
            cle, proba = msg.split(" ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
            return
        
        try:
            proba = int(proba)
            assert proba >= 0
        except (ValueError, AssertionError):
            self.pere << "|err|Ce nombre est invalide.|ff|"
            return
        
        try:
            proto = importeur.objet.prototypes[cle.lower()]
        except KeyError:
            self.pere << "|err|Clé {} invalide.|ff|".format(cle)
            return
        
        if not proto.est_de_type("poisson"):
            self.pere << "|err|L'objet {} n'est pas un poisson.|ff|".Format(
            cle)
            return
        
        if proba == 0:
            if proto in banc.poissons:
                del banc.poissons[proto]
            else:
                self.pere << "|err|Cette clé n'est pas définie dans le " \
                        "banc et ne peut donc être supprimée.|ff|"
                return
        else:
            banc.poissons[proto] = proba
            self.actualiser()
