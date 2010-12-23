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


"""Fichier contenant la classe Joueur, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.perso.personnage import Personnage

class Joueur(Personnage):
    """Classe représentant un joueur, c'es-tà-dire un personnage connecté
    grâce à un client, à différencier des NPCs qui sont des personnages
    virtuels, animés par l'univers.
    
    """
    groupe = "joueurs"
    sous_rep = "joueurs"
    
    def __init__(self):
        """Constructeur du joueur"""
        Personnage.__init__(self)
        self.compte = None
        self.instance_connexion = None
    
    def _get_encodage(self):
        """Retourne l'encodage du compte"""
        return self.compte.encodage
    
    encodage = property(_get_encodage)
    
    def envoyer(self, msg):
        """On redirige sur l'envoie de l'instance de connexion."""
        self.instance_connexion.envoyer(msg)

# On ajoute le groupe à ObjetID
ObjetID.ajouter_groupe(Joueur)
