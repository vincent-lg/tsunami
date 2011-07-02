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


"""Fichier contenant la classe Temps, détaillée plus bas."""

from fractions import Fraction

from abstraits.unique import Unique

class Temps(Unique):
    
    """Classe contenant les informations d'un temps, enregistrée en fichier.
    Cette classe est créée en lui passant en paramètre la configuration du
    module temps.
    
    Si la configuration du module est modifiée, il est nécessaire de supprimer
    le temps enregistré.
    
    """
    
    def __init__(self, config):
        """Constructeur de l'objet"""
        Unique.__init__(self, "temps", "temps")
        if not config:
            return
        
        reglage_init = config.reglage_initial
        self.annee = reglage_init[0]
        self.mois = reglage_init[1] - 1
        self.jour = reglage_init[2] - 1
        self.heure = reglage_init[3]
        self.minute = reglage_init[4]
        self.seconde = Fraction()
        
        # Différents noms
        self.saisons = config.saisons
        self.mois_saisons = config.mois
        self.noms_mois = [nom for nom in config.mois.keys()]
        if config.noms_jours:
            self.noms_jours = config.noms_jours
        else:
            self.noms_jours = [str(i) for i in range(1, \
                    config.nombre_jours + 1)]
        
        # On vérifie que le réglage initial est conforme aux noms
        try:
            nom_mois = self.noms_mois[self.mois]
        except IndexError:
            raise ValueError("erreur lors du réglage de l'heure initial : " \
                    "le mois {} est invalide".format(self.mois))
        try:
            nom_jour = self.noms_jours[self.jour]
        except IndexError:
            raise ValueError("erreur lors du réglage de l'heure initial : " \
                    "le jour {} est invalide".format(self.jour))
        
        self.vitesse_ecoulement = Fraction(config.vitesse_ecoulement)
        
        self.formatage_date = config.formatage_date
        self.formatage_heure = config.formatage_heure
    
    def __getnewargs__(self):
        return (None, )
    
    @property
    def no_j(self):
        return "{:02}".format(self.jour)
    
    @property
    def nm_j(self):
        return self.noms_jours[self.jour]
    
    @property
    def no_m(self):
        return "{:02}".format(self.mois)
    
    @property
    def nm_m(self):
        return self.noms_mois[self.mois]
    
    @property
    def nm_s(self):
        return self.mois_saisons[self.nm_m]
    
    @property
    def no_a(self):
        return "{}".format(self.annee)
    
    @property
    def no_h(self):
        return "{:02}".format(self.heure)
    
    @property
    def no_m(self):
        return "{:02}".format(self.minute)
    
    @property
    def date_formatee(self):
        """Retourne la date formatée"""
        return self.formatage_date.format(no_j=self.no_j,
                nm_j=self.nm_j, no_m=self.no_m, nm_m=self.nm_m,
                nm_s=self.nm_s, no_a=self.no_a)
    
    @property
    def heure_formatee(self):
        """Retourne l'heure formatée"""
        return self.formatage_heure.format(no_h=self.no_h, no_m=self.no_m)
    
    def inc(self):
        """Incrémente de 1 seconde réelle"""
        self.seconde += 1 / self.vitesse_ecoulement
        
        if self.seconde >= 60:
            self.seconde = Fraction()
            self.minute += 1
        if self.minute >= 60:
            self.minute -= 60
            self.heure += 1
        if self.heure >= 24:
            self.heure -= 24
            self.jour += 1
        if self.jour >= len(self.noms_jours):
            self.jour -= len(self.noms_jours)
            self.mois += 1
        if self.mois > len(self.noms_mois):
            self.mois -= len(self.noms_mois)
            self.annee += 1
