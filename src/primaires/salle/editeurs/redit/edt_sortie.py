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


"""Contexte-éditeur 'edt_sortie', voir plus bas."""

from primaires.interpreteur.editeur import Editeur

class EdtSortie(Editeur):

    """Contexte d'édition des sorties une par une. Ce contexte est fils
    du contexte 'edt_sorties', voir la méthode interpreter() de ce dernier.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("r", self.opt_renommer_sortie)
        self.ajouter_option("s", self.opt_changer_sortie)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        sortie = self.objet
        salle = sortie.parent
        msg = "| |tit|"
        msg += "Edition de la sortie {} de {}" \
                .format(sortie.direction, salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        
        msg += "\n Nom de la sortie : |ent|" + sortie.nom_complet + "|ff|"
        msg += "\n Direction : " + sortie.direction
        msg += " (vers |vr|" + str(sortie.salle_dest) + "|ff|)"
        msg += "\n Réciproque : |cy|" + sortie.correspondante + "|ff|"
        
        return msg
    
    def opt_renommer_sortie(self, arguments):
        """Cette option renomme une sortie.
        Syntaxe : /r nom (/ préfixe)
        
        """
        sortie = self.objet
        salle = sortie.parent
        try:
            nouveau_nom, article = arguments.split(" / ")
        except ValueError:
            nouveau_nom = arguments
            article = ""
        
        nouveau_nom = nouveau_nom.lower()
        
        try:
            t_val = salle.sorties.get_sortie_par_nom_ou_direction(nouveau_nom)
            if t_val is None or t_val.direction != sortie.direction:
                self.pere << "|err|Ce nom de sortie est déjà utilisé.|ff|"
                return
        except KeyError:
            pass
        
        sortie.nom = nouveau_nom
        sortie.deduire_article()
        if article:
            sortie.article = article
        self.actualiser()
    
    def opt_changer_sortie(self, arguments):
        """Cette option modifie la salle vers laquelle pointe une sortie.
        Syntaxe : /s id_salle
        
        """
        sortie = self.objet
        salle = sortie.parent
        id_salle = arguments
        try:
            d_salle = type(self).importeur.salle[id_salle]
        except KeyError:
            self.pere << \
                "|err|L'identifiant '{}' n'est pas valide.|ff|".format(id_salle)
            return
        
        dir_opposee = salle.sorties.get_nom_oppose(sortie.direction)
        if d_salle.sorties.sortie_existe(dir_opposee):
            self.pere << \
                "|err|La direction opposée a déjà été définie dans {}.|ff|". \
                format(d_salle.ident)
            return
        if salle is d_salle:
            self.pere << \
                "|err|La salle de destination est la même que la salle " \
                "d'origine.|ff|"
            return
        
        sortie.salle_dest.sorties.supprimer_sortie(sortie.correspondante)
        salle.sorties.supprimer_sortie(sortie.direction)
        salle.sorties.ajouter_sortie(sortie.direction, sortie.nom,
                modele=sortie, salle_dest=d_salle, corresp=dir_opposee)
        d_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                salle_dest=salle, corresp=sortie.nom)
        self.objet = salle.sorties[sortie.direction]
        self.actualiser()
