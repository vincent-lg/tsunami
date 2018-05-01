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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant le paramètre 'étendre' de la commande 'chemin'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEtendre(Parametre):

    """Paramètre 'étendre de la commande 'chemin'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "étendre", "extend")
        self.schema = "<cle> <direction>"
        self.aide_courte = "ajoute une sortie au chemin"
        self.aide_longue = \
            "Cette commande permet d'ajouter une sortie en fin du " \
            "chemin précisé. Vous devez spécifier en premier paramètre " \
            "la clé du chemin et en second paramètre le nom de la " \
            "direction (|att|pas le nom de la sortie !|ff|). La dernière " \
            "salle du chemin sera cherchée pour une sortie correspondante."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        cle = self.noeud.get_masque("cle")
        cle.proprietes["regex"] = r"'[a-z0-9_:]{3,}'"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        direction = dic_masques["direction"].direction
        if cle not in importeur.pnj.chemins:
            personnage << "|err|Ce chemin n'existe pas.|ff|"
            return

        chemin = importeur.pnj.chemins[cle]
        if len(chemin.salles) == 0:
            personnage << "|err|Ce chemin n'a aucune salle de départ.|ff|"
            return

        salle = chemin.destination
        if salle.sorties.get(direction) is None:
            personnage << "|err|La salle {} ne possède pas de sortie " \
                    "dans la direction {}.|ff|".format(salle.ident,
                    direction)
            return

        chemin.ajouter_salle(direction)
        personnage << "La direction {} a bien été ajoutée dans le " \
                "chemin {}.".format(direction, chemin.cle)
