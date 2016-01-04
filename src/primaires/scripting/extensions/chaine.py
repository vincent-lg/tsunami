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


"""Module contenant la classe Chaine, détaillée plus bas."""

from primaires.interpreteur.editeur.flags import Flags
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.extensions.base import Extension

# Constantes
VERIFICATION = {
        "doit être une clé valide": 1,
}

MODIFICATION = {
        "première lettre en majuscule": 1,
}

class Chaine(Extension):

    """Classe représentation le type éditable 'chaîne'.

    Ce type utilise l'éditeur Uniligne.

    """

    extension = "chaîne"
    aide = "une chaîne de caractères"

    def __init__(self, structure, nom):
        Extension.__init__(self, structure, nom)
        self.verification = 0
        self.modification = 0

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        return Uniligne

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        return (self.verification, self.modification)

    def etendre_editeur(self, presentation):
        """Ëtend l'éditeur en fonction du type de l'extension."""
        # Flags de vérification
        verification = presentation.ajouter_choix("flags de vérification",
                None, Flags, self, "verification", VERIFICATION)
        verification.parent = presentation
        verification.aide_courte = \
            "Flags de vérification avant modification :"

        # Flags de modification
        modification = presentation.ajouter_choix("flags de modification",
                None, Flags, self, "modification", MODIFICATION)
        modification.parent = presentation
        modification.aide_courte = \
            "Flags de modification de la chaîne entrée :"
