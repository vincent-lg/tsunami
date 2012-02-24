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


"""Ce fichier définit le contexte-éditeur EdtPnjRepop."""

from primaires.interpreteur.editeur import Editeur

class EdtPnjRepop(Editeur):
    
    """Contexte-éditeur d'édition des pnj disponibles au repop.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition des pnj disponibles au repop de {}".format(
        salle).ljust(59)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "PNJ disponibles au repop :"
        
        # Parcours des pnj
        repop = salle.pnj_repop
        pnj = []
        for proto, nb in repop.items():
            nb_e = len([p for p in proto.pnj if p.salle_origine is salle])
            nb += nb_e
            pnj.append(proto.cle.ljust(20) + " (" + str(nb).rjust(3))
        
        pnj.sort
        if pnj:
             msg += "\n\n  " + "\n  ".join(pnj)
        else:
            msg += "\n\n  Aucun"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        salle = self.objet
        try:
            cle, nb = msg.split(" ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide."
            return
        
        try:
            nb = int(nb)
            assert nb >= 0
        except (ValueError, AssertionError):
            self.pere << "|err|Ce nombre est invalide.|ff|"
            return
        
        try:
            proto = importeur.pnj.prototypes[cle.lower()]
        except KeyError:
            self.pere << "|err|Clé {} invalide.|ff|".format(cle)
            return
        
        nb_e = len([p for p in proto.pnj if p.salle_origine is self])
        nb = nb - nb_e
        if nb <= 0:
            if proto in salle.pnj_repop:
                del salle.pnj_repop[proto]
                self.actualiser()
            else:
                self.pere << "|err|Cette clé n'est pas définie dans le " \
                        "repop et ne peut donc être supprimée.|ff|"
        else:
            salle.pnj_repop[proto] = nb
            self.actualiser()
