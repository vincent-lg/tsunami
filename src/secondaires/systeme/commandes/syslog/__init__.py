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


"""Package contenant la commande 'syslog'"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import echapper_accolades

class CmdSyslog(Commande):

    """Commande 'syslog'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "syslog", "syslog")
        self.groupe = "administrateur"
        self.aide_courte = "affiche les derniers messages systèmes"
        self.aide_longue = \
            "Cette commande permet d'afficher les derniers messages " \
            "reçus par le système. Notez que ces systèmes sont ceux " \
            "transitant par le système de log interne à Kassie (man_log). " \
            "Les messages affichés à la console d'une autre façon ne " \
            "seront pas visibles grâce à cette commande."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        messages = type(self).importeur.man_logs.messages
        messages = messages[-20:]
        msg = "\n".join([m.message for m in messages])
        msg = echapper_accolades(msg)
        personnage << msg
