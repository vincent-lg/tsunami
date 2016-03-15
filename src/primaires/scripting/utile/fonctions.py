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


"""Fichier contenant les fonctions utiles au scripting."""

import re

# Constantes
RE_VAR = re.compile(r"\$\{([A-Za-z0-9_]+)\}")
RE_VAR_RAPIDE = re.compile(r"\$([A-Za-z0-9_]+)([ .,|-]|$)")

def formatter(variables, chaine):
    f_variables = {}
    chaine = chaine.replace("_b_", "|")
    chaine = chaine.replace("$$", "|dollar|")
    chaine = RE_VAR_RAPIDE.sub(r"{\1}\2", chaine)
    chaine = RE_VAR.sub(r"{\1}", chaine)
    for nom, variable in variables.items():
        if hasattr(variable, "get_nom_pour"):
            f_variables[nom] = "{" + nom + "}"
        else:
            f_variables[nom] = str(variable)

    chaine = chaine.replace("|dollar|", "$")
    chaine = chaine.replace("|", "_b_")
    chaine = chaine.format(**f_variables)
    return chaine

def get_variables(variables, chaine):
    """Retourne les variables trouvées dans la chaîne."""
    vars = VariablesAAfficher(variables)
    chaine = RE_VAR_RAPIDE.sub(r"{\1}\2", chaine)
    chaine.format(**vars)
    return vars.utilisees

class VariablesAAfficher(dict):

    """Classe héritant d'un dictionnaire, chargée de retourner les variables.

    Les variables retournées sont uniquement celles demandées.

    """

    def __init__(self, variables):
        self.variables = variables
        self.utilisees = {}

    def __getitem__(self, item):
        self.utilisees[item] = self.variables[item]
        return "{" + item + "}"
