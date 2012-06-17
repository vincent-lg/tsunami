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


"""Fichier contenant la fonction peut_prendre."""

from primaires.scripting.fonction import Fonction
from primaires.objet.conteneur import SurPoids

class ClasseFonction(Fonction):
    
    """Teste si le conteneur a de la place."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.peut_contenir_objet, "Objet", "Objet")
        cls.ajouter_types(cls.peut_contenir_proto, "Objet", "str", "Fraction")
    
    @staticmethod
    def peut_contenir_objet(conteneur, objet):
        """Renvoie vrai si le conteneur peut contenir l'objet, faux sinon.
        
        L'objet testé doit être une variable de type Objet.
        
        """
        if conteneur.est_de_type("conteneur de nourriture"):
            if sum(o.poids_unitaire for o in conteneur.nourriture) \
                    + objet.poids_unitaire > conteneur.poids_max:
                return False
            else:
                return True
        try:
            conteneur.conteneur.supporter_poids_sup(objet.poids_unitaire,
                    recursif=False)
            assert conteneur.est_de_type("conteneur")
            assert conteneur.accepte_type(objet)
        except (AssertionError, SurPoids):
            return False
        else:
            return True
    
    @staticmethod
    def peut_contenir_proto(conteneur, prototype, nb):
        """Renvoie vrai si le conteneur peut contenir nb objets, faux sinon.
        
        Cet usage permet de tester à partir d'un objet non encore créé, et
        surtout de tester une quantité. Le conteneur, lui, doit être une
        variable de type Objet.
        
        """
        nb = int(nb)
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        prototype = importeur.objet.prototypes[prototype]
        if conteneur.est_de_type("conteneur de nourriture"):
            if sum(o.poids_unitaire for o in conteneur.nourriture) \
                    + prototype.poids_unitaire * nb > conteneur.poids_max:
                return False
            else:
                return True
        try:
            conteneur.conteneur.supporter_poids_sup(
                    prototype.poids_unitaire * nb, recursif=False)
            assert conteneur.est_de_type("conteneur")
            assert conteneur.accepte_type(prototype)
        except (AssertionError, SurPoids):
            return False
        else:
            return True
