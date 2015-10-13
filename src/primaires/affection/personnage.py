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


"""Ce module contient la classe AffectionPersonnage, détaillée plus bas."""

from fractions import Fraction

from bases.collections.flags import Flags
from .base import AffectionAbstraite
from primaires.affection.script_personnage import ScriptAffectionPersonnage

class AffectionPersonnage(AffectionAbstraite):

    """Affection propre à un personnage."""

    nom_type = "personnage"
    nom_scripting = "affection de personnage"
    def_flags = Flags()
    def_flags.ajouter("doit être connecté", 1)
    def_flags.ajouter("doit être vivant", 2)

    def __init__(self, cle):
        AffectionAbstraite.__init__(self, cle)
        self.script = ScriptAffectionPersonnage(self)
        self.etat = ""

        # Liste de tuple (force, message)
        self.messages_personnels = []

        if cle:
            importeur.affection.aff_personnages[self.cle] = self

    def initialiser(self, affection):
        """Initialise une affection concrète."""
        if self.etat:
            affection.affecte.etats.ajouter(self.etat, vider=True)

    def programmer_destruction(self, affection):
        """Programme la destruction de l'affection de personnage."""
        try:
            self.message_detruire(affection)
        except NotImplementedError:
            self.executer_script("détruit", affection)

        if self.etat and self.etat in affection.affecte.etats:
            affection.affecte.etats.retirer(self.etat)

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
        self.script[evenement].executer(personnage=affection.affecte,
                force=Fraction(affection.force),
                duree=Fraction(affection.duree), **variables)

    def tick(self, affection):
        """Tick l'affection."""
        if affection.affecte is None or not affection.affecte.e_existe:
            affection.e_existe = False
            return

        if self.a_flag("doit être vivant") and affection.affecte.est_mort():
            return

        if self.a_flag("doit être connecté"):
            from primaires.joueur.joueur import Joueur
            personnage = affection.affecte
            if isinstance(personnage, Joueur) and not joueur.est_connecte():
                return False

        AffectionAbstraite.tick(self, affection)
