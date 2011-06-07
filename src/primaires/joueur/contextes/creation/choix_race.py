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
# pereIBILITY OF SUCH DAMAGE.


"""Fichier contenant le contexte "personnage:creation:choix_race"""

from primaires.interpreteur.contexte import Contexte
from primaires.format.fonctions import *

class ChoixRace(Contexte):
    """Contexte demandant au client de choisir la race de son personnage.
    
    """
    nom = "personnage:creation:choix_race"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        races = type(self).importeur.perso.races
        noms_races = [race.nom for race in races]
        return \
            "\n|tit|-------= Choix de la race =-------|ff|\n\n" \
            "Entrez l'une des |ent|races|ff| proposées ci-après\n" \
            "ou |cmd|info <nom de la race>|ff| pour obtenir plus " \
            "des informations sur la race.\nExemple : |cmd|info " \
            "humain|ff|\n\nRaces disponibles :\n\n" \
            "  " + "\n  ".join(noms_races)
    
    def get_prompt(self):
        """Message de prompt"""
        return "Entrez le nom de la race : "
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        msg = supprimer_accents(msg).lower()
        race = None
        for t_race in type(self).importeur.perso.races:
            if contient(t_race.nom, msg):
                race = t_race
                break

        if not race:
            self.pere << "|err|Cette race n'est pas disponible.|ff|"
        else:
            self.pere.joueur.race = race
            
            if self.pere.joueur not in self.pere.compte.joueurs:
                print("On ajoute")
                self.pere.compte.ajouter_joueur(self.pere.joueur)
            
            self.pere.joueur.pre_connecter()

