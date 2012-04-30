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


"""Fichier contenant le type ConteneurNourriture."""

from math import ceil

from primaires.interpreteur.editeur.entier import Entier
from bases.objet.attribut import Attribut
from .base import BaseType

class ConteneurNourriture(BaseType):
    
    """Type d'objet: conteneur de nourriture.
    
    Les conteneurs de nourriture sont des conteneurs spéciaux genre assiette,
    bol, écuelle...
    
    """
    
    nom_type = "conteneur de nourriture"
    nettoyer = False
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.statuts = [
            (5, "à moitié plein"),
            (10, "rempli"),
        ]
        self.poids_max = 10
        self.etendre_editeur("m", "poids maximum", Entier, self,
                "poids_max", 1)
        
        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "nourriture": Attribut(list),
        }
            
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes."""
        poids_max = enveloppes["m"]
        poids_max.apercu = "{objet.poids_max}"
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| que peut contenir cet objet " \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max}"
    
    @property
    def nourriture_qtt(self):
        """Retourne un dictionnaire {Nourriture:quantité}."""
        dico_qtt = {}
        for item in self.nourriture:
            if item.prototype not in dico_qtt:
                dico_qtt[item.prototype] = 1
            else:
                dico_qtt[item.prototype] += 1
        return dico_qtt
    
    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        for o, nb in self.conteneur.iter_nombres():
            poids += o.poids * nb
        
        return round(poids, 3)
    
    # Actions sur les objets
    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.
        
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel
        
        """
        ajout = "vide"
        if self.nourriture:
            poids_contenu = sum([o.poids_unitaire for o in self.nourriture])
            ratio = ceil(poids_contenu / self.poids_max)
            for r, message in self.statuts:
                if ratio <= r:
                    ajout = message
                    break
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier + " " + ajout
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel + " " + ajout
    
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        
        if self.nourriture:
            nourriture = [o.get_nom(nb) for o, nb \
                    in self.nourriture_qtt.items()]
            if len(nourriture) > 1:
                ajout = ", ".join(nourriture[:-1]) + " et " + nourriture[-1]
            else:
                ajout = nourriture[0]
            msg += "\nCe récipient contient " + ajout + "."
        else:
            msg += "\nCe récipient est vide."
        
        return msg
