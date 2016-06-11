# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'pivoter' de la commande 'canon'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmPivoter(Parametre):

    """Commande 'canon pivoter'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "pivoter", "pivot")
        self.schema = "<nombre>"
        self.aide_courte = "fait pivoter le canon"
        self.aide_longue = \
            "Cette commande permet de faire pivoter le canon " \
            "horizontalement. Tous les canons ne peuvent pas être " \
            "réorientés et ceux qui le peuvent disposent généralement " \
            "d'angles de tir. Même quand ce n'est pas le cas, n'oubliez " \
            "pas que vous devez faire attention à aligner le canon " \
            "correctement (si vous le retournez complètement, c'est " \
            "votre propre navire qui sera endommagé par l'explosion). " \
            "Précisez l'angle en degrés : un nombre positif (par exemple " \
            "|ent|90|ff| pour faire pivoter le canon de 90°) fera " \
            "pivoter le canon vers tribord, un nombre négatif (par " \
            "exemple |ent|-90|ff|) fera pivoter le canon sur bâbord."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_inf"] = "-359"
        nombre.proprietes["limite_sup"] = "359"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        personnage.agir("manip_canon")
        canon = None
        angle = dic_masques["nombre"].nombre
        if hasattr(salle, "navire"):
            for element in salle.elements:
                if element.nom_type == "canon":
                    canon = element
                    break

        if canon is None:
            personnage << "|err|Aucun canon ne se trouve ici.|ff|"
            return

        if angle == 0:
            personnage << "|err|Vous avez précisé un angle nul.|ff|"
            return

        if not hasattr(salle, "sabord_min"):
            sabord_min = None
        else:
            sabord_min = (salle.sabord_min - salle.sabord_max) % 360
            sabord_max = (salle.sabord_min + salle.sabord_max) % 360

        if sabord_min is None or sabord_min == 0:
            personnage << "|err|Vous ne pouvez faire pivoter ce canon.|ff|"
            return

        h_angle = canon.h_angle
        m_angle = (h_angle + angle) % 360
        if not salle.sabord_oriente(m_angle):
            personnage << "|err|Vous ne pouvez faire pivoter ce canon " \
                    "dans ce sens.|ff|"
            return

        canon.h_angle = m_angle
        cote = " tribord"
        r_cote = "tribord"
        if m_angle == 0:
            cote = ""
        elif m_angle < 0:
            cote = " bâbord"
            m_angle = -m_angle
        if angle < 0:
            r_cote = "bâbord"

        personnage << "Vous faites pivoter {} sur {}.".format(canon.nom,
                r_cote)
        salle.envoyer("{{}} fait pivoter {} sur {}.".format(canon.nom, r_cote),
                personnage)
        personnage << "{} est à présent sur {}°{}.".format(
                canon.nom.capitalize(), m_angle, cote)
