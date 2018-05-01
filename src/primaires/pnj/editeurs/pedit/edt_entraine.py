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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur Edtentraine."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import supprimer_accents

class EdtEntraine(Editeur):
    
    """Contexte-éditeur d'édition de l'équipement du PNJ.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Édition des stats entraînées par {}".format(
                prototype).ljust(64)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Stats entraînées par ce PNJ :"
        
        # Parcours des stats
        stats = prototype.entraine_stats
        lignes = []
        for stat, max in sorted(stats.items()):
            lignes.append("{:<15} (max={})".format(stat, max))
        
        if lignes:
             msg += "\n\n  " + "\n  ".join(lignes)
        else:
            msg += "\n\n  Aucune"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        try:
            nom, max = msg.split(" ")
            assert max.isdigit()
            max = int(max)
            assert 0 <= max <= 100
        except ValueError:
            self.pere << "|err|Précisez la stat suivie d'un espace et de " \
                    "la valeur maximum.|ff|"
            return
        except AssertionError:
            self.pere << "|err|Maximum invalide.|ff|"
            return
        
        nom = supprimer_accents(nom)
        if nom not in importeur.perso.cfg_stats.entrainables:
            self.pere << "|err|Stat inconnue.|ff|"
            return
        
        if max == 0: # suppression
            if nom in prototype.entraine_stats:
                del prototype.entraine_stats[nom]
                self.actualiser()
                return
            else:
                self.pere << "|err|Cette stat n'est pas défini dans ce " \
                        "prototype.|ff|"
                return
        
        prototype.entraine_stats[nom] = max
        self.actualiser()
