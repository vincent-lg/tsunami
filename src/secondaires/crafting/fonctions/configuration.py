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


"""Fichier contenant la fonction configuration."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

# Fonction de conversion
def convertir_liste(liste):
    """Convertit la liste passée en argument, récursivement."""
    for i, elt in enumerate(liste):
        if isinstance(elt, (int, float)):
            liste[i] = Fraction(elt)
        elif isinstance(elt, list):
            convertir_liste(elt)


class ClasseFonction(Fonction):

    """Retourne la configuration d'une salle, personnage ou objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.configuration_salle, "Salle", "str")
        cls.ajouter_types(cls.configuration_personnage, "Personnage", "str")
        cls.ajouter_types(cls.configuration_objet, "Objet", "str")
        cls.ajouter_types(cls.configuration_chaine, "str", "str")

    @staticmethod
    def configuration_salle(salle, nom_configuration):
        """Retourne la configuration spécifique à une salle.

        La configuration est le résultat de l'extension du
        crafting. Chaque guilde peut configurer ses propres
        extensions d'éditeur. Cette fonction scripting permet de
        récupérer la valeur particulière. Si la configuration n'existe
        pas, retourne simplement une variable vide. Vous pouvez
        (et devriez) contrôler la validité de la variable retournée
        grâce à une simple condition (voir les exemples plus bas).

        Paramètres à préciser :

          * salle : la salle dont on veut récupérer la configuration
          * nom_configuration : le nom de la configuration (une chaîne)

        Si vous avez créé, dans une guilde, une extension dont le
        nom est "forme" s'appliquant à l'éditeur de salle, par exemple,
        vous pouvez récupérer la valeur pour chaque salle configurée
        grâce à l'instruction :

          forme = configuration(salle, "forme")

        Assurez-vous que la configuration existe. Si la configuration
        n'a pas été renseignée dans l'éditeur, elle sera vide.

          si forme:
              # forme n'est pas vide, vous pouvez travailler avec

        """
        donnee = getattr(importeur.crafting.configuration[salle],
                nom_configuration)

        if isinstance(donnee, (int, float)):
            donnee = Fraction(donnee)
        elif isinstance(donnee, list):
            # Déréférence
            donnee = list(donnee)
            convertir_liste(donnee)

        return donnee

    @staticmethod
    def configuration_personnage(personnage, nom_configuration):
        """Retourne la configuration spécifique à un personnage.

        La configuration est le résultat de l'extension du
        crafting. Chaque guilde peut configurer ses propres
        extensions d'éditeur. Cette fonction scripting permet de
        récupérer la valeur particulière. Si la configuration n'existe
        pas, retourne simplement une variable vide. Vous pouvez
        (et devriez) contrôler la validité de la variable retournée
        grâce à une simple condition (voir les exemples plus bas).

        Notez que si vous passez un joueur à cette fonction, le
        retour sera toujours vide (les joueurs n'ont pas de
        configuration crafting propre). Les PNJ retourneront la
        configuration spécifique de leur prototype, car la configuration
        est définie au niveau prototype, pas au niveau PNJ.

        Paramètres à préciser :

          * personnage : le personnage spécifique
          * nom_configuration : le nom de la configuration (une chaîne)

        Si vous avez créé, dans une guilde, une extension dont le
        nom est "humeur" s'appliquant à l'éditeur de PNJ, par exemple,
        vous pouvez récupérer la valeur pour chaque PNJ configuré
        grâce à l'instruction :

          humeur = configuration(pnj, "humeur")

        Assurez-vous que la configuration existe. Si la configuration
        n'a pas été renseignée dans l'éditeur, elle sera vide.

          si humeur:
              # humeur n'est pas vide, vous pouvez travailler avec

        """
        prototype = getattr(personnage, "prototype", None)
        if prototype is None:
            return None

        donnee = getattr(importeur.crafting.configuration[prototype],
                nom_configuration)

        if isinstance(donnee, (int, float)):
            donnee = Fraction(donnee)
        elif isinstance(donnee, list):
            # Déréférence
            donnee = list(donnee)
            convertir_liste(donnee)

        return donnee

    @staticmethod
    def configuration_objet(objet, nom_configuration):
        """Retourne la configuration spécifique à un objet.

        La configuration est le résultat de l'extension du
        crafting. Chaque guilde peut configurer ses propres
        extensions d'éditeur. Cette fonction scripting permet de
        récupérer la valeur particulière. Si la configuration n'existe
        pas, retourne simplement une variable vide. Vous pouvez
        (et devriez) contrôler la validité de la variable retournée
        grâce à une simple condition (voir les exemples plus bas).

        Notez que les objets retourneront la configuration
        spécifique de leur prototype, car la configuration est
        définie au niveau prototype, pas au niveau objet.

        Paramètres à préciser :

          * objet : l'objet spécifique
          * nom_configuration : le nom de la configuration (une chaîne)

        Si vous avez créé, dans une guilde, une extension dont le
        nom est "qualité" s'appliquant à l'éditeur d'objet, par exemple,
        vous pouvez récupérer la valeur pour chaque objet configuré
        grâce à l'instruction :

          qualite = configuration(objet, "qualité")

        Notez que le même système s'applique pour des types
        particuliers avec leurs extensions spécifiques.
        Assurez-vous que la configuration existe. Si la configuration
        n'a pas été renseignée dans l'éditeur, elle sera vide.

          si qualite:
              # qualite n'est pas vide, vous pouvez travailler avec

        """
        prototype = getattr(objet, "prototype", None)
        if prototype is None:
            return None

        donnee = getattr(importeur.crafting.configuration[prototype],
                nom_configuration)

        if isinstance(donnee, (int, float)):
            donnee = Fraction(donnee)
        elif isinstance(donnee, list):
            # Déréférence
            donnee = list(donnee)
            convertir_liste(donnee)

        return donnee

    @staticmethod
    def configuration_chaine(adresse, nom_configuration):
        """Retourne la configuration spécifique à un donnée variable.

        La configuration est le résultat de l'extension du
        crafting. Chaque guilde peut configurer ses propres
        extensions d'éditeur. Cette fonction scripting permet de
        récupérer la valeur particulière. Si la configuration n'existe
        pas, retourne simplement une variable vide. Vous pouvez
        (et devriez) contrôler la validité de la variable retournée
        grâce à une simple condition (voir les exemples plus bas).

        À la différence des autres usages, vous devez ici préciser
        en premier paramètre l'adresse d'une donnée sous la forme
        d'une chaîne : par exemple, "zone picte" pour récupérer
        l'extension de la zone Picte. Ce système permet de récupérer
        certaines données qui ne sont pas définies en crafting (comme
        les zones).

        Paramètres à préciser :

          * adresse : l'adresse de l'information configurée (une chaîne)
          * nom_configuration : le nom de la configuration (une chaîne)

        Si vous avez créé, dans une guilde, une extension dont le
        nom est "qualité" s'appliquant à l'éditeur de zone, par exemple,
        vous pouvez récupérer la valeur pour chaque zone configurée
        grâce à l'instruction :

          qualite = configuration("zone NOMZONE", "qualité")

        Notez que le même système s'applique pour des types
        particuliers avec leurs extensions spécifiques.
        Assurez-vous que la configuration existe. Si la configuration
        n'a pas été renseignée dans l'éditeur, elle sera vide.

          si qualite:
              # qualite n'est pas vide, vous pouvez travailler avec

        """
        adresse = adresse.lower()
        objets = {
                "prototype d'objet": importeur.objet._prototypes,
                "zone": importeur.salle.zones,
        }

        objet = None
        for nom, dictionnaire in objets.items():
            if adresse.startswith(nom + " "):
                cle = adresse[len(nom) + 1:]
                if cle not in dictionnaire:
                    raise ValueError("{} introuvable : {}".format(
                            nom, repr(cle)))

                objet = dictionnaire[cle]
                break

        if objet is None:
            raise ErreurExecution("Adresse {} introuvable".format(
                    repr(adresse)))

        donnee = getattr(importeur.crafting.configuration[objet],
                nom_configuration)

        if isinstance(donnee, (int, float)):
            donnee = Fraction(donnee)
        elif isinstance(donnee, list):
            # Déréférence
            donnee = list(donnee)
            convertir_liste(donnee)

        return donnee
