# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'rejoindre' de la commande 'canaux'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRejoindre(Parametre):
    
    """Commande 'canaux rejoindre <canal>'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "rejoindre", "join")
        self.schema = "<canal>"
        self.aide_courte = "rejoint le canal spécifié"
        self.aide_longue = \
            "Cette sous-commande vous connecte à un canal."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        if dic_masques["canal"].canal_existe:
            canal = dic_masques["canal"].canal
            if personnage in canal.connectes:
                personnage << "|err|Vous êtes déjà connecté à ce canal.|ff|"
            else:
                canal.rejoindre_ou_quitter(personnage)
        else:
            nom_canal = dic_masques["canal"].nom_canal
            canal = type(self).importeur.communication.ajouter_canal(nom_canal,
                    personnage)
            canal.rejoindre_ou_quitter(personnage)
            personnage << "|att|Le canal {} a été créé. Vous y êtes à " \
                    "présent connecté.|ff|".format(nom_canal)
