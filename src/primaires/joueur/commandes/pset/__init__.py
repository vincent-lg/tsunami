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


"""Package contenant la commande 'pset'"""

from primaires.interpreteur.commande.commande import Commande
from primaires.perso.exceptions.stat import *

class CmdPset(Commande):
    
    """Commande 'pset'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pset", "pset")
        self.groupe = "administrateur"
        self.schema = "<nom_joueur> <nom_stat> <nombre>"
        self.aide_courte = "modifie les stats d'un personnage"
        self.aide_longue = \
                "Cette commande permet de modifier les stats d'un " \
            "personnage. Vous devez lui préciser le personnage à modifier, " \
            "le nom de la stat et sa nouvelle valeur."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage_mod = dic_masques["nom_joueur"].joueur
        nom_stat = dic_masques["nom_stat"].nom_stat
        valeur = dic_masques["nombre"].nombre
        
        # On cherche la stat
        try:
            stat = getattr(personnage_mod.stats, "_{}".format(nom_stat))
        except AttributeError:
            personnage << "|err|Le personnage {} ne possède pas cette " \
                    "stat|ff|.".format(personnage_mod.nom)
            return
        
        # On cherche à modifier la stat
        try:
            stat.courante = valeur
        except DepassementStat:
            personnage << "|att|Votre valeur a soulevée une erreur.|ff|"
        
        personnage << "Le personnage {} a à présent la stat {} égale à " \
                "{}.".format(personnage_mod.nom, nom_stat, stat.courante)
