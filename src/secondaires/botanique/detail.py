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


"""Ce fichier contient la classe DetailMod, détaillée plus bas."""

from primaires.salle.detail import Detail

class DetailMod(Detail):

    """Classe décrivant le détail générique végétation.

    Ce détail permet au module botanique d'ajouter un élément observable
    constant dans chaque salle qui renvoie la végétation observable dans
    la salle.

    """

    def __init__(self, salle):
        """Constructeur de la période."""
        Detail.__init__(self, "vegetation plantes arbres", parent=salle)
        self.titre = "la végétation alentours"

    def __getnewargs__(self):
        return (None, )

    def get_nom_pour(self, personnage):
        return self.nom

    def regarder(self, personnage):
        """Le personnage regarde le détail dynamique.

        Ici, on lui affiche les plantes présentes dans la salle si il y en a.

        """
        msg = "Vous regardez la végétation alentours :\n"
        plantes = importeur.botanique.salles.get(self.parent, [])
        plantes = [p for p in plantes if p.cycle.visible and p.periode.visible]
        if not plantes:
            return "|att|Vous ne voyez rien de récoltable ici.|ff|"

        groupe = {}
        periodes = {}
        for plante in plantes:
            nb = groupe.get(plante.nom, 0)
            nb += 1
            groupe[plante.nom] = nb
            periodes[plante.nom] = plante.periode

        for nom, nb in groupe.items():
            periode = periodes[nom]
            msg += "\n  " + periode.get_nom(nb)

        return msg
