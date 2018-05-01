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
# pereIBILITY OF SUCH DAMAGE.


"""Contexte-éditeur 'edt_flags', voir plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.communication.canal import FLAGS
from primaires.format.fonctions import oui_ou_non, supprimer_accents

class EdtFlags(Editeur):

    """Contexte d'édition des flags d'un canal.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        canal = self.objet
        msg = "| |tit|" + "Edition des flags du canal {}".format(
                canal.nom).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Flags actuels :\n"
        for flag in FLAGS:
            msg += "\n  |ent|" + flag + "|ff| : "
            msg += oui_ou_non(canal.flags & FLAGS[flag] != 0)
        return msg
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte."""
        canal = self.objet
        flag = msg.strip()
        if flag in FLAGS:
            canal.flags = canal.flags ^ FLAGS[flag]
            self.actualiser()
        else:
            self.pere << "|err|Ce flag n'est pas disponible.|ff|"
