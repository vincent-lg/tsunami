# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'voir' de la commande 'rapport'."""

from primaires.format.date import get_date
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.rapport.constantes import CLR_STATUTS, CLR_AVC

class PrmVoir(Parametre):

    """Commande 'rapport voir'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<nombre>"
        self.aide_courte = "visionne un rapport particulier"
        self.aide_longue = \
            "Cette commande offre un affichage détaillé d'un rapport."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        id = dic_masques["nombre"].nombre
        try:
            rapport = importeur.rapport.rapports[id]
        except KeyError:
            if personnage.est_immortel():
                personnage << "|err|Ce rapport n'existe pas.|ff|"
            else:
                personnage << "|err|Vous ne pouvez lire ce rapport.|ff|"
        else:
            if not personnage.est_immortel() and rapport.createur is not \
                    personnage and not rapport.public:
                personnage << "|err|Vous ne pouvez lire ce rapport.|ff|"
            else:
                createur = rapport.createur.nom if rapport.createur \
                        else "personne"
                ret = "Rapport #" + str(rapport.id) + " : " + rapport.titre
                ret += "\nCatégorie : " + rapport.type + " (" + \
                        rapport.categorie + ")"
                ret += "\nStatut : " + rapport.statut + ", avancement : " + \
                        str(rapport.avancement) + "%"
                ret += "\nCe rapport est classé en priorité " + \
                        rapport.priorite + "."
                ret += "\nDétail :\n"
                ret += str(rapport.description)
                ret += "\nRapport envoyé par " + createur + " " + \
                        get_date(rapport.date.timetuple()) + "\n"
                if personnage.est_immortel():
                    ret += "Depuis " + str(rapport.salle) + " "
                ret += "Assigné à " + rapport.aff_assigne_a + ".\n"
                personnage << ret
