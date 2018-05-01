# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Eéquipage SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'contrôle' de la commande 'équipage'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre

class PrmControle(Parametre):

    """Commande 'équipage contrôle'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "contrôle", "control")
        self.tronquer = True
        self.schema = "(<texte_libre>)"
        self.aide_courte = "consulte ou modifie les contrôles"
        self.aide_longue = \
            "Les contrôles sont des formes d'ordres prolongés. " \
            "Ils nécessitent généralement la présence d'un commandant " \
            "(un capitaine ou un second) PNJ. Celui-ci est en charge " \
            "du contrôle et vérifie son déroulement au fur et à " \
            "mesure. Un exemple de contrôle répandu est celui modifiant " \
            "le cap du navire. Contrairement à un ordre simple, le " \
            "contrôle va s'assurer que l'ordre est toujours valable " \
            "plus tard. Si la direction du navire est modifiée pour " \
            "une raison quelconque, le commandant donnera les ordres " \
            "appropriés pour rectifier la direction. Côté manipulation, " \
            "certains ordres sont justes propres à un contrôle et " \
            "vous le verrez clairement indiqué dans l'aide de l'ordre. " \
            "Vous pouvez entrer cette commande pour vérifier les " \
            "contrôles actuels ou bien entrer en argument optionnel " \
            "un contrôle pour le supprimer."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = getattr(salle, "navire", None)
        if navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        if not navire.a_le_droit(personnage, "officier"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        equipage = salle.navire.equipage
        texte = dic_masques["texte_libre"]
        if texte:
            texte = supprimer_accents(texte.texte).lower()
            nom = equipage.noms_controles.get(texte)
            if nom is None:
                personnage << "|err|Contrôle introuvable.|ff|"
                return

            equipage.retirer_controle(nom)
            personnage << "Le contrôle {} a été réinitialisé.".format(
                    texte)
            return

        if not equipage.controles:
            personnage << "Aucun contrôle actif sur cet équipage."
            return

        msg = "Contrôles actifs :\n"
        for nom, cle in sorted(equipage.noms_controles.items()):
            controle = equipage.controles.get(cle)
            if controle is None:
                continue

            msg += "\n  {} : {}".format(nom.ljust(10).capitalize(),
                    controle.afficher())

        personnage << msg
