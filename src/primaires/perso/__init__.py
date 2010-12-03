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


"""Fichier contenant le module primaire perso."""

from abstraits.module import *
from primaires.interpreteur.commande.commande import Commande
from primaires.perso.masques.personne import MasquePersonne
from primaires.interpreteur.masque.parametre import Parametre

class Module(BaseModule):
    """Module gérant la classe Personnage qui sera héritée pour construire
    des joueurs et NPCs. Les mécanismes propres au personnage (c'est-à-dire
    indépendant de la connexion et liées à l'univers) seront gérées ici.
    
    En revanche, les contextes de connexion ou de création d'un personnage
    ne se trouve pas ici (il s'agit d'informations propres à un joueur, non
    à un NPC.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "perso", "primaire")
    
    def init(self):
        """Initialisation du module"""
        self.importeur.interpreteur.ajouter_masque(MasquePersonne())
        commande = Commande("regarder", "look")
        parametre = Parametre("depuis", "from")
        commande.ajouter_parametre(parametre)
        schema = "<personne> depuis (<personne> (<personne>))"
        self.importeur.interpreteur.ajouter_commande(commande, schema)
        commande = Commande("regarder", "look")
        parametre = Parametre("depuis", "from")
        commande.ajouter_parametre(parametre)
        schema = "depuis (<personne> (<personne>))"
        self.importeur.interpreteur.ajouter_commande(commande, schema)
