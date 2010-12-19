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


"""Fichier contenant le paramètre 'hotboot' de la commande 'module'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmHotboot(Parametre):
    
    """Commande 'module hotboot'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "hotboot", "hotboot")
        self.aide_courte = "permet de redémarrer les modules du MUD"
        self.aide_longue = \
            "Cette commande permet de redémarrer un ou plusieurs modules " \
            "pendant l'exécution du MUD. Cela permet de corriger des bugs, " \
            "intégrer des modifications, ajouter ou retirer des commandes " \
            "sans avoir à déconnecter un seul joueur. Si les modifications " \
            "touchent au corps, il est nécessaire de redémarrer complètement " \
            "le MUD (voir la commande |cmd|shutdown|ff|)."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        personnage.envoyer("Redémarrage à chaud des modules en cours...")
        nom = personnage.compte.nom
        type(self).importeur.tout_recharger()
        personnage = type(self).importeur.connex.get_compte( \
                nom).get_joueur(personnage)
        personnage.envoyer("Les modules ont bien été redémarré.")
