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


"""Fichier contenant la fonction objets."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne plusieurs objets."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.objets_prototype, "str")
        cls.ajouter_types(cls.objets_salle, "Salle")
        cls.ajouter_types(cls.objets_salle, "Salle", "str")
        cls.ajouter_types(cls.objets_personnage, "Personnage")
        cls.ajouter_types(cls.objets_personnage, "Personnage", "str")

    @staticmethod
    def objets_prototype(cle_prototype):
        """Retourne les objets modelés sur le prototype précisé.

        Les paramètres à entrer sont :

          * cle_prototype : la clé du prototype (chaîne)

        Cette fonction retourne tous les objets modelés sur ce prototype.
        Si vous appelez par exemple cette fonction avec le paramètre
        "pomme_rouge", tous les objets "pomme_rouge" (comme "pomme_rouge_1",
        "pomme_rouge_2" et ainsi de suite) seront retournés.

        """
        try:
            prototype = importeur.objet.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        return list(prototype.objets)

    @staticmethod
    def objets_salle(salle, type_ou_prototype=""):
        """Retourne les objets posés dans la salle (éventuellement filtrés).

        Cette fonction prend un argument obligatoire : la salle
        dans laquelle chercher. Elle retourne une liste des objets
        posés sur le sol de cette salle. Vous pouvez également
        préciser un second paramètre, sous la forme d'une chaîne,
        contenant la clé du prototype d'objet ou le type grâce
        auquel filtrer les résultats. Voir les exemples cidessous
        pour plus d'informations.

        Paramètres à préciser :

          * salle : la salle dans laquelle chercher
          * type_ou_prototype (optionnel) : paramètre pour filtrer la liste

        Exemples d'utilisation :

          # Retourne tous les objets posés dans la salle
          objets = objets(salle)
          # Retourne les objets dans la salle du prototype "pomme_rouge"
          pommes = objets(salle, "pomme_rouge")
          # Retourne les objets posés dans la salle de type "arme"
          armes = objets(salle, "+arme")
          # Si aucun objet n'est trouvé, retourne une liste vide

        """
        objets = [o for o in salle.objets_sol._objets]
        if type_ou_prototype:
            if type_ou_prototype.startswith("+"):
                nom_type = type_ou_prototype[1:]
                objets = [o for o in objets if o.est_de_type(nom_type)]
            else:
                cle_prototype = type_ou_prototype
                objets = [o for o in objets if o.cle == cle_prototype]

        return objets


    @staticmethod
    def objets_personnage(personnage, filtre=""):
        """Retourne une liste d'objets possédés par le personnage.

        Le filtre facultatif permet de ne retourner que certains objets
        spécifiques, en fonction de leur type ou de leur clé.

        Paramètres à préciser :

          * personnage : le personnage en question.
          * filtre (facultatif) : un ou plusieurs filtres.

        Le filtre est à préciser sous la forme d'une chaîne. Si on veut
        préciser plusieurs filtres, il faut les séparer par une
        accolade (&). Le filtre peut être soit une clé d'objet simple,
        soit un type d'objet précédé du signe '+'. Il existe également
        deux filtres particuliers :

          * *equipement : cherche uniquement dans l'équipement du personnage.
          * *inventaire : cherche uniquement dans l'inventaire.

        Si aucun filtre n'est précisé, le filtre utilisé est
        "*equipement&*inventaire", ce qui signifie "tous les objets
        de l'équipement et ceux possédés dans l'inventaire". Voir les
        exemples ci-dessous pour plus d'information.

        Exemples d'utilisation :

          # Retourne tous les objets possédés ou équipés par le personnage
          possedes = objets(personnage)
          # Ne retourne que les objets équipés
          objets = objets(personnage, "*equipement")
          # Ne retourne que les objets possédés (sans l'équipement)
          objets = objets(personnage, "*inventaire")
          # Retourne les objets équipes ou possédés de clé 'sabre_bois'
          objets = objets(personnage, "sabre_bois")
          # Ne retourne que les objets équipés de clé 'sabre_bois'
          objets = objets(personnage, "*equipement&sabre_bois")
          # Retourne tous les objets possédés de type 'fruit'
          objets = objets(personnage, "*inventaire&+fruit")

        """
        filtre = filtre or "*equipement&*inventaire"
        filtre = filtre.lower()
        filtres = filtre.split("&")
        objets = []
        if "*equipement" in filtres:
            objets.extend([o for o in personnage.equipement.equipes])
            filtres.remove("*equipement")
        if "*inventaire" in filtres:
            objets.extend([o for o in personnage.equipement.inventaire_simple])
            filtres.remove("*inventaire")

        for filtre in filtres:
            if filtre.startswith("+"):
                objets = [o for o in objets if o.est_de_type(filtre[1:])]
            else:
                objets = [o for o in objets if o.cle == filtre]

        return objets
