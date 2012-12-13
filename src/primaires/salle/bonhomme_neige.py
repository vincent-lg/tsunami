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

"""Ce fichier contient différentes classes :

BonhommeNeige -- un bonhomme de neige concret
PrototypeBonhommeNeige -- un prototype de bonhomme de neige
Etat -- un état de prototype
Element -- un élément de l'habillement du bonhomme de neige

"""

from collections import OrderedDict

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents
from .decor import *

class BonhommeNeige(Decor):
    
    """Cette classe représente un bonhomme de neige concret.
    
    Les bonhommes de neige sont des décors, ils apparaissent
    dans la description d'une salle et peuvent êre regardés.
    
    """
    
    def __init__(self, prototype, parent=None):
        """Constructeur de la classe"""
        Decor.__init__(self, prototype, parent)
        self.etat = -1
        self.createur = None
        self.elements = {}
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        return "<bonhomme de neige {} (état={}) en {}>".format(
                self.cle_prototype, self.etat, self.parent)
    
    @property
    def complet(self):
        """Retourne True si le bonhomme est complet, False sinon."""
        if self.etat == -1:
            return True
        
        return self.etat == len(self.prototype.etats) - 1
    
    def get_nom(self, nombre=1):
        return self.prototype.get_nom(self.etat, nombre)
    
    def get_nom_etat(self, nombre=1):
        return self.prototype.get_nom_etat(self.etat, nombre)
    
    def regarder(self, personnage):
        """Le personnage regarde self."""
        ret = "Vous regardez {} :\n\n".format(self.get_nom())
        ret += self.prototype.get_description(self.etat).regarder(
                personnage, self)
        if self.elements:
            ret += "\n"
        
        for nom in self.prototype.elements:
            objet = self.elements.get(nom)
            if objet:
                ret += "\n" + nom.capitalize().ljust(20)
                ret += " : " + objet.get_nom()
        
        personnage << ret
        personnage.salle.envoyer("{{}} regarde {}.".format(self.get_nom()),
                personnage)

class PrototypeBonhommeNeige(PrototypeDecor):
    
    """Classe représentant un prototype de bonhomme de neige.
    
    Les informations comme le nom ou la description se trouvent
    dans le prototype. La classe BonhommeNeige (définie au-dessus) est une
    concrétisation du prototype dans une salle.
    
    """
    
    def __init__(self, cle):
        PrototypeDecor.__init__(self, cle)
        del self.nom_pluriel
        del self.etat_singulier
        del self.etat_pluriel
        del self.description
        self.nom = "bonhomme"
        self.utilisable_joueurs = True
        self.etats = [Etat(self)]
        self.elements = OrderedDict()
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def _get_nom_singulier(self):
        """Retourne le nom singulier du dernier état."""
        return self.etats[-1].nom_singulier
    def _set_nom_singulier(self, nom):
        pass
    nom_singulier = property(_get_nom_singulier, _set_nom_singulier)
    
    @property
    def str_etats(self):
        """Retourne la chaîne des états possibles."""
        chaine = "\n  " + "\n  ".join(e.nom_singulier for e in self.etats)
        return chaine
    
    @property
    def str_elements(self):
        """Retourne la chaîne des éléments existants."""
        if not self.elements:
            return "aucun"
        
        return "\n  " + "\n  ".join(self.elements.keys())
    
    def get_nom(self, etat, nombre):
        """Retourne le nom singulier ou pluriel."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))
        
        etat = self.etats[etat]
        if nombre == 1:
            return etat.nom_singulier
        else:
            nombre = get_nom_nombre(nombre)
            return nombre + " " + etat.nom_pluriel
    
    def get_nom_etat(self, etat, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))
        
        d_etat = self.etats[etat]
        if nombre == 1:
            return self.get_nom(etat, 1) + " " + d_etat.etat_singulier
        else:
            return self.get_nom(etat, nombre) + " " + d_etat.etat_pluriel
    
    def get_description(self, etat):
        """Retourne la description correspondante à l'état."""
        return self.etats[etat].description
    
    def get_etat(self, nom):
        """Retourne, si trouvé, l'état du nom indiqué.
        
        Si l'état n'est pas trouvé, retourne None.
        
        La recherche se fait sans tenir compte de la casse ou des
        accents.
        
        """
        nom = supprimer_accents(nom).lower()
        for etat in self.etats:
            if supprimer_accents(etat.nom_singulier).lower() == nom:
                return etat
        
        return None
    
    def ajouter_etat(self, nom_singulier):
        """Ajoute un nouvel état."""
        etat = Etat(self)
        etat.nom_singulier = nom_singulier
        self.etats.append(etat)
        return etat
    
    def supprimer_etat(self, indice):
        """Supprime un état."""
        del self.etats[indice]
    
    def get_element(self, nom):
        """Retourne, si trouvé, l'élément du nom indiqué.
        
        Si l'élément n'est pas trouvé, retourne None.
        
        La recherche se fait sans tenir compte de la casse ou des
        accents.
        
        """
        nom = supprimer_accents(nom).lower()
        for t_nom, element in self.elements.items():
            if supprimer_accents(t_nom).lower() == nom:
                return element
        
        return None
    
    def ajouter_element(self, nom):
        """Ajoute un élément."""
        element = Element(self, nom)
        self.elements[nom] = element
    
    def supprimer_element(self, nom):
        """Supprime un élément."""
        del self.elements[nom]


