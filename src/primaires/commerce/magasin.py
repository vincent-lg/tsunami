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
        self.vendeur = None
        self.monnaies = []
        self.caisse = 0
        self._o_prototypes = {}
        self._p_prototypes = {}
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        """Affichage du magasin en éditeur"""
        liste_obj = []
        liste_pnj = []
        taille_max = 0
        for o in self._o_prototypes.keys():
            if len(o.cle) > taille_max:
                taille_max = len(o.cle) + 1
        for p in self._p_prototypes.keys():
            if len(p.cle) > taille_max:
                taille_max = len(p.cle) + 1
        taille_max = taille_max >= 6 and taille_max or 6
        for o, nb in self._o_prototypes.items():
            liste_obj.append(o.cle.ljust(taille_max) + "|" + \
                    str(o.prix).rjust(7) + " |" + str(nb).rjust(9) + " |\n")
        for p, nb in self._p_prototypes.items():
            liste_pnj.append(p.cle.ljust(taille_max) + "|" + \
                    str(p.prix).rjust(7) + " |" + str(nb).rjust(9) + " |\n")
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
    
    def __setitem__(self, item, quantite):
        """Ajoute un objet ou modifie sa quantité"""
        if isinstance(item, BaseType):
            self._o_prototypes[item] = quantite
        elif isinstance(item, Prototype):
            self._p_prototypes[item] = quantite
    
    def __delitem__(self, item):
        """Retire un objet du magasin"""
        if isinstance(item, str):
            for o in self._o_prototypes.keys():
                if o.cle == item:
                    del self._o_prototypes[o]
                    break
            for p in self._p_prototypes.keys():
                if p.cle == item:
                    del self._p_prototypes[p]
                    break
        else:
            if item in self._o_prototypes:
                del self._o_prototypes[item]
            if item in self._p_prototypes:
                del self._p_prototypes[item]
    
    @property
    def cle_vendeur(self):
        """Retourne le nom du vendeur"""
        return ("|vrc|" + self.vendeur.cle + "|ff|") if self.vendeur else \
                "|rgc|aucun|ff|"
    
    @property
    def str_monnaies(self):
        """Retourne la liste des monnaies utilisables dans ce magasin"""
        ret = ", ".join([m.cle for m in self.monnaies])
        ret = "|rgc|aucune|ff|" if not ret else ("|jn|" + ret + "|ff|")
        return ret
    
    @property
    def liste_objets(self):
        """Retourne la liste des objets en vente, par ordre alphabétique"""
        ret = []
        liste_cles = sorted([o.cle for o in self._o_prototypes.keys()])
        for cle in liste_cles:
            ret.append(self.get_item_par_cle(cle))
        return ret
    
    @property
    def liste_pnjs(self):
        """Retourne la liste des PNJs en vente, par ordre alphabétique"""
        ret = []
        liste_cles = sorted([p.cle for p in self._p_prototypes.keys()])
        for cle in liste_cles:
            ret.append(self.get_item_par_cle(cle))
        return ret
    
    def est_en_vente(self, objet):
        """Retourne True si la clé correspond à un objet en vente,
        False sinon.
        
        """
        return objet in [o.cle for o in self._o_prototypes.keys()]
    
    def encaisser(self, calcul):
        """Modifie la valeur de la caisse en fonction d'une chaîne de calcul"""
        self.caisse = eval(self.caisse + calcul)
    
    def get_item_par_id(self, id):
        """Retourne un objet en fonction de son id (voir self.afficher)"""
        liste_items = self.liste_objets + self.liste_pnjs
        try:
            objet = liste_items[id - 1]
        except IndexError:
            return None
        else:
            return objet
    
    def get_item_par_cle(self, cle):
        """Retourne un objet en fonction de sa clé"""
        liste_items = self.liste_objets + self.liste_pnjs
        for it in liste_items:
            if it.cle == cle:
                return it
        return None
    
    def afficher(self):
        """Affichage du magasin en jeu"""
        ret = self.nom + "\n\n"
        liste_obj = []
        liste_pnj = []
        taille_max = 0
        for o in self._o_prototypes.keys():
            if len(o.nom_singulier) > taille_max:
                taille_max = len(o.nom_singulier) + 1
        for p in self._p_prototypes.keys():
            if len(p.nom_singulier) > taille_max:
                taille_max = len(p.nom_singulier) + 1
        taille_max = taille_max >= 6 and taille_max or 6
        id = 1
        for o, nb in self._o_prototypes.items():
            liste_obj.append(("#" + str(id)).rjust(3) + " | " + \
                    o.nom_singulier.ljust(taille_max) + "|" + \
                    str(o.prix).rjust(5) + " |" + str(nb).rjust(5) + " |\n")
            id += 1
        for p, nb in self._p_prototypes.items():
            liste_pnj.append(("#" + str(id)).rjust(3) + " | " + \
                    p.nom_singulier.ljust(taille_max) + "|" + \
                    str(p.prix).rjust(5) + " |" + str(nb).rjust(5) + " |\n")
            id += 1
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
