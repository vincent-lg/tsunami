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


"""Fichier contenant le paramètre 'info' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmInfo(Parametre):
    
    """Commande 'navire info'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "info", "info")
        self.schema = "(<cle_navire>)"
        self.aide_courte = "donne des informations sur un navire"
        self.aide_longue = \
            "Cette commande donne des informations, soit sur le navire " \
            "passé en paramètre, soit sur le navire où vous vous trouvez " \
            "si aucun paramètre n'est précisé."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navire = dic_masques["cle_navire"]
        if navire is None:
            salle = personnage.salle
            if not hasattr(salle, "navire") or salle.navire is None:
                personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
                return
            
            navire = salle.navire
        else:
            navire = navire.navire
        
        modele = navire.modele
        etendue = navire.etendue
        etendue = etendue and etendue.cle or "aucune"
        direction = navire.direction.direction
        nom_direction = navire.direction.nom_direction
        vitesse = navire.vitesse.norme
        vitesse = round(vitesse, 3)
        vitesse = str(vitesse).replace(".", ",")
        acceleration = navire.acceleration.norme
        acceleration = round(acceleration, 3)
        acceleration = str(acceleration).replace(".", ",")
        dir_acceleration = navire.acceleration.direction
        dir_acceleration = round(dir_acceleration, 3)
        dir_acceleration = str(dir_acceleration).replace(".", ",")
        msg = "Informations sur le navire {} :\n".format(navire.cle)
        msg += "\n  Modèle : {} ({})".format(modele.cle, modele.nom)
        msg += "\n  Étendue : " + etendue
        msg += "\n  Coordonnées : {}".format(navire.position.coordonnees)
        msg += "\n  Vitesse : {}".format(vitesse)
        msg += "\n  Accélération : {} ({}°)".format(acceleration,
                dir_acceleration)
        msg += "\n  Direction : {} ({})".format(direction, nom_direction)
        personnage << msg
