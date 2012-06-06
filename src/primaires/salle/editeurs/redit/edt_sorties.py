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


"""Ce fichier définit le contexte-éditeur 'edt_sorties'."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.salle.sorties import NOMS_SORTIES
from .edt_sortie import EdtSortie

class EdtSorties(Editeur):
    
    """Contexte-éditeur d'édition des sorties.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("r", self.opt_renommer_sortie)
        self.ajouter_option("s", self.opt_changer_sortie)
        self.ajouter_option("d", self.opt_suppr_sortie)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition des sorties de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Sorties courantes :\n"
        
        # Parcours des sorties
        sorties = salle.sorties
        liste_sorties = ""
        for nom in NOMS_SORTIES.keys():
            direction = "\n  |ent|" + nom.ljust(10) + "|ff| :"
            sortie = sorties[nom]
            if sortie:
                destination = ""
                if sortie.nom != nom:
                    destination = " vers " + sortie.nom_complet + ""
                    destination += " (|vr|" + str(sortie.salle_dest) + "|ff|)"
                else:
                    destination = " vers |vr|" + str(sortie.salle_dest) + "|ff|"
                reciproque = sortie.correspondante and (", réciproque : " \
                        "|cy|" + sortie.correspondante + "|ff|") or " "
                liste_sorties += direction
                liste_sorties += destination
                liste_sorties += reciproque
        if not liste_sorties:
            liste_sorties += "\n Aucune sortie pour l'instant."
        msg += liste_sorties
        
        return msg
    
    def opt_renommer_sortie(self, arguments):
        """Renomme une sortie en un autre nom
        La syntaxe pour renommer une sortie est :
            /r ancien_nom / nouveau nom (/ article)
        
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
                self.pere << "|err|La syntaxe est invalide pour cette " \
                        "option.|ff|"
                return
        
        try:
            ancien_nom = sorties.get_nom_long(ancien_nom)
        except KeyError:
            self.pere << "|err|La direction '{}' est " \
                    "inconnue.|ff|".format(ancien_nom)
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
    
    def opt_changer_sortie(self, arguments):
        """Modifie une sortie comme setexit
        Le fonctionnement est le même, cette option permet de lier un sortie
        à une salle.
        Syntaxe : /s nom / id_salle
            
        """
        salle = self.objet
        sorties = salle.sorties
        try:
            nom, id_salle = arguments.split(" / ")
        except ValueError:
            self.pere << "|err|La syntaxe est invalide pour cette " \
                    "option.|ff|"
            return
        try:
            nom = sorties.get_nom_long(nom)
        except KeyError:
            self.pere << "|err|La direction '{}' n'existe pas.|ff|".format(nom)
            return
        try:
            d_salle = type(self).importeur.salle[id_salle]
        except KeyError:
            self.pere << \
                "|err|L'identifiant '{}' n'est pas valide.|ff|".format(id_salle)
            return
        
        dir_opposee = sorties.get_nom_oppose(nom)
        if sorties.sortie_existe(nom):
            self.pere << \
                "|err|Cette direction a déjà été définie dans la salle " \
                "courante.|ff|"
            return
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
        
        sorties.ajouter_sortie(nom, nom,
                salle_dest=d_salle, corresp=dir_opposee)
        d_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                salle_dest=salle, corresp=nom)
        self.actualiser()
    
    def opt_suppr_sortie(self, arguments):
        """Supprime une sortie
        Syntaxe : /d nom
        
        """
        salle = self.objet
        sorties = salle.sorties
        nom = arguments
        
        try:
            d_salle = sorties[nom].salle_dest
        except (KeyError, AttributeError):
            self.pere << "|err|La sortie spécifiée n'existe pas.|ff|"
        else:
            dir_opposee = salle.sorties.get_nom_oppose(nom)
            
            d_salle.sorties.supprimer_sortie(dir_opposee)
            salle.sorties.supprimer_sortie(nom)
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        salle = self.objet
        sorties = salle.sorties
        
        try:
            sortie = sorties[msg]
            if not sortie:
                raise AttributeError
        except (KeyError, AttributeError):
            self.pere << "|err|La sortie spécifiée n'existe pas.|ff|"
        else:
            enveloppe = EnveloppeObjet(EdtSortie, sortie, None)
            enveloppe.parent = self
            enveloppe.aide_courte = \
                "Entrez |ent|/|ff| pour revenir à la fenêtre parente.\n" \
                "Options :\n" \
                " - |cmd|/r <nouveau nom> (/ <préfixe>)|ff| : renomme la " \
                "sortie\n" \
                " - |cmd|/s <identifiant d'une salle>|ff| : fait pointer la " \
                "sortie vers la salle\n" \
                "   spécifiée\n" \
                " - |cmd|/dq|ff| : détruit la sortie réciproque (permet de " \
                "créer des sorties à sens\n   unique)\n" \
                " - |cmd|/c|ff| : bascule l'état caché de la sortie\n" \
                " - |cmd|/p (<clef>)|ff| : ajoute ou supprime une porte à " \
                "la sortie ; vous pouvez\n" \
                "   préciser l'identifiant d'un objet de type clef"
            if sortie.direction in ("bas", "haut"):
                enveloppe.aide_courte += \
                    "\n - |cmd|/e <difficulté à escalader entre 1 et 10|ff|"
            contexte = enveloppe.construire(self.pere)
            self.migrer_contexte(contexte)
