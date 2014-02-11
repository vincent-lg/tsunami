# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Package contenant la commande 'oublier'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import contient

class CmdOublier(Commande):

    """Commande 'oublier'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "oublier", "forget")
        self.groupe = "joueur"
        self.schema = "<message>"
        self.aide_courte = "oublie un talent"
        self.aide_longue = \
            "Cette commande permet d'oublier un talent en récupérant les " \
            "points d'apprentissage utilisés pour l'apprendre. L'oubli " \
            "est irréversible et vous devrez réapprendre ce talent " \
            "à partir de zéro si vous changez d'avis. Un malus augmentant " \
            "à chaque utilisation de cette commande limitera les points " \
            "d'apprentissage récupérés, sauf si vous avez une connaissance " \
            "du talent inférieure à 10|pc|."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nom_talent = dic_masques["message"].message
        for tal in importeur.perso.talents.values():
            if contient(tal.nom, nom_talent) and tal.cle in personnage.talents:
                oubli = personnage.talents[tal.cle]
                malus = int(oubli / 100 * 5) + 1 if oubli > 10 else 0
                #personnage.malus += malus
                #if personnage.malus > 60:
                    #personnage.malus = 60
                del personnage.talents[tal.cle]
                personnage << "Vous avez oublié le talent {}.".format(tal.nom)
                return
        personnage << "|err|Le talent '{}' est introuvable.|ff|".format(
                nom_talent)
