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


import re

"""Package contenant le paramètre 'supprimer' de la commande 'route'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmSupprimer(Parametre):

    """Commande 'route supprimer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "supprimer", "del")
        self.schema = "<texte_libre>"
        self.aide_courte = "supprime une ou plusieurs routes"
        self.aide_longue = \
            "Cette commande permet de supprimer une ou plusieurs " \
            "routes. La syntaxe pour supprimer une route est de " \
            "préciser sa salle d'origine et de destination, comme " \
            "%route% %route:supprimer%|cmd| depart:1 depart:12|ff|. " \
            "Un signe astérisque (*) au début ou à la fin du paramètre " \
            "étend la recherche à toutes les salles dont la destination " \
            "ou l'origine est celle indiquée. Par exemple %route% " \
            "%route:supprimer%|cmd| picte:5*|ff|."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        texte = re.escape(dic_masques["texte_libre"].texte)
        texte = "^" + texte.replace("\\*", ".*") + "$"
        print(texte)
        regex = re.compile(texte)
        routes = list(importeur.route.routes.values())
        supprimer = []
        for route in routes:
            identifiant = str(route.origine)
            if route.destination:
                identifiant += " " + str(route.destination)
            
            print(identifiant)
            if regex.search(identifiant):
                supprimer.append(route)
        
        if supprimer:
            s = "s" if len(supprimer) > 1 else ""
            for route in supprimer:
                importeur.route.supprimer_route(route.ident)
            
            personnage << "{} route{s} supprimée{s}.".format(len(supprimer), s=s)
        else:
            personnage << "|err|Aucune route correspondant à supprimer.|ff|"
