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


"""Ce module contient la classe AffectionSalle, détaillée plus bas."""

from fractions import Fraction

from .base import AffectionAbstraite
from primaires.affection.script_salle import ScriptAffectionSalle

class AffectionSalle(AffectionAbstraite):

    """Affection propre à une salle."""

    nom_type = "salle"
    nom_scripting = "affection de salle"
    def_flags = {
        "humide": 1,
    }

    def __init__(self, cle):
        AffectionAbstraite.__init__(self, cle)
        self.script = ScriptAffectionSalle(self)
        if cle:
            importeur.affection.aff_salles[self.cle] = self

    def programmer_destruction(self, affection):
        """Programme la destruction de l'affection de salle."""
        if affection.affecte is None:
            return

        try:
            affection.affecte.envoyer(self.message_detruire(affection),
                    prompt=False)
        except NotImplementedError:
            self.executer_script("détruit", affection)

    def message_detruire(self, affection):
        """Retourne le message à afficher quand l'affection se termine.

        Par défaut, lève une exception NotImplementedError. Cela a
        pour effet d'exécuter l'évènement 'détruit' à la place. Si
        vous souhaitez faire une affection par défaut, redéfinissez la
        méthode 'message_detruire' en sachant que, par défaut, elle
        n'appellera pas l'évènement 'détruit'.

        """
        raise NotImplementedError

    def executer_script(self, evenement, affection, **variables):
        """Exécute le script lié."""
        self.script[evenement].executer(salle=affection.affecte,
                force=Fraction(affection.force),
                duree=Fraction(affection.duree), **variables)

    def detruire(self):
        """Destruction de l'affection."""
        AffectionAbstraite.detruire(self)
        self.script.detruire()
