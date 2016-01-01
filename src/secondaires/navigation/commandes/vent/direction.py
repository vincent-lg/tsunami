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


"""Fichier contenant le paramètre 'direction' de la commande 'vent'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDirection(Parametre):
    
    """Commande 'vent direction'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "direction", "direction")
        self.schema = "<cle_vent> <nombre>"
        self.aide_courte = "place le vent dans la direction"
        self.aide_longue = \
            "Cette commande place le vent dans la direction " \
            "indiquée. Celle-ci doit être en degré, entre 0 (est) et " \
            "359. Le sens de rotation est horaire, ainsi, 45 => " \
            "sud-est, 90 => sud et ainsi de suite. Elle prend " \
            "en premier argument la clé du vent et en second " \
            "la direction sous la forme d'un angle."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_inf"] = "0"
        nombre.proprietes["limite_sup"] = "359"
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le vent et la direction
        vent = dic_masques["cle_vent"].vent
        direction = dic_masques["nombre"].nombre
        vent.vitesse.orienter(direction)
        personnage << \
                "Le vent {} a bien été placé dans ladirection {}°.".format(
                vent.cle, direction)
