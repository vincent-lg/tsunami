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
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'structures voir'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre
from primaires.scripting.structure import StructureComplete

class PrmVoir(Parametre):

    """Commande 'structures voir'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<cle> <nombre>"
        self.aide_courte = "affiche le détail d'une structure"
        self.aide_longue = \
            "Cette commande affiche le détail d'une structure. Vous " \
            "devez préciser deux paramètres séparés par un espace : " \
            "le premier est la clé du groupe, le second est l'identifiant " \
            "de la structure. Pour savoir quels groupes existent, " \
            "utilisez la commande %structure% %structure:liste% sans " \
            "paramètre. Pour savoir les identifiants des structures de " \
            "ce groupe, utilisez de nouveau %structure% %structure:liste% " \
            "suivi du nom de groupe à examiner. Par exemple %structure% " \
            "%structure:voir%|cmd| journal 1|ff|."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        cle = dic_masques["cle"].cle
        nombre = dic_masques["nombre"].nombre

        if cle not in importeur.scripting.structures:
            personnage << "|err|Groupe {} inconnu.|ff|".format(
                    repr(cle))
            return

        groupe = importeur.scripting.structures[cle]
        structure = groupe.get(nombre)
        if structure is None:
            personnage << "|err|La structure de groupe {} et d'ID " \
                    "{} n'existe pas.|ff|".format(repr(cle), nombre)
            return

        tableau = Tableau("Détail de la structure {} {} :".format(cle, nombre))
        tableau.ajouter_colonne("Case")
        tableau.ajouter_colonne("Valeur")
        donnees = sorted(tuple(structure.donnees.items()))
        for champ, valeur in donnees:
            if isinstance(valeur, StructureComplete):
                valeur = valeur.structure + " " + str(valeur.id)
            elif isinstance(valeur, bool):
                valeur = "vrai" if valeur else "faux"
            elif isinstance(valeur, list):
                liste = []
                for element in valeur:
                    if isinstance(element, StructureComplete):
                        element = element.structure + " " + str(element.id)

                    liste.append(element)

                valeur = liste

            tableau.ajouter_ligne(champ, valeur)

        personnage << tableau.afficher()
