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


"""Fichier contenant le paramètre 'supprimer' de la commande 'étendue obstacle'.

"""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation

class PrmObstacleSupprimer(Parametre):
    
    """Commande 'étendue obstacle supprimer'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "supprimer", "del")
        self.schema = "<cle> <coords2d>"
        self.aide_courte = "retire l'obstacle aux coordonnées"
        self.aide_longue = \
            "Cette commande permet de suppriemr un obstacle de " \
            "l'étendue. Vous devez préciser la clé de l'étendue et " \
            "les coordonnées, en deux dimensions, du point à supprimer."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        coords = dic_masques["coords2d"].coords
        # On vérifie que la clé est une étendue
        try:
            etendue = type(self).importeur.salle.etendues[cle]
        except KeyError:
            personnage << "|err|Cette étendue {} n'existe pas.|ff|".format(cle)
        else:
            if coords not in etendue.obstacles:
                personnage << "|err|Ce point n'est pas un obstacle de " \
                        "l'étendue.|ff|"
            else:
                str_coords = str(coords[0]) + "." + str(coords[1])
                etendue.supprimer_obstacle(coords)
                personnage << \
                        "Le point {} a été retiré des obstacles de " \
                        "l'étendue {}.".format(str_coords, etendue.cle)
