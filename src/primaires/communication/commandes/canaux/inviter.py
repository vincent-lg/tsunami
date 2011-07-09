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


"""Fichier contenant le paramètre 'inviter' de la commande 'canaux'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.communication.contextes.invitation import Invitation

class PrmInviter(Parametre):
    
    """Commande 'canaux inviter <canal> <joueur>'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "inviter", "invite")
        self.schema = "<canal> <nom_joueur>"
        self.aide_courte = "invite un joueur dans un canal"
        self.aide_longue = \
            "En précisant un canal et un joueur, vous pouvez envoyer à ce " \
            "joueur une invitation à rejoindre ce canal."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        if not dic_masques["canal"].canal_existe:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
        else:
            canal = dic_masques["canal"].canal
            joueur = dic_masques["nom_joueur"].joueur
            if not personnage in canal.connectes:
                personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            elif joueur in canal.connectes:
                personnage << "|err|Ce joueur est déjà connecté au canal " \
                        "{}.|ff|".format(canal.nom)
            elif joueur not in type(self).importeur.connex.joueurs_connectes:
                personnage << "|err|Ce joueur n'est pas connecté.|ff|"
            else:
                contexte = Invitation(joueur.instance_connexion)
                contexte.emetteur = personnage
                contexte.canal = canal
                contexte.actualiser()
                personnage << "|att|Vous venez d'inviter {} à rejoindre le " \
                        "canal {}.|ff|".format(joueur.nom, canal.nom)
