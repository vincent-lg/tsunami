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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'retirer' de la commande 'matelot'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRetirer(Parametre):

    """Commande 'matelot retirer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "retirer", "remove")
        self.schema = "<nom_matelot>"
        self.tronquer = True
        self.aide_courte = "retire un matelot de l'équipage"
        self.aide_longue = \
            "Cette commande permet de retirer un matelot de votre " \
            "équipage. Entrez le nom du matelot en paramètre. Le " \
            "personnage ne sera pas altéré (il s'agit d'un changement " \
            "de poste un peu sévère, voilà tout) et il restera sur " \
            "le pont dans l'attente de votre bon plaisir."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = salle.navire
        matelot = dic_masques["nom_matelot"].matelot
        if not navire.a_le_droit(personnage, "maître d'équipage"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        equipage = navire.equipage
        equipage.supprimer_matelot(matelot.nom)
        personnage << "{} a quitté votre équipage.".format(matelot.nom)
