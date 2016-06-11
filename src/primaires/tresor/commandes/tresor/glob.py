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


"""Package contenant le paramètre 'global' de la commande 'tresor'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmGlobal(Parametre):
    
    """Commande 'tresor global'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "global", "global")
        self.aide_courte = "consulte le trésor global"
        self.aide_longue = \
            "Cette commande pdonne des informations statistiques sur " \
            "l'argent en jeu et des idées quant à sa répartition globale. " \
            "Il peut être utile de suivre l'évolution du marché, pour " \
            "savoir notamment ce que possèdent les joueurs considérant " \
            "le marché global, à quelle vitesse le marché évolue, à " \
            "quel point fluctue-t-il. Il est peu probable que l'argent " \
            "en jeu diminue mais il est cependant peu souhaitable " \
            "qu'il augmente trop (bien qu'une stagnation soit très peu " \
            "probable). Plus le marché est instable, plus il est ouvert."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # On demande les informations au module
        stats = importeur.tresor.get_stats()
        msg = "Statistiques actuelles du trésor :"
        msg += "\n  Argent en jeu : " + stats.argent_total
        msg += " (" + stats.fluctuation + "% depuis " + \
                stats.nb_jours_fluctuation + " jour(s))"
        msg += "\n  Argent détenus par les joueurs : " + stats.argent_joueurs
        msg += " (soit " + stats.pc_joueurs_total + "% du trésor)"
        msg += "\n  Plus grande fortune : " + \
                stats.valeur_max + " (soit " + \
                stats.pc_joueur_max_total + "% du trésor)"
        
        personnage << msg
