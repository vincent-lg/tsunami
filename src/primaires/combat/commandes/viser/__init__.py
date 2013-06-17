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


"""Package contenant la commande 'viser'.

"""

from random import random

from primaires.interpreteur.commande.commande import Commande

class CmdViser(Commande):

    """Commande 'viser'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "viser", "target")
        self.nom_categorie = "combat"
        self.schema = "(<nombre>)"
        self.aide_courte = "vise un personnage"
        self.aide_longue = \
            "Cette commande vous permet de viser un personnage que " \
            "vous avez auparavant aperçu avec la commande %scruter%. " \
            "Vous devez simplement préciser en paramètre un nombre " \
            "(celui donné par %scruter% pour la cible particulière). " \
            "Si vous souhaitez arrêter de viser qui que ce soit, " \
            "entrez cette commande sans paramètre."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
            cibles = importeur.combat.cibles.get(personnage)
            if cibles is None:
                personnage << "|err|Vous ne voyez aucune cible " \
                        "pour l'heure.|ff|"
                return

            try:
                chemin, cible = cibles[nombre - 1]
            except IndexError:
                personnage << "|err|Ce nombre est invalide.|ff|"
                return

            if not cible.pk:
                personnage << "|err|Vous ne pouvez viser une cible " \
                        "qui n'a pas le flag PK activé.|ff|"
                return

            importeur.combat.cible[personnage] = cible
            personnage.envoyer("Vous commencez à viser {}.", cible)
        else:
            if personnage in importeur.combat.cible:
                del importeur.combat.cible[personnage]
                personnage << "Vous ne visez plus personne."
            else:
                personnage << "Vous ne visez personne actuellement."
