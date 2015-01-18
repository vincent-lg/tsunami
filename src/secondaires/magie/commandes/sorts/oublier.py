# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Package contenant la commande 'sort oublier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmOublier(Parametre):

    """Commande 'sort oublier'."""

    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "oublier", "forget")
        self.schema = "<nom_sort>"
        self.aide_courte = "oublie un sort"
        self.aide_longue = \
            "Cette commande vous permet d'oublier un sort. Vous " \
            "devez préciser en paramètre le nom du sort. Pour éviter " \
            "de sélectionner le mauvais sort, veillez à préciser le " \
            "nom le plus complètement possible. |att|ATTENTION|ff| : " \
            "vous ne pourrez oublier le même sort qu'une fois. Si " \
            "vous apprenez un sort X et que vous oubliez ce sort, " \
            "puis que vous le réappreniez pour une raison ou une autre, " \
            "vous ne pourrez plus l'oublier de nouveau."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        sort = dic_masques["nom_sort"].sort

        if personnage.sorts.get(sort.cle) is None:
            personnage << "Vous ne connaissez pas ce sort.|ff|"
            return

        if sort.cle in personnage.sorts_oublies:
            personnage << "|err|Vous avez déjà oublié ce sort une fois.|ff|"
            return

        del personnage.sorts[sort.cle]
        personnage.sorts_oublies.append(sort.cle)
        personnage.points_tribut += sort.points_tribut
        s = "s" if sort.points_tribut > 1 else ""
        personnage << "Vous oubliez {} et récupérez {} point{s} de " \
                "tribut{s}.".format(sort.nom, sort.points_tribut, s=s)
