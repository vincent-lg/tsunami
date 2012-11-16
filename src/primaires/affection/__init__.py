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


"""Ce fichier contient le module primaire affection."""

from abstraits.module import *
from . import defaut

class Module(BaseModule):
    
    """Classe représentant le module 'affection'.
    
    Ce module gère les affections, c'est-à-dire ce qui affecte
    temporairement une salle, un personnage ou un objet. Différentes
    classes sont créées pour ces différents cas.
    
    Les affections peuvent à la fois être créées par le système ou
    par les bâtisseurs. Les affections que créent le système ne peuvent
    pas être retirées et sont souvent appelées lors d'évènement contenus
    dans le code-même. Les affections créées par les bâtisseurs
    doivent être appelées au cas par cas (grâce au scripting).
    
    Voici le plan des principales classes du module :
        Affection -- une affection concrète générique
        AffectionAbstraite -- une affection abstraite
        AffectionPersonnage -- une affection propre aux personnages
        AffectionSalle -- une affection de salle
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "affection", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger("affection", \
                "affections")
        self.aff_salles = {}
        self.aff_personnages = {}
    
    def preparer(self):
        """Prépare le module.
        
        Crée les affections par défaut si elles n'existent pas.
        
        """
        aff_salles = {
            "neige": defaut.salle.neige.Neige,
        }
        aff_personnages = {
            "alcool": defaut.personnage.alcool.Alcool,
        }
        
        for cle, classe in aff_salles.items():
            if cle not in self.aff_salles:
                classe() # crée (et enregistre automatiquement) l'affection
        
        for cle, classe in aff_personnages.items():
            if cle not in self.aff_personnages:
                classe() # crée (et enregistre automatiquement) l'affection
    
    def get_affection(self, type, cle):
        """Retourne, si trouvé, l'objet représentant l'affection."""
        types = {
            "personnage": self.aff_personnages,
            "salle": self.aff_salles,
        }
        
        affections = types[type]
        return affections[cle]
