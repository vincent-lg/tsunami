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


"""Fichier contenant le type cible."""

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur.aes import AES
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from .base import BaseType

class Cible(BaseType):
    
    """Type d'objet: cible.
    
    """
    
    nom_type = "cible"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.elements = []
        self.etendre_editeur("l", "élémemnts de la cible", AES, self,
                "elements", "objet:cible:element",
                (("nom", "chaîne"), ("probabilité", "entier"),
                ("points", "entier")), "get_element", "ajouter_element",
                "supprimer_element", "nom_complet")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        elements = enveloppes["l"]
        elements.apercu = "{valeur}"
        elements.aide_courte = \
            "Entrez |ent|le nom d'un rang|ff| pour l'éditer ou :\n" \
            " |ent|/a <nom de l'élément à créer> / <probabilité> / <points> " \
            "|ff|\n (Exemple : |cmd|/a bras gauche / 8 / 3|ff|)\n" \
            " |ent|/s <nom de l'élément à supprimer>|ff|\n\n" \
            "La probabilité de toucher un élément est calculée en " \
            "fonciton\nde la probabilité totale de tous les éléments.\n\n" \
            "Éléments actuels de la cible :{valeur}"

    def get_element(self, nom):
        """Retourne l'élément du nom indiqué.
        
        Si l'élément ne peut être trouvé, lève une exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for element in self.elements:
            if supprimer_accents(element.nom).lower() == nom:
                return element
        
        raise ValueError("l'élément {} ne peut être trouvé".format(nom))
    
    def est_element(self, nom):
        """Retourne True si l'élément du nom indiqué est trouvé."""
        try:
            elt = self.get_element(nom)
        except ValueError:
            return False
        else:
            return True
    
    def ajouter_element(self, nom, *args, **kwargs):
        """Ajoute un élément.
        
        Le paramètre obligatoire est le nom de l'élément.
        Les paramètres supplémentaires (obligatoires ou non) sont transmis
        au constructeur de Element (voire la classe plus bas).
        
        Si le nom de l'élément est déjà utilisé, lève une exception ValueError.
        
        """
        if self.est_element(nom):
            raise ValueError("l'élément {} est déjà utilisé".format(nom))
        
        element = Element(self, nom, *args, **kwargs)
        self.elements.append(element)
        return element
    
    def supprimer_element(self, nom):
        """Supprime l'élément du nom indiqué."""
        nom = supprimer_accents(nom).lower()
        for i, element in enumerate(self.elements):
            if supprimer_accents(element.nom).lower == nom:
                del self.elements[i]
                return
        
        raise ValueError("l'élément {} ne peut être trouvé".format(nom))

class Element(BaseObj):
    
    """Classe représentant un élément de la cible.
    
    Il contient :
            nom -- le nom d'élément
            probabilite -- la probabilité de le toucher [1]
            points -- le nombre de points de l'élément
    
    [1] La probabilité totale n'est pas 100 mais la somme des probabilités
        de tous les éléments de la cible.
    
    """
    
    def __init__(self, cible, nom, probabilite=1, points=1):
        """Constructeur de l'élément."""
        BaseObj.__init__(self)
        self.cible = cible
        self.nom = nom
        self.probabilite = probabilite
        self.points = points
    
    def __getnewargs__(self):
        return (None, "inconnu", )
    
    def __repr__(self):
        return "<élément de cible {}>".format(self.nom)
    
    @property
    def nom_complet(self):
        """Retourne le nom complet."""
        return "{:25} (probabilité={}, {})".format(
                self.nom, self.probabilite_sur, self.msg_points)
    
    @property
    def msg_points(self):
        """Retourne une chaîne représentant le nombre de points."""
        points = self.points
        if points > 1:
            return "{} points".format(points)
        else:
            return "{} point".format(points)

    @property
    def probabilite_sur(self):
        """Retourne la probabilité sur la probabilité totale."""
        if getattr(self, "cible", None):
            total = sum(e.probabilite for e in self.cible.elements)
        else:
            total = "|err|inconnu|ff|"
        
        return "{} / {}".format(self.probabilite, total)

class CibleElementEdt(Presentation):

    """Classe définissant l'éditeur d'éléments."""

    nom = "objet:cible:element"

    def __init__(self, personnage, elt, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, elt, None, False)
        if personnage and elt:
            self.construire(elt)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, elt):
        """Construction de l'éditeur."""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, elt, "nom")
        nom.parent = self
        nom.prompt = "Nom de l'élément : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| de l'élément ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nNom actuel : " \
            "|bc|{valeur}|ff|"

        # Probabilité
        probabilite = self.ajouter_choix("probabilité de toucher l'élément",
                "r", Entier, elt, "probabilite")
        probabilite.parent = self
        probabilite.apercu = "{objet.probabilite_sur}"
        probabilite.prompt = "Probabilité de toucher l'élément : "
        probabilite.aide_courte = \
            "Entrez |ent|la probabilité|ff| de toucher l'élément " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Probabilité actuelle : {valeur}"
        
        # Points
        points = self.ajouter_choix("points de l'élément", "p", Entier,
                elt, "points")
        points.parent = self
        points.apercu = "{objet.msg_points}"
        points.prompt = "Points de l'élément : "
        points.aide_courte = \
            "Entrez |ent|le nombre de points|ff| de l'élément " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Points actuels : {valeur}"
