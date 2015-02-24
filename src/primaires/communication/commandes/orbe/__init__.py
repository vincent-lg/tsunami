# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Package contenant la commande 'orbe'."""

from primaires.interpreteur.commande.commande import Commande
from .choisir import PrmChoisir
from .renommer import PrmRenommer

class CmdOrbe(Commande):

    """Commande 'orbe'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "orbe", "orb")
        self.nom_categorie = "parler"
        self.aide_courte = "manipulation des orbes"
        self.aide_longue = \
                "Les orbes de communication sont des objets reliés " \
                "magiquement, formant une toile de taille variable " \
                "et permettant une communication strictement RP, " \
                "mais à distance. Pour communiquer grâce à un orbe, " \
                "il suffit d'utiliser le symbole |cmd|*|ff| suivi " \
                "d'un espace et du message à envoyer. Tous les autres " \
                "détenteurs de l'orbe de même type recevront ce " \
                "message, plus ou moins longtemps après l'envoie, " \
                "plus ou moins altéré en fonction de la distance et " \
                "des pouvoirs de l'auteur de l'émission. Il est " \
                "également possible de n'envoyer le message qu'à " \
                "l'un des orbes. Pour ce faire, il faut utiliser " \
                "le signe |cmd|!|ff| suivi du nom de l'orbe, d'un " \
                "espace et du message à envoyer (par exemple " \
                "|cmd|!crabe J'arrive bientôt|ff|). Chaque joueur " \
                "peut renommer les orbes qu'il possède (voir la " \
                "commande %orbe% %orbe:renommer%). Pour parler avec " \
                "ces orbes, en utilisant soit la syntaxe publique " \
                "(|cmd|*|ff|), soit la syntaxe privée (|cmd|!|ff|), " \
                "il faut choisir l'orbe que l'on veut utiliser. Il " \
                "n'est en effet pas impossible d'avoir plusieurs " \
                "orbes sur soi, et il est important de préciser " \
                "lequel on veut utiliser quand on en possède plusieurs. " \
                "Pour ce faire, utilisez la commande %orbe% " \
                "%orbe:choisir%."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmChoisir())
        self.ajouter_parametre(PrmRenommer())
