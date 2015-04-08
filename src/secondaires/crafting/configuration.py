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


"""Fichier contenant la classe Configuration, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.crafting.association import Association

class Configuration(BaseObj):

    """Classe représentant la configuration dynamique du crafting.

    Cette configuration associe un objet (une salle, un personnage
    ou autre) à une valeur. En soi, ce système est assez proche
    de celui des mémoires utilisées par le module primaire scripting,
    mais les configurations crafting ne sont pas destinées à être
    écrites par le scripting, seulement lues. Les configurations
    crafting permettent surtout d'étendre le champ de certaines
    informations (comme ajouter des attributs à des objets) en
    maintenant cette connexion indépendante, pour rendre l'indépendance
    inter-module plus grande.

    Pour utiliser la configuration (qui doit se trouver dans
    'importeur.crafting.configuration', il suffit de chercher
    l'association avec un objet (par exemple,
    'importeur.crafting.configuration[objet]'). Une classe
    particulière, assez proche du 'namespace' défini par 'argparse'
    est créée, ayant simplement pour but de faire correspondre
    l'attribut tel que recherché avec la valeur associée.

    Si vous avez une variable 'salle' contenant une salle,
    vous pouvez donc utiliser l'assocation crafting comme suit :
        configuration = importeur.crafting.configuration[salle]
        # Pour accéder à une valeur
        configuration.valeur
        # Pour la modifier
        configuration.valeur = "nouvelle valeur"
        # Vous pouvez aussi utiliser getattr et setattr

    """

    enregistrer = True

    def __init__(self):
        BaseObj.__init__(self)
        self.configuration = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __getitem__(self, objet):
        """Lecture d'une configuration."""
        if objet not in self.configuration:
            self.configuration[objet] = Association()

        return self.configuration[objet]
