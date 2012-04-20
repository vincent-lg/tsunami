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


"""Fichier contenant le paramètre 'nettoyer' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmNettoyer(Parametre):
    
    """Commande 'rapport nettoyer'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "nettoyer", "clean")
        self.schema = ""
        self.groupe = "administrateur"
        self.aide_courte = "supprime tous les rapports fermés"
        self.aide_longue = \
            "Cette commande nettoie la liste des rapports en supprimant " \
            "définitivement tous ceux qui sont fermés."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nb_sup = 0
        for rapport in list(importeur.rapport.rapports.values()):
            if not rapport.ouvert:
                importeur.rapport.rapports[rapport.id].detruire()
                del importeur.rapport.rapports[rapport.id]
                nb_sup += 1
        if not nb_sup:
            personnage << "|err|Tous les rapports de la liste sont " \
                    "ouverts ; aucune suppression.|ff|"
        else:
            s = "s" if nb_sup > 1 else ""
            personnage << "|att|{nb} rapport{s} supprimé{s}.|ff|".format(
                    nb=nb_sup, s=s)
