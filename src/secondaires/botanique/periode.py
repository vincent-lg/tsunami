# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient la classe Periode, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.aleatoire import varier
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents
from .element import Element

class Periode(BaseObj):
    
    """Classe décrivant une période de temps (cycle pour une plante).
    
    Une période possède :
    plante -- le prototype de plante définissant la période
    nom -- le nom de la période
    nom_singulier, nom_pluriel -- les noms définis pour cettte période
    description -- la description du végétal à cette période
    fin -- un tuple (jour, mois) représentant la fin du cycle
    variation -- un nombre de jours représentant la variation aléatoire [1]
    elements -- une liste représentant les éléments récoltables
                à cette période [2]
    
    [1] La première période présente dans la liste d'un prototype est
        toujours choisie au début de l'année. Si plus d'une période
        est définie, la première étape laisse la place à la suivante
        au jour précisé plus ou moins la variation optionnelle.
        Cela permet d'introduire une donnée aléatoire faisant
        qu'un plan de maïs pourra être récoltable dans des dates
        approximatives. Notez qu'après la dernière étape définie,
        la plante revient en étape 0 (la première).
    
    [2] La liste des éléments est constituée d'objets Element (voir
        la classe définie dans .element.py).
    
    """
    
    def __init__(self, nom, cycle):
        """Constructeur de la période."""
        BaseObj.__init__(self)
        self.nom = nom
        self.cycle = cycle
        self.nom_singulier = "une plante"
        self.nom_pluriel = "plantes"
        self.description = Description(parent=self)
        self.fin = (0, 0)
        self.variation = 0
        self.elements = []
    
    def __getnewargs__(self):
        return ("", None)
    
    def __repr__(self):
        return "<période {} ({}-{} variation={})>".format(self.nom,
                self.fin[0] + 1, self.fin[1] + 1, self.variation)
    
    def __str__(self):
        return self.nom
    
    @property
    def date_fin(self):
        """Retourne la date de fin grâce aux informations du module temps."""
        return "{} du {}".format(importeur.temps.cfg.noms_jours[ \
                self.fin[0]], importeur.temps.cfg.mois[self.fin[1]][0])
    
    @property
    def plante(self):
        return self.cycle and self.cycle.plante or None
    
    @property
    def periode_suivante(self):
        """Retourne, si trouvée, la période suivante.
        
        Si aucune période ne vient après, retourne self.
        Si la période présente ne peut être trouvée dans le cycle, lève une
        exception IndexError.
        
        """
        indice = self.cycle.periodes.index(self)
        if indice == -1:
            raise IndexError("période introuvable {} dans la plante {}".format(
                    self, self.plante))
        
        try:
            return self.cycle.periodes[indice + 1]
        except IndexError:
            return self
    
    @property
    def finie(self):
        """Retourne true si la période est finie, False sinon."""
        tps = importeur.temps.temps
        jour = tps.jour
        mois = tps.mois
        t_j, t_m = self.fin
        t_j += varier(t_j, self.variation, min=None)
        if t_j < 0:
            t_m -= t_j // 30
            t_j = t_j % 30
        
        if mois > t_m:
            return True
        elif mois == t_m and jour > t_j:
            return True
        return False
    
    def get_nom(self, nombre=1):
        """Retourne le nom singulier ou pluriel en fonction du nombre."""
        if nombre == 1:
            return self.nom_singulier
        
        return str(nombre) + " " + self.nom_pluriel
    
    def ajouter_element(self, nom, objet, quantite):
        """Ajout d'un élément.
        
        Si on cherche à ajouter un élément existant (l'objet est défini
        dans un autre élément), une exception ValueError est levée.
        
        """
        sa_nom = supprimer_accents(nom).lower()
        for elt in self.elements:
            if elt.objet is objet or supprimer_accents(elt.nom) == sa_nom:
                raise ValueError("l'élément {} existe déjà".format(elt))
        
        elt = Element(self.plante, self, nom.lower(), objet, quantite)
        self.elements.append(elt)
        return elt
    
    def get_element(self, nom):
        """Retourne l'élément portant ce nom
        
        La recherche n'est pas sensible aux majuscules / minuscules
        ou aux accents.
        
        """
        nom = supprimer_accents(nom).lower()
        for elt in self.elements:
            if elt.nom == nom:
                return elt
        
        raise ValueError("le nom d'élément {} est introuvable".format(nom))
    
    def get_element_depuis_objet(self, objet):
        """Retourne l'élément associé à l'objet."""
        for elt in self.elements:
            if elt.objet is objet:
                return elt
        
        raise ValueError("aucun élément ne correspond à l'objet {}".Format(
                objet.cle))
    
    def est_element(self, nom):
        """Retourne True si l'élément existe, False sinon."""
        try:
            return bool(self.get_element(nom))
        except KeyError:
            return False
    
    def supprimer_element(self, nom):
        """Supprime l'élément."""
        nom = supprimer_accents(nom).lower()
        for elt in list(self.elements):
            if elt.nom == nom:
                self.elements.remove(elt)
                elt.detruire()
                return
        
        raise ValueError("aucun élément ne porte le nom {}".format(nom))
    
    def detruire(self):
        """Destruction de la période."""
        for elt in self.elements:
            elt.detruire()
        
        BaseObj.detruire(self)
