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


"""Fichier contenant la classe Tresor, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class Tresor(BaseObj):
    
    """Classe représentant les statistiques globales sur le trésor.
    
    Ces informations doivent être sauvegardées car ces statistiques
    sont faites sur une certaine période, définie dans la configuration.
    
    """
    
    enregistrer = True
    def __init__(self):
        """Constructeur des statistiques."""
        BaseObj.__init__(self)
        self.derniere_stats = datetime.now()
        self.argent_total = 0
        self.argent_joueurs = 0
        self.joueur_max = None
        self.valeur_max = 0
        self.stats = []
    
    def __getnewargs__(self):
        return ()
    
    def __repr__(self):
        return "<tresor mis à jour le {}>".format(self.derniere_stats)
    
    @property
    def pc_joueurs_total(self):
        """Retourne le pourcentage de argent_joueurs sur argent_total."""
        if self.argent_total == 0:
            return 0
        
        return self.argent_joueurs / self.argent_total * 100
    
    @property
    def pc_joueur_max_total(self):
        """Retourne le pourcentage du joueur le plus riche sur le total."""
        if self.argent_total == 0:
            return 0
        
        return self.valeur_max / self.argent_total * 100
    
    @property
    def pc_fluctuation(self):
        """Retourne la fluctuation en pourcentage."""
        if self.stats:
            ancien_total = self.stats[0][1]
        else:
            ancien_total = self.argent_total
        
        if ancien_total == 0:
            return 0
        
        return (self.argent_total - ancien_total) / ancien_total * 100
    
    def mettre_a_jour(self):
        """Met à jour les stats."""
        self.stats.append((self.derniere_stats, self.argent_total))
        self.derniere_stats = datetime.now()
        nb_jours_fluctuation = importeur.tresor.cfg.nb_jours_fluctuation
        # Suppression des enregistrements trop anciens
        nb_secs = nb_jours_fluctuation * 24 * 60 * 60
        while self.stats:
            if (self.derniere_stats - self.stats[0][0]).seconds > nb_secs:
                del self.stats[0]
            else:
                break
        
        # Calcul de l'argent total
        total = 0
        total_joueurs = 0
        joueur_max = None
        valeur_max = 0
        for joueur in importeur.joueur.joueurs.values():
            nb = joueur.argent_total
            total += nb
            total_joueurs += nb
            if nb > valeur_max:
                valeur_max = nb
                joueur_max = joueur
        
        for zone in importeur.salle.zones.values():
            total += zone.argent_total
        
        self.argent_total = total
        self.argent_joueurs = total_joueurs
        self.joueur_max = joueur_max
        self.valeur_max = valeur_max
