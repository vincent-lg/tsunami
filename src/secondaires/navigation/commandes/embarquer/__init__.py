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


"""Package contenant la commande 'embarquer'."""

from math import sqrt

from primaires.interpreteur.commande.commande import Commande
from secondaires.navigation.constantes import *

class CmdEmbarquer(Commande):
    
    """Commande 'embarquer'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "embarquer", "embark")
        self.nom_categorie = "navire"
        self.aide_courte = "embarque sur un navire proche"
        self.aide_longue = \
            "Cette commande permet d'embarquer sur un navire proche. " \
            "Vous devez l'entrer sur un quai. Si un navire se trouve " \
            "assez prêt, vous sauterez à bord, ce qui peut être utile " \
            "pour des navires n'ayant aucune passerelle."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if hasattr(salle, "navire"):
            o_navire = salle.navire
            etendue = o_navire.etendue
        else:
            # On va chercher le navire le plus proche
            o_navire = None
            etendue = salle.etendue
            if etendue is None:
                personnage << "|err|Vous n'êtes pas sur un quai.|ff|"
                return
            
        navires = [n for n in importeur.navigation.navires.values() if \
                n.etendue is etendue and n is not o_navire]
        
        personnage.agir("deplacer")
        # On cherche la salle de nagvire la plus proche
        d_salle = None # la salle de destination
        navire = None
        distance = 2
        x, y, z = salle.coords.tuple()
        for t_navire in navires:
            for t_salle in t_navire.salles.values():
                if t_salle.coords.z == etendue.altitude:
                    t_x, t_y, t_z = t_salle.coords.tuple()
                    t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
                    if t_distance < distance:
                        navire = t_navire
                        d_salle = t_salle
                        distance = t_distance
        
        if d_salle is None:
            personnage << "|err|Aucun navire n'a pu être trouvé à " \
                    "proximité.|ff|"
            return
        
        personnage.salle = d_salle
        personnage << "Vous sautez dans {}.".format(
                navire.nom)
        personnage << d_salle.regarder(personnage)
        d_salle.envoyer("{{}} arrive en sautant depuis {}.".format(
                salle.titre.lower()), personnage)
        salle.envoyer("{{}} saute dans {}.".format(
                navire.nom), personnage)
