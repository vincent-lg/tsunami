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


"""Fichier contenant le type à manger."""

from primaires.objet.editeurs.generique.edt_cle import EdtCle
from .base import BaseType

class AManger(BaseType):
    
    """Type d'objet: à manger.
    
    """
    
    nom_type = "à manger"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.conteneur_nourriture = None
        self.nourriture_contenue = None
        self.etendre_editeur("r", "conteneur de nourriture", EdtCle, self,
                "conteneur_nourriture", "conteneur de nourriture")
        self.etendre_editeur("ue", "nourriture contenue", EdtCle, self,
                "nourriture_contenue", "nourriture")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        conteneur = enveloppes["r"]
        conteneur.prompt = "Clé du conteneur de nourriture : "
        conteneur.aide_courte = \
            "Entrez la |ent|clé du conteneur de nourriture|ff| lié " \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente."
        
        contenu = enveloppes["ue"]
        contenu.prompt = "Clé de la nourriture contenue : "
        contenu.aide_courte = \
            "Entrez la |ent|clé de la nourriture contenue|ff| " \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente."
    
    def _get_nom_singulier(self):
        """Retourne le nom singulier de l'objet en devenir."""
        if self.conteneur_nourriture:
            nom = self.conteneur_nourriture.nom_singulier
            if self.conteneur_nourriture.statuts:
                nom += " " + self.conteneur_nourriture.statuts[-1][1]
        else:
            nom = "encore inconnu"
        
        return nom
    def _set_nom_singulier(self, nom_singulier):
        """Ne fait rien."""
        pass
    nom_singulier = property(_get_nom_singulier, _set_nom_singulier)
    def _get_nom_pluriel(self):
        """Retourne le nom pluriel de l'objet en devenir."""
        if self.conteneur_nourriture:
            nom = self.conteneur_nourriture.nom_pluriel
            if self.conteneur_nourriture.statuts:
                nom += " " + self.conteneur_nourriture.statuts[-1][1]
        else:
            nom = "encore inconnu"
        
        return nom
    def _set_nom_pluriel(self, nom_pluriel):
        """Ne fait rien."""
        pass
    nom_pluriel = property(_get_nom_pluriel, _set_nom_pluriel)
    
    def acheter(self, quantite, magasin, transaction):
        """Achète les objets dans la quantité spécifiée."""
        salle = magasin.parent
        if self.conteneur_nourriture is None:
            raise ValueError("aucun conteneur de nourriture n'a été spécifié " \
                    "pour '{}'".format(self.cle))
        if self.nourriture_contenue is None:
            raise ValueError("aucune nourriture contenue n'a été spécifiée " \
                    "pour '{}'".format(self.cle))
        for i in range(quantite):
            objet = importeur.objet.creer_objet(self.conteneur_nourriture)
            nourriture = importeur.objet.creer_objet(self.nourriture_contenue)
            objet.nourriture = [nourriture]
            salle.objets_sol.ajouter(objet)