class Etat(BaseObj):
    
    """Classe représentant un état possible d'un prototype de bonhomme de neige.
    
    C'est dans cette classe qu'on trouve réellement les
    informations nom_singulier, nom_pluriel, etat_singulier,
    etat_pluriel et description.
    
    """
    
    def __init__(self, prototype):
        BaseObj.__init__(self)
        self.nom_singulier = "un bonhomme de neige"
        self.nom_pluriel = "bonhommes de neige"
        self.etat_singulier = "se tient ici"
        self.etat_pluriel = "se tiennent ici"
        self.description = Description(parent=self, scriptable=False)
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        return "<état {}>".format(self.nom_singulier)
    
    def __str__(self):
        return self.nom_singulier


class Element(BaseObj):
    
    """Classe représentant un élément habillable du bonhomme de neige.
    
    Par exemple, on pourrait vouloir mettre un bonnet sur la
    tête d'un bonhomme de neige. Cet habillement est propre
    à un prototype de bonhomme de neige.
    
    """
    
    def __init__(self, prototype, nom):
        BaseObj.__init__(self)
        self.prototype = prototype
        self.nom = nom
        self.objets_admis = []
        self.types_admis = []
        self.etat_min = 0
        self.connecteur = "sur"
        self.masculin = True
    
    def __getnewargs__(self):
        return (None, "aucun")
    
    def __repr__(self):
        return "<élément {}>".format(self.nom)
    
    def __str__(self):
        return self.nom
    
    @property
    def str_types_admis(self):
        """Retourne les noms en une chaîne des types admis."""
        if not self.types_admis:
            return "Aucun"
        
        return ", ".join(self.types_admis)
    
    @property
    def str_objets_admis(self):
        """Retourne les cléss en une chaîne des objets admis."""
        if not self.objets_admis:
            return "Aucun"
        
        return ", ".join(self.objets_admis)
    
    @property
    def article(self):
        """Retourne l'article."""
        if self.masculin:
            return "le"
        else:
            return "la"
    
    @property
    def nom_complet(self):
        """Retourne le nom complet."""
        nom = self.nom
        article = self.article
        if nom.startswith("aeiouyh"):
            return "l'" + nom
        
        return article + " " + nom
    
    def ajouter_ou_retirer_type_admis(self, nom):
        """Ajoute ou retire un type admis."""
        if nom in self.types_admis:
            self.types_admis.remove(nom)
        else:
            self.types_admis.append(nom)
    
    def ajouter_ou_retirer_objet_admis(self, cle):
        """Ajoute ou retire un objet admis."""
        if cle in self.objets_admis:
            self.objets_admis.remove(cle)
        else:
            self.objets_admis.append(cle)
