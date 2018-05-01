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
# LIABLE FOR ANY bugCT, INbugCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'bug'."""

from primaires.interpreteur.commande.commande import Commande

class CmdBug(Commande):

    """Commande 'bug'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "bug", "bug")
        self.schema = "(<message>)"
        self.aide_courte = "envoie un rapport de bug"
        self.aide_longue = \
            "Cette commande permet de créer un rapport de bug très " \
            "rapidement : il suffit d'entrer la commande %bug% suivie du " \
            "message du rapport. Le rapport est créé sans titre ni " \
            "catégorie, mais l'éditeur de configuration de rapport " \
            "n'apparaît pas, vous reviendrez tout de suite au jeu. " \
            "Cependant, si besoin est, vous pouvez toujours éditer votre " \
            "rapport après coup pour lui ajouter un titre plus explicite " \
            "et une catégorie. En outre, si vous ne précisez pas de " \
            "message, le système cherchera dans les dernières erreurs pour " \
            "constituer un rapport par défaut, comme il le fait avec la " \
            "commande %rapport% %rapport:bug% sans argument."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        if dic_masques["message"] is None:
            commande, trace = importeur.rapport.traces.get(personnage,
                    (None, None))
            if trace is None:
                personnage << "|err|Aucune erreur n'a été rapportée pour " \
                        "votre joueur.\nVous devez donc préciser un titre " \
                        "pour le bug que vous voulez rapporter.|ff|"
                return

            titre = "Erreur durant la commande {}".format(repr(commande))
            description = trace
        else:
            titre = "Sans titre"
            description = dic_masques["message"].message
            if len(description) < 10:
                personnage << "|err|Cette description de bug est trop " \
                        "courte.|ff|"
                return

        rapport = importeur.rapport.creer_rapport(titre, personnage)
        rapport.type = "bug"
        if description:
            rapport.description.paragraphes.extend(description.split("\n"))

        personnage << "Le rapport sans titre #{} a bien été envoyé.".format(
                rapport.id)
