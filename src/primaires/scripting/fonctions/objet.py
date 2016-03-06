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


"""Fichier contenant la fonction objet."""

from primaires.objet.conteneur import SurPoids
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Recherche et retourne un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.objet_salle, "Salle", "str")
        cls.ajouter_types(cls.objet_perso, "Personnage", "str")
        cls.ajouter_types(cls.objet_ident, "str")

    @staticmethod
    def objet_salle(salle, type_ou_prototype):
        """Retourne, si trouvé, l'objet indiqué posé dans la salle.

        Vous devez préciser en paramètre la salle et la clé du prototype
        de l'objet. L'objet retourné est cherché parmi les objets posés
        au sol de la salle. Si aucun n'est trouvé, retourne une variable
        vide. Vous pouvez également faire une recherche par type
        (voir plus bas).

        Paramètres à préciser :

          * salle : la salle dans laquelle chercher
          * type_u_prototype : la clé du prototype ou nom du type à chercher

        Exemples d'utilisation :

          pomme_rouge = objet(salle, "pomme_rouge")
          # Si l'objet de prototype 'pomme_rouge' peut être trouvé sur le sol,
          # retourne le premier objet trouvé. Sinon retourne une variable vide.
          # Vous devriez donc tester.
          si pomme_rouge:
              ...

          # Vous pouvez aussi faire la recherche sur le type en
          # ajoutant un '+' devant le nom du type :
          fruit = objet(salle, "+fruit")
          # Là encore, pour vérifier qu'un objet a pu être trouvé
          si fruit:
              ...

        """
        nom_type = None
        cle_prototype = None
        if type_ou_prototype.startswith("+"):
            nom_type = type_ou_prototype[1:]
        else:
            cle_prototype = type_ou_prototype

        for objet in salle.objets_sol._objets:
            if nom_type and objet.est_de_type(nom_type):
                return objet
            elif cle_prototype and objet.cle == cle_prototype:
                return objet

        return None

    @staticmethod
    def objet_perso(personnage, cle_prototype):
        """Retourne, si trouvé, l'objet indiqué possédé par le personnage.

        La recherche se fait dans l'inventaire étendu (comprenant
        donc l'équipement) du personnage. Vous pouvez par exemple
        chercher le premier objet de clé "sac_toile" possédé par
        le personnage. Si il en possède effectivement un (ou plusieurs),
        le premier trouvé est retourné. Sinon, une valeur nulle est
        retournée.

        """
        # on teste l'inventaire
        for o in personnage.equipement.inventaire:
            if o.cle == cle_prototype:
                return o

        return None

    @staticmethod
    def objet_ident(identifiant):
        """Retourne l'objet correspondant à l'identifiant.

        Si l'objet de l'identifiant n'est pas trouvé, crée une
        alerte. L'identifiant, à préciser sous forme d'une chaîne,
        est sous la forme "cle_NOMBRE". Par exemple, "pomme_rouge_128".

        Paramètres à préciser :

          * identifiant : l'identifiant de l'objet (une chaîne).

        Exemple d'utilisation :

          objet = objet("sabre_38")

        """
        try:
            return importeur.objet.objets[identifiant.lower()]
        except KeyError:
            raise ErreurExecution("Identifiant d'objet {} introuvable.".format(
                    repr(identifiant)))
