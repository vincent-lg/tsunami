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


"""Package contenant la commande 'route trouver'."""

import traceback
from textwrap import wrap

from primaires.interpreteur.masque.parametre import Parametre

class PrmTrouver(Parametre):

    """Commande 'route trouver'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "trouver", "find")
        self.schema = "<ident_salle>"
        self.aide_courte = "cherche une route"
        self.aide_longue = \
            "Cette commande demande au système de chercher le chemin " \
            "le plus court entre deux salles : la salle d'origine " \
            "est celle où vous vous trouvez actuellement. La salle de " \
            "destination doit être précisée sous la forme d'un " \
            "paramètre (|ent|zone:mnemonique|ff|). Notez bien que " \
            "ces deux salles doivent se trouver dans le complexe " \
            "des routes, sans quoi le chemin le plus court ne porura " \
            "pas être déterminé."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        origine = personnage.salle
        destination = dic_masques["ident_salle"].salle
        try:
            description = importeur.route.trouver_chemin(origine,
                    destination)
        except ValueError as err:
            print(traceback.format_exc())
            personnage << "|err|" + str(err).capitalize() + ".|ff|"
        else:
            personnage << "\n".join(wrap(description.afficher(ligne=True)))
