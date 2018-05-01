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


"""Ce fichier définit le contexte-éditeur EdtCycle."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_cycle import EdtCycle

class EdtCycles(Editeur):
    
    """Contexte-éditeur d'édition des cycles du prototype végétal.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("n", self.opt_ajouter_cycle)
        self.ajouter_option("d", self.opt_supprimer_cycle)
    
    def opt_ajouter_cycle(self, arguments):
        """Ajout d'un cycle.
        
        Syntaxe : /n <age> <nom du cycle>
        
        """
        prototype = self.objet
        arguments = arguments.strip()
        if not arguments:
            self.pere << "|err|Précisez l'âge minimum du cycle suivi " \
                    "d'un espace et de son nom.|ff|"
            return
        
        args = arguments.split(" ")
        age = args[0]
        nom = " ".join(args[1:])
        if not nom:
            self.pere << "|err|Précisez un nom.|ff|"
            return
        
        try:
            age = int(age)
            assert age >= 0
        except (ValueError, AssertionError):
            self.pere << "|err|Age invalide.|ff|"
            return
        
        if prototype.est_cycle(nom):
            self.pere << "|err|Ce nom de cycle est déjà utilisé.|ff|"
            return
        
        prototype.ajouter_cycle(nom, age)
        self.actualiser()
    
    def opt_supprimer_cycle(self, arguments):
        """Suppression d'un cycle.
        
        Syntaxe : /d <nom du cycle>
        
        """
        prototype = self.objet
        arguments = arguments.strip()
        if not arguments:
            self.pere << "|err|Précisez le nom du cycle.|ff|"
            return
        
        nom = arguments
        if not prototype.est_cycle(nom):
            self.pere << "|err|Ce nom de cycle n'existe pas.|ff|"
            return
        
        if len(prototype.cycles) == 1:
            self.pere << "|err|Vous ne pouvez supprimer tous les " \
                    "cycles d'un prototype.|ff|"
            return
        
        prototype.supprimer_cycle(nom)
        self.actualiser()
    
    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Edition des cycles dans le " \
                "prototype {}".format(prototype.cle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte + "\n"
        msg += "Cycles définis :"
        
        # Parcours des cycles
        cycles = prototype.cycles
        lignes = []
        for cycle in cycles:
            s = "s" if len(cycle.periodes) > 1 else ""
            lignes.append("{:<20} : {} période{s}".format(
                    cycle.nom, len(cycle.periodes), s=s))
        
        if cycles:
             msg += "\n\n  " + "\n  ".join(lignes)
        else:
            msg += "\n\n  Aucun"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        try:
            cycle = prototype.get_cycle(msg.strip())
        except ValueError:
            self.pere << "|err|Cycle introuvable.|ff|"
            return
        
        enveloppe = EnveloppeObjet(EdtCycle, cycle, None)
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere)
        self.migrer_contexte(contexte)
