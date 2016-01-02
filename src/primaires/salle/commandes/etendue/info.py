# -*-coding:Utf-8 -*

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


"""Fichier contenant le paramètre 'info' de la commande 'étendue'."""

from textwrap import wrap

from primaires.interpreteur.masque.parametre import Parametre

class PrmInfo(Parametre):
    
    """Commande 'etendue info'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "info", "info")
        self.schema = "<cle>"
        self.aide_courte = "affiche des informations sur l'étendue"
        self.aide_longue = \
            "Affiche des informations sur l'étendue d'eau précisée " \
            "en paramètre, comme ses obstacles, côtes et liens. Les " \
            "obstacles sont des points neutres de l'étendue, pouvant " \
            "représenter des rochers, des récifs, des îlots inaccessibles. " \
            "Les côtes sont des salles liées à l'étendue (des plages, " \
            "des ports, des îles accessibles). Enfin, les liens sont " \
            "des points reliant deux étendues entre elles (une rivière " \
            "se jette dans la mer)."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        # On vérifie que cette étendue existe
        if cle not in type(self).importeur.salle.etendues.keys():
            personnage << "|err|Cette clé {} n'existe pas.|ff|".format(
                    repr(cle))
            return
        
        etendue = type(self).importeur.salle.etendues[cle]
        msg = "Information sur l'étendue {} :\n\n".format(cle)
        msg += "  Altitude de l'étendue : {}\n".format(etendue.altitude)
        msg += "  Profondeur moyenne de l'étendue : {}\n".format(
                etendue.profondeur)
        msg += "  Obstacles :\n"
        obstacles = " ".join("{1}.{2} ({0})".format(point.nom, *o) \
                for o, point in etendue.obstacles.items())
        obstacles = obstacles or "Aucun"
        msg += "    " + "\n    ".join(wrap(obstacles))
        msg += "\n  Côtes :\n"
        cotes = ", ".join(s.ident for s in etendue.cotes.values())
        cotes = cotes or "Aucune"
        msg += "    " + "\n    ".join(wrap(cotes))
        msg += "\n  Liens :\n"
        liens = ", ".join("{}.{} ({cle})".format(*p, cle=e.cle) for p, e in \
                etendue.liens.items())
        liens = liens or "Aucun"
        msg += "    " + "\n    ".join(wrap(liens))
        
        personnage << msg
