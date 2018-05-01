# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'retnom'"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import couper_phrase
from primaires.joueur.joueur import Joueur

class CmdRetnom(Commande):
    
    """Commande 'retnom'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "retnom", "remchar")
        self.groupe = "joueur"
        self.schema = "<personnage_present> comme/as <message>"
        self.aide_courte = "retient un nom d'un joueur"
        self.aide_longue = \
            "Cette commande permet de retenir un joueur. Par défaut, vous " \
            "ne voyez que la distinction anonyme de ce joueur. Si il vous " \
            "est présenté dans un contexte RP, vous pouvez le retenir et " \
            "le lier au nom qu'il vous donne grâce à cette commande. Vous " \
            "ne verrez plus, quand il fera une action (ou dans le " \
            "%regarder%), sa distinction anonyme mais le nom que vous " \
            "avez lié à cette distinction."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        joueur = dic_masques["personnage_present"].personnage
        message = dic_masques["message"].message
        if not isinstance(joueur, Joueur):
            personnage << "|err|Ce personnage n'est pas un joueur.|ff|"
            return
        
        personnage.envoyer("{{}} sera, pour vous, désormais connu sous le " \
                "nom de {}.".format(message), joueur)
        personnage.retenus[joueur] = message
