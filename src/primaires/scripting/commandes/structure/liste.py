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


"""Package contenant la commande 'structures liste'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'structures liste'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.schema = "(<cle>)"
        self.aide_courte = "affiche les structures"
        self.aide_longue = \
            "Sans argument, cette commande affiche tous les groupes " \
            "de structure définis, ainsi que le nombre de structures " \
            "de chaque groupe. Vous pouvez également préciser en " \
            "paramètre une clé de groupe : dans ce cas-là, les structures " \
            "du groupe précisé sont affichés."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        if dic_masques["cle"]:
            cle = dic_masques["cle"].cle
            if cle not in importeur.scripting.structures:
                personnage << "|err|Groupe {} inconnu.|ff|".format(
                        repr(cle))
                return

            groupe = importeur.scripting.structures[cle]
            tableau = Tableau("Structures du groupe " + cle)
            tableau.ajouter_colonne("Groupe")
            tableau.ajouter_colonne("ID", DROITE)
            tableau.ajouter_colonne("Champs", DROITE)
            structures = sorted(list(groupe.values()), key=lambda s: s.id)
            for structure in structures:
                tableau.ajouter_ligne(cle, structure.id,
                        len(structure.donnees))

            personnage << tableau.afficher()
        else:
            groupes = importeur.scripting.structures.items()
            tableau = Tableau("Groupes de structure actuels")
            tableau.ajouter_colonne("Groupe")
            tableau.ajouter_colonne("Nombre", DROITE)
            for cle, structures in sorted(tuple(groupes)):
                tableau.ajouter_ligne(cle, len(structures))

            personnage << tableau.afficher()
