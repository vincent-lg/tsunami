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


from abstraits.obase import BaseObj
from primaires.format.fonctions import contient, oui_ou_non
"""Ce fichier contient la classe UOptions, détaillée plus bas."""

OPT_AUTOTAB = 1
OPT_AUTONL = 2

AIDES = {
    OPT_AUTOTAB: \
        "Si cette option est activée, à chaque fois que l'on commence " \
        "un nouveau paragraphe, une nouvelle tabulation est " \
        "automatiquement ajoutée avant le texte que l'on insert.",
    OPT_AUTONL: \
        "Si cette option est activée, quand on finit un paragraphe " \
        "et presse ENTRER le texte suivant sera un nouveau paragraphe. " \
        "En revanche, si cette option est désactivée, si vous insérez " \
        "du texte il sera ajouté à la fin du dernier paragraphe. " \
        "Pour commencer un nouveau paragraphe, vous devrez appuyer sur " \
        "ENTRER sans entrer de texte auparavant.",
}

NOMS_OPTIONS = {
    OPT_AUTOTAB: "tabulation automatique",
    OPT_AUTONL: "retour automatique à la ligne",
}

class UOptions(BaseObj):

    """Classe contenant les options utilisateurs concernant l'édition.

    Ces options se trouvent dans un dictionnaire. En clé, le personnage
    et en valeur le chiffre correspondant aux options.

    """

    enregistrer = True
    def __init__(self):
        """Constructeur du dictionnaire."""
        BaseObj.__init__(self)
        self.options = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __getstate__(self):
        """Enregistrement de l'objet.

        MongoDB n'aime pas enregistrer des dictionnaires avec des
        joueurs en clé, on convertit donc en nom.

        """
        attrs = BaseObj.__getstate__(self)
        options = {}
        for joueur, valeur in attrs["options"].items():
            options[joueur.nom] = valeur

        attrs["options"] = options
        return attrs

    def get_options(self, personnage):
        """Retourne le nombre correspondant au personnage ou 0.

        0 représente en effet aucun flag.

        """
        return self.options.get(personnage, 0)

    def a_option(self, personnage, option):
        """Retourne True si le personnage a l'option, False sinon.

        L'option doit être donnée sous la forme d'un nombre.

        """
        return bool(option & self.get_options(personnage))

    @staticmethod
    def get_nombre_option(nom):
        """Retourne le nombre lié à un nom d'option, même abrégé."""
        for nombre, t_nom in NOMS_OPTIONS.items():
            if contient(t_nom, nom):
                return nombre

        raise ValueError("l'option {} est introuvable".format(repr(nom)))

    def afficher_options(self, personnage):
        """Retourne les options actives du personnage (list)."""
        nombre = self.get_options(personnage)
        options = []
        for n, o in NOMS_OPTIONS.items():
            msg = o.capitalize().ljust(15) + " : "
            msg += oui_ou_non(bool(n & nombre))
            options.append(msg)

        options.sort()
        return options

    def changer_option(self, personnage, option):
        """Change la valeur de l'option."""
        self.options[personnage] = self.get_options(personnage) ^ option
        self._enregistrer()
