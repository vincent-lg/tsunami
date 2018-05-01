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


"""Fichier contenant les convertisseurs de la classe Personnage."""

class Convertisseur:
    """Classe pour envelopper les convertisseurs."""
    def depuis_version_0(objet, classe):
        objet.set_version(classe, 1)

    def depuis_version_1(objet, classe):
        objet.set_version(classe, 2)
        objet.nom = objet.nom.capitalize()
    def depuis_version_2(objet, classe):
        objet.set_version(classe, 3)
        objet.nom_groupe = objet.__dict__["groupe"]
        del objet.__dict__["groupe"]
    def depuis_version_3(objet, classe):
        objet.set_version(classe, 4)
        objet._prompt = "Vit   {stats.vitalite}     Man   {stats.mana}     " \
                "End   {stats.endurance}"
    def depuis_version_4(objet, classe):
        objet.set_version(classe, 5)
        objet.stats.parent = objet

    def depuis_version_5(objet, classe):
        """Mise à jour des étatts.

        Les états étaient conserfvés sous l'attribut _cle_etat. Il n'y
        avait que peu de personnalisation sur les templates et les états
        simultanés n'étaient pas autorisés. Tout cela change.

        """
        objet.set_version(classe, 6)
        del objet._cle_etat
        del objet.position
        del objet.occupe

    def depuis_version_6(objet, classe):
        """Mise à jour du prompt."""
        objet.set_version(classe, 7)
        prompt = objet._prompt
        del objet._prompt
        objet.prompts["défaut"] = prompt
