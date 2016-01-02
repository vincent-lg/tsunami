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
# LIABLE FOR ANY extraireCT, INextraireCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action extraire."""

import re

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Extrait des informations d'une chaîne.

    Cette action est complexe mais puissante : elle permet
    d'extraire certaines informations d'une chaîne, potentiellement
    longue et formée de façon précise. Par exemple, si le script
    doit réagir à un message comme "arrêter <nom_du_joueur>", il
    est utile d'extraire le nom du joueur de la chaîne.

    Pour ce faire, on utilise les expressions régulières et les
    groupes de capture. Pour chaque groupe précisé dans l'expression,
    on doit préciser une variable. Considérez cet exemple :

        message = "abc123"
        extraire "^([a-z]+)([0-9]+)" message "chaine" "nombre"

    Après cet appel, la variable 'chaine' contiendra "abc" et la
    variable 'nombre' contiendra "123".

    +*ATTENTION*+ : c'est le NOM de la variable que vous devez
    préciser, pas la variable-même.*+

    Si vous n'êtes pas sûr que votre capture ait fonctionnée (la
    chaîne était peut-être mal formée), vous pouvez vérifier le
    contenu des variables extraites. Si la capture a échouée, toutes
    les variables contiendront une valeur nulle.

        extraire "^([a-z]+)$" chaine "nom"
        si nom:
            # L'extraction a réussie
        sinon:
            # L'extraction n'a pas réussie

    Pour plus d'informations sur les expressions régulirèes, rendez-vous
    [[regex|sur cette page d'aide]].

    """

    entrer_variables = True
    verifier = False

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.extraire)

    @staticmethod
    def extraire(expression, chaine, *noms_variables, variables=None):
        """Extrait les groupes dans les variables spécifiées.

        Paramètres à entrer :

          * expression : l'expression contenant les groupes de capture
          * chaine : la chaîne dans laquelle rechercher
          * Les noms des variables dans laquelle capturer l'information.

        Il faut préciser autant de noms de variables qu'il y a de
        groupes de capture.

        Par exemple :

          message = "abc123"
          extraire "^([a-z]+)([0-9]+)$" message "chaine" "nombre"

        Après cet appel, la variable 'chaine' contiendra "abc" et la
        variable 'nombre' contiendra "123".

        """
        t_chaine = supprimer_accents(chaine)
        res = re.search(expression, t_chaine, re.I)
        if res:
            groupes = res.groups()
            if len(groupes) != len(noms_variables):
                raise ErreurExecution("Le nombre de groupes de capture " \
                        "({}) est différent du nombre de variable " \
                        "précisé ({})".format(len(groupes),
                        len(noms_variables)))

            for i, groupe in enumerate(groupes):
                debut = res.start(i + 1)
                fin = res.end(i + 1)
                valeur = chaine[debut:fin]
                variables[noms_variables[i]] = valeur
        else:
            for nom in noms_variables:
                variables[nom] = None
