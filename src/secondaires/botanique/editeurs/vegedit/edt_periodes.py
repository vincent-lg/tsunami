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


"""Ce fichier définit le contexte-éditeur EdtPeriode."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_periode import EdtPeriode

class EdtPeriodes(Editeur):
    
    """Contexte-éditeur d'édition des périodes du cycle.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("n", self.opt_ajouter_periode)
        self.ajouter_option("d", self.opt_supprimer_periode)
    
    def opt_ajouter_periode(self, arguments):
        """Ajout d'une période.
        
        Syntaxe : /n <age> <nom de la période>
        
        """
        cycle = self.objet
        arguments = arguments.strip()
        if not arguments:
            self.pere << "|err|Précisez le nom de la période.|ff|"
            return
        
        nom = arguments
        if cycle.est_periode(nom):
            self.pere << "|err|Ce nom de période est déjà utilisé.|ff|"
            return
        
        cycle.ajouter_periode(nom)
        self.actualiser()
    
    def opt_supprimer_periode(self, arguments):
        """Suppression d'une période.
        
        Syntaxe : /d <nom de la période>
        
        """
        cycle = self.objet
        arguments = arguments.strip()
        if not arguments:
            self.pere << "|err|Précisez le nom de la période.|ff|"
            return
        
        nom = arguments
        if not cycle.est_periode(nom):
            self.pere << "|err|Ce nom de période n'existe pas.|ff|"
            return
        
        if len(cycle.periodes) == 1:
            self.pere << "|err|Vous ne pouvez supprimer toutes les " \
                    "périodes d'un cycle.|ff|"
            return
        
        cycle.supprimer_periode(nom)
        self.actualiser()
    
    def accueil(self):
        """Message d'accueil du contexte."""
        cycle = self.objet
        msg = "| |tit|" + "Edition des périodes du " \
                "cycle {}".format(cycle.nom).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte + "\n"
        msg += "Périodes définies :"
        
        # Parcours des périodes
        periodes = cycle.periodes
        lignes = []
        for periode in periodes:
            lignes.append("{:<20} jusqu'au {}".format(
                    periode.nom, periode.date_fin))
        
        if periodes:
             msg += "\n\n  " + "\n  ".join(lignes)
        else:
            msg += "\n\n  Aucune"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        cycle = self.objet
        try:
            periode = cycle.get_periode(msg.strip())
        except ValueError:
            self.pere << "|err|période introuvable.|ff|"
            return
        
        enveloppe = EnveloppeObjet(EdtPeriode, periode, None)
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere)
        self.migrer_contexte(contexte)
