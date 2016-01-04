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


"""Package contenant la commande 'structures supprimer'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmSupprimer(Parametre):

    """Commande 'structures supprimer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "supprimer", "del")
        self.schema = "<cle> <nombre>"
        self.aide_courte = "supprime une structure"
        self.aide_longue = \
            "Cette commande supprime une structure existante. Vous " \
            "devez préciser deux paramètres séparés par un espace : " \
            "le premier est la clé du groupe, le second est l'identifiant " \
            "de la structure. Pour savoir quels groupes existent, " \
            "utilisez la commande %structure% %structure:liste% sans " \
            "paramètre. Pour connaître les identifiants des structures de " \
            "ce groupe, utilisez de nouveau %structure% %structure:liste% " \
            "suivi du nom de groupe à examiner. Par exemple %structure% " \
            "%structure:supprimer%|cmd| journal 1|ff|."

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

        importeur.scripting.supprimer_structure(structure)
        personnage << "La structure {} {} a bien été supprimée.".format(
                structure.structure, structure.id)
