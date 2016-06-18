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


"""Fichier contenant le paramètre 'carte' de la commande 'étendue'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.salle.contextes.carte import CarteEtendue

class PrmCarte(Parametre):

    """Commande 'etendue carte'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "carte", "map")
        self.schema = "<cle>"
        self.aide_courte = "affiche la carte de l'étendue"
        self.aide_longue = \
            "Cette commande permet d'afficher un contexte représentant " \
            "la carte (tronquée) de l'étendue. Les obstacles et les " \
            "liens peuvent être édités simplement ici. Le contexte " \
            "en lui-même propose beaucoup d'options et peut être " \
            "difficile à manipuler pour commencer (certaines étendues " \
            "sont bien plus grandes que la carte de base et il faut " \
            "apprendre à naviguer dedans) mais de l'aide est mise à " \
            "disposition pour vous aider à comprendre les différentes " \
            "possibilités d'édition."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        # On vérifie que cette étendue existe
        if cle not in type(self).importeur.salle.etendues.keys():
            personnage << "|err|Cette clé {} n'existe pas.|ff|".format(
                    repr(cle))
            return

        etendue = type(self).importeur.salle.etendues[cle]
        if not personnage.salle.coords.valide:
            personnage << "|err|La salle où vous vous trouvez n'a pas " \
                    "de coordonnées valides.|ff|"
            return

        x = int(personnage.salle.coords.x) - 15
        y = int(personnage.salle.coords.y) - 8
        contexte = CarteEtendue(personnage.instance_connexion, x, y)
        contexte.etendue = etendue
        personnage.contexte_actuel.migrer_contexte(contexte, detruire=False)
