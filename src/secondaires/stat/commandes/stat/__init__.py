# -*-coding:Utf-8 -*

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


"""Package contenant la commande 'stat'

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.date import *

class CmdStat(Commande):
    
    """Commande 'stat'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "stat", "stat")
        self.groupe = "administrateur"
        self.aide_courte = "donne des statistiques sur le MUD"
        self.aide_longue = \
            "Cette commande donne plusieurs statistiques sur le MUD depuis " \
            "son lancement."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # On récupère les statistiques
        stats = type(self).importeur.stat.stats
        imp = type(self).importeur
        
        ## Générales
        msg = "Informations générales :"
        # Depuis quand le serveur est-il lancé ?
        uptime = stats.uptime
        msg += "\n    Le MUD est démarré depuis {}.".format(get_date(uptime))
        
        msg += "\n"
        
        ## Commandes
        msg += "\nCommandes :"
        
        # Combien de commandes entrées ?
        msg += "\n    {} commandes entrées".format(stats.nb_commandes)
        # Temps moyen d'exécution
        msg += "\n    Temps moyen d'exécution : {:.3f}".format( \
                stats.tps_moy_commandes)
        
        # Commandes les plus gourmandes
        msg += "\n    Temps d'exécution maximum :"
        for temps in sorted(tuple(stats.max_commandes), reverse=True):
            commande = stats.max_commandes[temps]
            # on affiche que les 15 premiers caractères de la commande
            if len(commande) > 15:
                commande = commande[:15] + "..."
            
            msg += "\n        {} {:02.3f}s".format(commande.ljust(15), temps)
        
        msg += "\n"
        
        ## Watch dog
        msg += "\nWatch dog :"
        # Temps moyen du WD
        msg += "\n    Temps moyen : {:.3f}".format(stats.moy_wd)
        # WD maximum
        msg += "\n    Temps maximum : {:.3f}".format(stats.max_wd)
        
        ## Mémoire
        msg += "\nEn mémoire :"
        msg += "\n    {} joueurs issus de {} comptes".format(len(imp.connex.joueurs),
                len(imp.connex.comptes))
        msg += "\n    {} salles".format(len(imp.salle))
        msg += "\n    {} objets issus de {} prototypes".format(len(imp.objet.objets),
                len(imp.objet.prototypes))
        
        personnage << msg
