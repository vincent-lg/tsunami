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


"""Fichier contenant le paramètre 'lister' de la commande 'canaux'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.communication.canal import INVISIBLE, PRIVE, BLOQUE

class PrmLister(Parametre):
    
    """Commande 'canaux lister'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lister", "list")
        self.schema = ""
        self.aide_courte = "liste les canaux existants"
        self.aide_longue = \
            "Cette sous-commande offre une liste des canaux existants, " \
            "accompagnée d'une courte aide pour chacun d'eux."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        tous_canaux = type(self).importeur.communication.canaux
        canaux = []
        for canal in tous_canaux.iter().values():
            if personnage in canal.connectes:
                if not canal.flags & BLOQUE:
                    canaux.append(canal)
            else:
                if not canal.flags & INVISIBLE and not canal.flags & PRIVE:
                    canaux.append(canal)
        if not canaux:
            res = "|err|Il n'y a aucun canal de communication.|ff|"
        else:
            # On détermine la taille du tableau
            taille = 0
            for canal in canaux:
                if len(canal.infos) > taille:
                    taille = len(canal.infos)
            res = "+" + "-" * (taille - 9) + "+\n"
            res += "| |tit|" + "Canaux existants".ljust(taille - 11) + "|ff| |\n"
            res += "+" + "-" * (taille - 9) + "+\n"
            for canal in canaux:
                if personnage in canal.connectes:
                    res += "| |bc|* " + canal.infos.ljust(taille) + "|ff| |\n"
                else:
                    res += "| |cmd|" + canal.infos.ljust(taille + 2) + "|ff| |\n"
            res += "+" + "-" * (taille - 9) + "+"
            res += \
                "\n|cmd|canal|ff| : résumé (|rgc|nombre de connectés|ff|)\n" \
                "Les canaux auxquels vous êtes connecté apparaissent en " \
                "|bc|blanc|ff| et\nprécédés du signe |bc|*|ff|."
        
        personnage << res
