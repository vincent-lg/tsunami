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


"""Fichier contenant le masque <duree>."""

import re

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

# Constantes
RE_DUREE = re.compile(r"^(\d+)\s?([A-Za-z]+)$")

class Duree(Masque):
    
    """Masque <duree>.
    
    On attend une durée en paramètre, sous la forme d'une partie
    entière et d'un nom d'unité.
    Exemple :
        3h
        5m
    
    """
    
    nom = "duree"
    nom_complet = "durée"
    
    def init(self):
        """Initialisation des attributs"""
        self.secondes = 0
        self.temps = ""
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        message = liste_vers_chaine(commande).lstrip()
        self.a_interpreter = message
        commande[:] = []
        if not message:
            raise ErreurValidation(
                "Précisez une durée.")
        
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        duree = self.a_interpreter
        res = RE_DUREE.search(duree)
        if not res:
            raise ErreurValidation("Durée invalide.")
        
        nb, mesure = res.groups()
        nb = int(nb)
        mesure = mesure.lower()
        if mesure in ("s", "sec", "seconde", "secondes"):
            mult = 1
            nom_complet = "seconde"
        elif mesure in ("m", "mn", "min", "minute", "minutes"):
            mult = 60
            nom_complet = "minute"
        elif mesure in ("h", "hr", "heure", "heures"):
            mult = 3600
            nom_complet = "heure"
        elif mesure in ("j", "jr", "jour", "jours"):
            mult = 86400
            nom_complet = "jour"
        else:
            raise ErreurValidation("Mesure {} inconnue.".format(mesure))
        
        self.secondes = mult * nb
        s = ""
        if nb > 1:
            s = "s"
        self.temps = "{} {}{s}".format(nb, nom_complet, s=s)
        return True
