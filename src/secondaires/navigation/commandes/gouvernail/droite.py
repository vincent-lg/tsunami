# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'droite' de la commande 'gouvernail'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDroite(Parametre):

    """Commande 'gouvernail droite'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "droite", "right")
        self.schema = "(<nombre>)"
        self.aide_courte = "incline le gouvernail à tribord"
        self.aide_longue = \
                "Cette commande incline le gouvernail présent vers " \
                "tribord. Vous pouvez lui préciser en paramètre un " \
                "nombre entre 1 et 5 pour l'incliner plus."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_inf"] = "1"
        nombre.proprietes["limite_sup"] = "10"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        gouvernail = salle.gouvernail
        if not gouvernail:
            personnage << "|err|Il n'y a pas de gouvernail ici.|ff|"
            return

        if not gouvernail.tenu or gouvernail.tenu is not personnage:
            personnage << "|err|Vous ne tenez pas ce gouvernail.|ff|"
        else:
            nombre = dic_masques["nombre"]
            nombre = nombre and nombre.nombre or 1
            gouvernail.virer_tribord(personnage, nombre)
