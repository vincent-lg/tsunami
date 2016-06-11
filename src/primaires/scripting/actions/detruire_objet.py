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


"""Fichier contenant l'action detruire_objet."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Détruit un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.detruire_objet, "Objet")
        cls.ajouter_types(cls.detruire_objet_personnage, "Personnage", "str")
        cls.ajouter_types(cls.detruire_objet_personnage, "Personnage", "str",
                "Fraction")

    @staticmethod
    def detruire_objet(objet):
        """Détruit l'objet spécifié.

        L'objet peu être n'importe où (possédé par un personnage, posé sur
        le sol ou même existant dans les limbes) mais il faut préciser
        l'objet, pas son identifiant.

        Exemple d'utilisation :

          detruire_objet objet

        """
        importeur.objet.supprimer_objet(objet.identifiant)

    @staticmethod
    def detruire_objet_personnage(personnage, cle_objet, a_detruire=1):
        """Détruit le premier objet indiqué détenu par le personnage.

        L'objet détenu peut être :
          * Tenu par le personnage
          * Equipé par le personnage
          * Contenu dans un conteneur équipé par le personnage

        """
        a_detruire_o = a_detruire
        det_qtt = 0
        for objet, qtt, conteneur in \
                personnage.equipement.inventaire.iter_objets_qtt(True):
            if objet.cle == cle_objet:
                if qtt > a_detruire:
                    qtt = a_detruire
                conteneur.retirer(objet, qtt)
                if hasattr(objet, "identifiant"):
                    importeur.objet.supprimer_objet(objet.identifiant)

                a_detruire -= qtt
                det_qtt += qtt
                if det_qtt >= a_detruire_o:
                    break
