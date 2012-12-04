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


"""Ce fichier définit le contexte-éditeur 'edt_etats'."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_etat import EdtEtat

class EdtEtats(Editeur):
    
    """Contexte-éditeur d'édition des états."""
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("n", self.opt_creer_etat)
        self.ajouter_option("d", self.opt_supprimer_etat)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Edition des états de {}".format(prototype).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Options :\n"
        msg += " |cmd|/n <nom singulier de l'état à créer>|ff|\n"
        msg += " |cmd|/d <nom de l'état à supprimer>|ff|\n\n"
        msg += "États actuels :\n"
        
        # Parcours des états
        i = 1
        for etat in prototype.etats:
            msg += "\n  " + str(i).rjust(2) + " " + etat.nom_singulier
            i += 1
        
        if not prototype.etats:
            msg += "\n  Aucun état pour l'instant"
        
        return msg
    
    def opt_supprimer_etat(self, arguments):
        """Supprime un état.
        
        Syntaxe :
            /d <nom de l'état>
        
        """
        pass
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        etats = prototype.etats
        try:
            no = int(msg)
            assert no > 0
            assert no <= len(etats)
        except ValueError:
            self.pere << "|err|Nombre invalide.|ff|"
            return
        
        etat = etats[no]
        enveloppe = EnveloppeObjet(Edtetat, etat, None)
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere)
        self.migrer_contexte(contexte)
