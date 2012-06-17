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


"""Fichier contenant l'action poser."""

from primaires.scripting.action import Action

class ClasseAction(Action):
    
    """Pose quelque chose sur le sol ou dans un conteneur."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.poser_objet, "Salle", "Objet")
        cls.ajouter_types(cls.poser_objet_conteneur, "Objet", "Objet")
        cls.ajouter_types(cls.poser_proto_nb, "Salle", "str", "Fraction")
        cls.ajouter_types(cls.poser_proto_nb_conteneur, "Objet", "str",
                "Fraction")
    
    @staticmethod
    def poser_objet(salle, objet):
        """Pose l'objet sur le sol de la salle."""
        salle.objets_sol.ajouter(objet)
    
    @staticmethod
    def poser_objet_conteneur(conteneur, objet):
        """Pose l'objet dans le conteneur (pas conteneur de nourriture).
        
        Attention, l'objet conteneur ne peut en aucun cas être "flottant" mais
        doit lui-même être contenu quelque part (sol d'une salle, inventaire
        d'un personnage, autre conteneur...).
        
        """
        if not conteneur.est_de_type("conteneur"):
            raise ErreurExecution("{} n'est pas un conteneur".format(
                    conteneur.get_nom()))
        if not conteneur.contenu:
            raise ErreurExecution("{} n'est contenu nul part".format(
                    conteneur.get_nom()))
        conteneur.conteneur.ajouter(objet)
    
    @staticmethod
    def poser_proto_nb(salle, prototype, nb):
        """Pose sur le sol de la salle nb objets du prototype précisé."""
        nb = int(nb)
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        prototype = importeur.objet.prototypes[prototype]
        for i in range(nb):
            objet = importeur.objet.creer_objet(prototype)
            salle.objets_sol.ajouter(objet)
    
    @staticmethod
    def poser_proto_nb_conteneur(conteneur, prototype, nb):
        """Pose dans le conteneur nb objets du prototype précisé.
        
        Attention, l'objet conteneur ne peut en aucun cas être "flottant" mais
        doit lui-même être contenu quelque part (sol d'une salle, inventaire
        d'un personnage, autre conteneur...). Il ne doit pas en outre être
        un conteneur de nourriture.
        
        """
        nb = int(nb)
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        prototype = importeur.objet.prototypes[prototype]
        if not conteneur.est_de_type("conteneur"):
            raise ErreurExecution("{} n'est pas un conteneur".format(
                    conteneur.get_nom()))
        if not conteneur.contenu:
            raise ErreurExecution("{} n'est contenu nul part".format(
                    conteneur.get_nom()))
        for i in range(nb):
            objet = importeur.objet.creer_objet(prototype)
            conteneur.conteneur.ajouter(objet)
