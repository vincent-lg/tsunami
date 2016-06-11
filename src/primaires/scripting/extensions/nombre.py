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


"""Module contenant la classe Nombre, détaillée plus bas."""

from textwrap import dedent

from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.extensions.base import Extension

class Nombre(Extension):

    """Classe représentant le type éditable 'nombre'.

    Ce type utilise soit l'éditeur Entier, soit l'éditeur Flottant.
    Les limites inférieures et supérieures sont également supportées.

    """

    extension = "nombre"
    aide = "un nombre, à virgule ou pas"

    def __init__(self, structure, nom):
        Extension.__init__(self, structure, nom)
        self.a_virgule = False
        self.limite_inf = None
        self.limite_sup = None

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        if self.a_virgule:
            return Flottant
        else:
            return Entier

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        return (self.limite_inf, self.limite_sup)

    def etendre_editeur(self, presentation):
        """Ëtend l'éditeur en fonction du type de l'extension."""
        # Nombre à virgule
        a_virgule = presentation.ajouter_choix("nombre à virgule", "v", Flag,
                self, "a_virgule")
        a_virgule.parent = presentation

        # Limite inférieure
        inf = presentation.ajouter_choix("limite inférieure", "f", Entier,
                self, "limite_inf")
        inf.parent = presentation
        inf.prompt = "Entrez la limite inférieure : "
        inf.apercu = "{valeur}"
        inf.aide_courte = dedent("""
            Entrez la limite inférieure autorisée ou |ent|/|ff| pour
            revenir à la fenêtre parente.

            Si une limite inférieure est précisée, le personnage édiant
            ce menu ne pourra pas entrer un nombre inférieur.

            Limite inférieure actuelle : {valeur}""".strip("\n"))

        # Limite supérieure
        sup = presentation.ajouter_choix("limite supérieure", "s", Entier,
                self, "limite_sup")
        sup.parent = presentation
        sup.prompt = "Entrez la limite supérieure : "
        sup.apercu = "{valeur}"
        sup.aide_courte = dedent("""
            Entrez la limite supérieure autorisée ou |cmd|/|ff| pour
            revenir à la fenêtre parente.

            Si une limite supérieure est précisée, le personnage édiant ce
            menu ne pourra pas entrer un nombre supérieur.

            Limite supérieure actuelle : {valeur}""".strip("\n"))
