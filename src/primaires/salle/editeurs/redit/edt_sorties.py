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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'edt_sortie'."""

from primaires.interpreteur.editeur import Editeur
from primaires.salle.sorties import NOMS_SORTIES

class EdtSorties(Editeur):
    
    """Contexte-éditeur d'édition des sorties.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("r", self.opt_renommer_sortie)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|Edition des sorties de {}|ff|".format(
                salle).ljust(87) + "|\n"
        msg += self.opts.separateur + "\n"
        msg += "| " + "Direction".ljust(12) + " | "
        msg += "Vers".ljust(12) + " | " + "Destination".ljust(12) + " | "
        msg += "Réciproque".ljust(12) + " |"
        
        # Parcourt des sorties
        sorties = salle.sorties
        for nom in NOMS_SORTIES:
            sortie = sorties[nom]
            msg += "\n| |ent|" + nom.ljust(12) + "|ff|"
            nom_sortie = ""
            destination = ""
            reciproque = ""
            if sortie:
                if sortie.nom != nom:
                    nom_sortie = sortie.nom_complet
                destination = str(sortie.salle_dest)
                reciproque = sortie.correspondante
            
            msg += " | |ent|" + nom_sortie.ljust(12) + "|ff|"
            msg += " | " + destination.ljust(12)
            msg += " | " + reciproque.ljust(12) + " |"
        
        return msg
    
    def opt_renommer_sortie(self, arguments):
        """Renomme une sortie en un autre nom
        La syntaxe pour renommer une sortie est :
            /option ancien_nom / nouveau nom (/ article)
        
        """
        salle = self.objet
        sorties = salle.sorties
        try:
            ancien_nom, nouveau_nom, article = arguments.split(" / ")
        except ValueError:
            try:
                ancien_nom, nouveau_nom = arguments.split(" / ")
                article = ""
            except ValueError:
                self.pere << "Syntaxe invalide pour cette option."
                return
        
        try:
            ancien_nom = sorties.get_nom_long(ancien_nom)
        except KeyError:
            self.pere << "Sortie inconnue {}.".format(ancien_nom)
        else:
            nouveau_nom = nouveau_nom.lower()
            sortie = sorties[ancien_nom]
            if sortie is None:
                self.pere << "|err|Cette sortie n'existe pas.|ff|"
                return
            
            try:
                t_val = sorties.get_sortie_par_nom_ou_direction(nouveau_nom)
                if t_val is None or t_val.direction != ancien_nom:
                    self.pere << "|err|Ce nom de sortie est déjà utilisé.|ff|"
                    return
            except KeyError:
                pass
            
            sortie.nom = nouveau_nom
            sortie.deduire_article()
            if article:
                sortie.article = article
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        pass
