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


"""Fichier contenant l'action deplacer_alea."""

from random import choice

from primaires.format.fonctions import supprimer_accents
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action

class ClasseAction(Action):
    
    """Un ppersonnage se déplace aléatoirement.
    
    Cette action demande à un personnage de se déplacer aléatoirement suivant
    des critères optionnels.
    
    """
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.deplacer_alea_personnage, "Personnage")
        cls.ajouter_types(cls.deplacer_alea_personnage_terrains, "Personnage",
                "str")
    
    @staticmethod
    def deplacer_alea_personnage(personnage):
        """Déplace aléatoirement le personnage sans aucun critères.
        
        Le personnage va choisir une direction aléatoirement autour de lui.
        Il retire cependant du calcul :
        
          * Les portes verrouillées
          * Les sorties cachées
        
        """
        # Choix de la direction
        sorties = []
        for sortie in personnage.salle.sorties:
            if sortie and not sortie.cachee and (not sortie.porte or \
                    not sortie.porte.verrouillee):
                sorties.append(sortie.nom)
        
        if not sorties:
            # Aucune sortie disponible
            return
        
        sortie = choice(sorties)
        try:
            personnage.deplacer_vers(sortie)
        except ExceptionAction:
            pass
    
    def deplacer_alea_personnage_terrains(personnage, terrains):
        """Déplace aléatoirement le personnage en fonction de terrains.
        
        On doit préciser, sous la forme d'une chaîne, le (ou les terrains,
        séparés par le signe |) qui sont autorisés pour ce personnage.
        
        Par exemple : "ville|route"
        
        Dans le cas ci-dessus, le personnage ne choisira dans la salle
        que des sorties menant à des salles de terrain ville ou route.
        De plus, sont ignorées :
        
          * Les sorties cachées
          * Les portes verrouillées.
        
        """
        # Choix des terrains
        if not terrains:
            raise ErreurExecution("aucun terrain n'est précisé")
        
        terrains = terrains.split("_b_")
        for i, terrain in enumerate(terrains):
            terrains[i] = supprimer_accents(terrain.strip())
        
        # Choix de la direction
        sorties = []
        for sortie in personnage.salle.sorties:
            if sortie and not sortie.cachee and (not sortie.porte or \
                    not sortie.porte.verrouillee) and sortie.salle_dest and \
                    supprimer_accents(sortie.salle_dest.nom_terrain) in \
                    terrains:
                sorties.append(sortie.nom)
        
        if not sorties:
            # Aucune sortie disponible
            return
        
        sortie = choice(sorties)
        try:
            personnage.deplacer_vers(sortie)
        except ExceptionAction:
            pass
