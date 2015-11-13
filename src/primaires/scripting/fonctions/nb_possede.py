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


"""Fichier contenant la fonction nb_possede."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Teste si un personnage possède un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nb_possede_proto, "Personnage", "str")

    @staticmethod
    def nb_possede_proto(personnage, prototype_ou_type):
        """Retourne le nombre d'objets possédés par le personnage.

        Paramètres à préciser :

          * personnage : le personnage à tester
          * prototype_ou_type : un nom de type ou clé de prototype

        Cette fonction retourne le nombre d'objets correspondants, 0
        si le personnage ne possède aucun objet correspondant
        (dans son équipement, directement, ou dans un sac). Vous
        pouvez aussi vérifier que le personnage possède un certain
        type d'objet en précisant le nom du type précédé d'un '+'. Voir
        les exemples ci-dessous.

        Exemples d'utilisation :

          nb = nb_possede(personnage, "pomme_rouge")
          si nb:
              # La pomme rouge a pu être trouvée dans le personnage

          si nb_possede(personnage, "pomme_rouge"):
              # ...

          # Si vous voulez savoir si un personnage possède une arme
          nb_armes = nb_possede(personnage, "+arme")
          si nb_armes:

          # Et si vous n'avez pas besoin de connaître l'objet
          si nb_possede(personnage, "+arme"):
              # ...

        """
        total = 0
        for objet, qtt in personnage.equipement.inventaire.iter_objets_qtt():
            if prototype_ou_type.startswith("+"):
                nom_type = prototype_ou_type[1:]
                if objet.est_de_type(nom_type):
                    total += qtt
            else:
                if objet.cle == prototype_ou_type:
                    total += qtt

        return Fraction(total)
