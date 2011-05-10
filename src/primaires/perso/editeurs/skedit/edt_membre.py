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


"""Contexte-éditeur 'edt_membre', voir plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import oui_ou_non

class EdtMembre(Editeur):

    """Contexte d'édition des membres une par une. Ce contexte est fils
    du contexte 'edt_membres', voir la méthode interpreter() de ce dernier.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("r", self.opt_renommer_membre)
        self.ajouter_option("s", self.opt_changer_membre)
        self.ajouter_option("c", self.opt_cache)
        self.ajouter_option("dq", self.opt_detruire_reciproque)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        membre = self.objet
        salle = membre.parent
        msg = "| |tit|"
        msg += "Edition de la membre {} de {}".format(
                membre.direction, salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        
        msg += "\n Nom de la membre : |ent|" + membre.nom_complet + "|ff|"
        msg += "\n Direction : " + membre.direction
        msg += " (vers |vr|" + str(membre.salle_dest) + "|ff|)"
        msg += "\n Réciproque : |cy|" + membre.correspondante + "|ff|"
        msg += "\n Membre cachée : |cy|" + oui_ou_non(membre.cache) + "|ff|"
        
        return msg
    
    def opt_renommer_membre(self, arguments):
        """Cette option renomme une membre.
        Syntaxe : /r nom (/ préfixe)
        
        """
        membre = self.objet
        salle = membre.parent
        try:
            nouveau_nom, article = arguments.split(" / ")
        except ValueError:
            nouveau_nom = arguments
            article = ""
        
        nouveau_nom = nouveau_nom.lower()
        
        try:
            t_val = salle.membres.get_membre_par_nom_ou_direction(nouveau_nom)
            if t_val is None or t_val.direction != membre.direction:
                self.pere << "|err|Ce nom de membre est déjà utilisé.|ff|"
                return
        except KeyError:
            pass
        
        membre.nom = nouveau_nom
        membre.deduire_article()
        if article:
            membre.article = article
        self.actualiser()
    
    def opt_changer_membre(self, arguments):
        """Cette option modifie la salle vers laquelle pointe une membre.
        Syntaxe : /s id_salle
        
        """
        membre = self.objet
        salle = membre.parent
        id_salle = arguments
        try:
            d_salle = type(self).importeur.salle[id_salle]
        except KeyError:
            self.pere << \
                "|err|L'identifiant '{}' n'est pas valide.|ff|".format(id_salle)
            return
        
        dir_opposee = salle.membres.get_nom_oppose(membre.direction)
        if d_salle.membres.membre_existe(dir_opposee):
            self.pere << \
                "|err|La direction opposée a déjà été définie dans {}.|ff|". \
                format(d_salle.ident)
            return
        if salle is d_salle:
            self.pere << \
                "|err|La salle de destination est la même que la salle " \
                "d'origine.|ff|"
            return
        
        membre.salle_dest.membres.supprimer_membre(membre.correspondante)
        salle.membres.supprimer_membre(membre.direction)
        salle.membres.ajouter_membre(membre.direction, membre.nom,
                modele=membre, salle_dest=d_salle, corresp=dir_opposee)
        d_salle.membres.ajouter_membre(dir_opposee, dir_opposee,
                salle_dest=salle, corresp=membre.nom)
        self.objet = salle.membres[membre.direction]
        self.actualiser()
    
    def opt_cache(self, argument):
        """Fait passer de cache en non caché la membre et réciproquement.
        Aucun argument n'est nécessaire.
        
        """
        membre = self.objet
        membre.cache = not membre.cache
        self.actualiser()
    
    def opt_detruire_reciproque(self, argument):
        """Permet de détruire la réciproque.
        Supprime du même coup le lien entre les deux membres.
        
        """
        membre = self.objet
        reciproque = membre.membre_opposee
        if not membre.membre_opposee:
            self.pere << "|err|Cette membre n'a pas de réciproque.|ff|"
            return
        
        # On casse le lien
        membre.correspondante = ""
        reciproque.correspondante = ""
        
        # On détruit à présent la membre opposée
        membre.salle_dest.membres.supprimer_membre(reciproque.direction)
        
        self.actualiser()
