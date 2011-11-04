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
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Magasin, détaillée plus bas."""

from bases.collections.liste_id import ListeID
from abstraits.obase import *
from primaires.pnj.prototype import Prototype
from primaires.objet.types.base import BaseType

class Magasin(BaseObj):
    
    """Cette classe représente un magasin.
    
    """
    
    def __init__(self, nom, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.nom = nom
        self.parent = parent
        self._vendeur = ""
        self._monnaies = []
        self.caisse = 0
        self._o_prototypes = {} # clé_obj : quantité
        self._p_prototypes = {} # clé_pnj : quantité
        # On passe le statut à 'construit'
        self._statut = CONSTRUIT
    
    def __getnewargs__(self):
        return ("", )
    
    def enregistrer(self):
        """Enregistre le magasin dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    def __str__(self):
        """Affichage du magasin en éditeur"""
        liste_obj = []
        liste_pnj = []
        taille_max = 0
        for o in self.liste_objets:
            if o and len(o.cle) > taille_max:
                taille_max = len(o.cle) + 1
        for p in self.liste_pnjs:
            if p and len(p.cle) > taille_max:
                taille_max = len(p.cle) + 1
        taille_max = taille_max >= 6 and taille_max or 6
        a_detruire = []
        for o, nb in self._o_prototypes.items():
            obj = self.get_item_par_cle(o)
            if not obj:
                a_detruire.append(o)
            else:
                liste_obj.append(obj.cle.ljust(taille_max) + "|" + str( \
                        obj.prix).rjust(7) + " |" + str(nb).rjust(9) + " |\n")
        for p, nb in self._p_prototypes.items():
            pnj = self.get_item_par_cle(p)
            if not pnj:
                a_detruire.append(o)
            else:
                liste_pnj.append(pnj.cle.ljust(taille_max) + "|" + str( \
                        pnj.prix).rjust(7) + " |" + str(nb).rjust(9) + " |\n")
        for item in a_detruire: # purge des items inexistants
            del self[item]
        liste_obj = sorted(liste_obj)
        liste_pnj = sorted(liste_pnj)
        if liste_obj or liste_pnj:
            ret = "+" + "-" * (taille_max + 1) + "+--------+----------+\n"
            ret += "| |tit|" + "Objet".ljust(taille_max) + "|ff|"
            ret += "|   |tit|Prix|ff| | |tit|Quantité|ff| |\n"
            if liste_obj:
                ret += "+" + "-" * (taille_max + 1) + "+--------+----------+\n"
                ret += "| " + "| ".join(liste_obj)
            if liste_pnj:
                ret += "+" + "-" * (taille_max + 1) + "+--------+----------+\n"
                ret += "| " + "| ".join(liste_pnj)
            ret += "+" + "-" * (taille_max + 1) + "+--------+----------+"
        else:
            ret = "|att|Aucun objet en vente.|ff|"
        return ret
    
    def __contains__(self, item):
        """Retourne True si l'objet est en vente, False sinon"""
        return item in self._o_prototypes or item in self._p_prototypes
    
    def __getitem__(self, item):
        """Retourne la quantité d'item en vente"""
        return self._o_prototypes[item] or self._p_prototypes[item]
    
    def __setitem__(self, item, quantite):
        """Ajoute un objet ou modifie sa quantité"""
        if isinstance(self.get_item_par_cle(item), BaseType):
            self._o_prototypes[item] = quantite
        elif isinstance(self.get_item_par_cle(item), Prototype):
            self._p_prototypes[item] = quantite
        self.enregistrer()
    
    def __delitem__(self, item):
        """Retire un objet du magasin"""
        if isinstance(item, str):
            if item in self._o_prototypes:
                del self._o_prototypes[item]
            elif item in self._p_prototypes:
                del self._p_prototypes[item]
        self.enregistrer()
    
    def _get_vendeur(self):
        """Retourne le prototype vendeur"""
        if self._vendeur in type(self).importeur.pnj.prototypes:
            return type(self).importeur.pnj.prototypes[self._vendeur]
        else:
            self._vendeur = ""
            return None
    def _set_vendeur(self, cle):
        self._vendeur = cle
        self.enregistrer()
    vendeur = property(_get_vendeur, _set_vendeur)
    
    @property
    def cle_vendeur(self):
        """Retourne le nom du vendeur"""
        return ("|vrc|" + self._vendeur + "|ff|") if self._vendeur else \
                "|rgc|aucun|ff|"
    
    @property
    def monnaies(self):
        """Retourne la liste des prototypes de monnaie utilisables"""
        ret = ListeID()
        for m in self._monnaies:
            if m in type(self).importeur.objet.prototypes:
                ret.append(type(self).importeur.objet.prototypes[m])
            else:
                self._monnaies.remove(m)
        return ret
    
    @property
    def str_monnaies(self):
        """Affiche la liste des monnaies utilisables dans ce magasin"""
        ret = "|ff|, |jn|".join(sorted(self._monnaies))
        ret = "|rgc|aucune|ff|" if not ret else ("|jn|" + ret + "|ff|")
        return ret
    
    @property
    def liste_objets(self):
        """Retourne les objets en vente, par ordre alphabétique"""
        ret = ListeID()
        liste_cles = sorted(list(self._o_prototypes.keys()))
        for cle in liste_cles:
            ret.append(self.get_item_par_cle(cle))
        return ret
    
    @property
    def liste_pnjs(self):
        """Retourne la liste des PNJs en vente, par ordre alphabétique"""
        ret = ListeID()
        liste_cles = sorted(list(self._p_prototypes.keys()))
        for cle in liste_cles:
            ret.append(self.get_item_par_cle(cle))
        return ret
    
    def ajouter_monnaie(self, monnaie):
        """Ajoute une monnaie à la liste"""
        self._monnaies.append(monnaie)
        self.enregistrer()
    
    def supprimer_monnaie(self, monnaie):
        """Supprime la monnaie de la liste"""
        self._monnaies.remove(monnaie)
        self.enregistrer()
    
    def encaisser(self, calcul):
        """Modifie la valeur de la caisse en fonction d'une chaîne de calcul"""
        self.caisse = eval(str(self.caisse) + calcul)
        self.enregistrer()
    
    def est_en_vente(self, objet):
        """Retourne True si la clé correspond à un objet en vente,
        False sinon.
        
        """
        return objet in self._o_prototypes.keys()
    
    def get_item_par_id(self, id):
        """Retourne un objet en fonction de son id (voir self.afficher)"""
        liste_items = list(self._o_prototypes.keys()) + \
                list(self._p_prototypes.keys())
        try:
            item = get_item_par_cle(liste_items[id - 1])
            assert(item is not None)
        except (IndexError, AssertionError):
            del self[liste_items[id - 1]]
            return None
        else:
            return item
    
    def get_item_par_cle(self, cle):
        """Retourne un objet en fonction de sa clé"""
        if cle in type(self).importeur.objet.prototypes:
            return type(self).importeur.objet.prototypes[cle]
        else:
            return None
    
    def afficher(self):
        """Affichage du magasin en jeu"""
        ret = self.nom + "\n\n"
        liste_obj = []
        liste_pnj = []
        taille_max = 0
        for o in self.liste_objets:
            if o and len(o.nom_singulier) > taille_max:
                taille_max = len(o.nom_singulier) + 1
        for p in self.liste_pnjs:
            if p and len(p.nom_singulier) > taille_max:
                taille_max = len(p.nom_singulier) + 1
        taille_max = taille_max >= 6 and taille_max or 6
        id = 1
        a_detruire = []
        for o, nb in self._o_prototypes.items():
            obj = self.get_item_par_cle(o)
            if not obj:
                a_detruire.append(o)
            else:
                liste_obj.append(("#" + str(id)).rjust(3) + " | " + \
                        obj.nom_singulier.ljust(taille_max) + "|" + str( \
                        obj.prix).rjust(5) + " |" + str(nb).rjust(5) + " |\n")
            id += 1
        for p, nb in self._p_prototypes.items():
            pnj = self.get_item_par_cle(p)
            if not pnj:
                a_detruire.append(p)
            else:
                liste_pnj.append(("#" + str(id)).rjust(3) + " | " + \
                        pnj.nom_singulier.ljust(taille_max) + "|" + str( \
                        pnj.prix).rjust(5) + " |" + str(nb).rjust(5) + " |\n")
            id += 1
        for item in a_detruire: # purge des items inexistants
            del self[item]
        liste_obj = sorted(liste_obj)
        liste_pnj = sorted(liste_pnj)
        if liste_obj or liste_pnj:
            ret += "+-----+-" + "-" * taille_max + "+------+------+\n"
            ret += "|  |tit|ID|ff| | |tit|" + "Objet".ljust(taille_max)
            ret += "|ff|| |tit|Prix|ff| |  |tit|Qtt|ff| |\n"
            if liste_obj:
                ret += "+-----+-" + "-" * taille_max + "+------+------+\n"
                ret += "| " + "| ".join(liste_obj)
            if liste_pnj:
                ret += "+-----+-" + "-" * taille_max + "+------+------+\n"
                ret += "| " + "| ".join(liste_pnj)
            ret += "+-----+-" + "-" * taille_max + "+------+------+"
        else:
            ret += "|att|Le magasin ne semble pas approvisionné pour le " \
                    "moment.|ff|"
        return ret
