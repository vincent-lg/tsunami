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


"""Fichier contenant le contexte "personnage:creation:nouveau_nom"""

import re

from primaires.interpreteur.contexte import Contexte
from primaires.joueur.joueur import Joueur
from primaires.format.fonctions import supprimer_accents

## Constantes
# Regex
RE_NOM_VALIDE = re.compile(r"^[A-Za-z]*$")

class NouveauNom(Contexte):
    """Contexte demandant au client d'entrer le nom de son nouveau personnage.
    La validité du nom est établie par la regex 'RE_NOM_VALIDE' et par
    des données de configuration
    précisant la taille minimum du nom, et sa taille maximum.
    
    Si le nom est valide, on passe au contexte de création suivant.
    
    """
    nom = "personnage:creation:nouveau_nom"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|------= Nom de votre personnage =-----|ff|\n" \
            "Entrez un |ent|nom pour votre nouveau personnage|ff|."
    
    def get_prompt(self):
        """Message de prompt"""
        return "Nom de votre nouveau personnage : "
    
    def interpreter(self, msg):
        """méthode d'interprétation"""
        t_min = 3
        t_max = 15
        print(msg, RE_NOM_VALIDE.search(msg))
        if len(msg) < t_min or len(msg) > t_max:
            self.pere.envoyer("|err|Le nom de votre joueur doit faire entre " \
                    "{0} et {1} caractères|ff|.".format(t_min, t_max))
        elif msg in type(self).importeur.connex.nom_joueurs:
            self.pere.envoyer("|err|Ce nom de joueur est déjà utilisé. " \
                    "Choisissez-en un autre|ff|.")
        elif RE_NOM_VALIDE.search(supprimer_accents(msg)):
            nouv_joueur = Joueur()
            nouv_joueur.nom = msg
            print("Création du joueur {0}".format(nouv_joueur.nom))
            self.pere.compte.ajouter_joueur(nouv_joueur)
            self.pere.envoyer(self.accueil())
        else:
            self.pere.envoyer("|err|Ce nom est invalide. Veuillez " \
                    "réessayer|ff|.")
