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

class Magasin(BaseObj):
    
    """Cette classe représente un magasin.
    
    """
    
    def __init__(self, nom, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.vendeur = None
        self.monnaies = []
        self.caisse = 0
        self._o_prototypes = {}
        self._p_prototypes = {}
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        """Affichage du magasin"""
        liste_obj = []
        for o, nb in self._o_prototypes.items():
            liste_obj.append(o.nom_singulier + ", " + str(nb))
        liste_obj = sorted(liste_obj)
        liste_pnj = []
        for p, nb in self._p_prototypes.items():
            liste_pnj.append(p.nom_singulier + ", " + str(nb))
        liste_pnj = sorted(liste_pnj)
        ret = "Objets :\n  " if liste_obj else ""
        ret += "\n  ".join(liste_obj)
        ret += "PNJs :\\n  " if liste_pnj else ""
        ret += "\n  ".join(liste_pnj)
        if not ret:
            ret = "|att|Aucun objet en vente.|ff|"
        return ret
    
    @property
    def nom_vendeur(self):
        """Retourne le nom du vendeur"""
        return self.vendeur.cle if self.vendeur else "aucun"
    
    @property
    def liste_monnaies(self):
        """Retourne la liste des monnaies utilisables dans ce magasin"""
        ret = ", ".join([m.cle for m in self.monnaies])
        if not ret:
            ret = "aucune"
        return ret
    
    def est_en_vente(self, objet):
        """Retourne True si l'objet est en vente, false sinon"""
        return objet in [o.cle for o in self._o_prototypes.keys()]
    
    def ajouter_ou_modifier(self, objet, quantite):
        """Ajoute un objet à la liste de ceux en vente ou modifie sa quantité
        si l'objet spécifié existe.
        
        """
        proto = type(self).importeur.objet.prototypes[objet]
        self._o_prototypes[proto] = quantite
    
    def retirer(self, objet):
        """Retire un objet de la liste de ceux en vente"""
        for o in self._o_prototypes.keys():
            if o.cle == objet:
                del self._o_prototypes[o]
                break
