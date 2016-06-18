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


"""Fichier contenant la classe Evenement détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import supprimer_accents
from .espaces import Espaces
from .test import Test
from .variable import Variable

class Evenement(BaseObj):

    """Classe contenant un évènement de scripting.

    Un évènement est appelé dans une certaine situation. Un cas classique,
    par exemple, est un script défini dans un PNJ. Un évènement pourrait
    être appelé quand le PNJ est attaqué.

    Les évènements peuvent contenir des sous-évènements.

    Au niveau de la structure, un évènement contient :
    -   un dictionnaire de variables qui doivent IMPERATIVEMENT être
        TOUTES RENSEIGNEES quand on l'appelle ;
    -   un dictionnaire pouvant contenir des sous-évènements ;
    -   une suite de tests ;
    -   plusieurs espaces de nom.

    En outre, l'évènement garde en mémoire le script dont il est issu,
    qu'il soit sous-évènement ou non.

    Un évènement est constitué de plusieurs conditions (ou tests). Ces
    conditions sont propres aux variables qui les définissent. Un exemple
    simple :
        Evènement donner du PNJ tavernier_picte
            1   objet = pot_biere et nombre > 1
    La condition ci-dessus est appelée si le joueur donne plus d'un pot de
    bière au tavernier. Cela permet de ranger plus facilement nos lignes
    de script en fonction de plusieurs variables.

    Les évènements n'ayant aucune variable définie n'ont pas cette
    distinction en conditions pour le bâtisseur. Du point de vue du code,
    ils ont une seule condition appelée automatiquement.

    Les espaces de nom sont présents dans l'attribut 'espaces'. Chaque
    attribut de cet objet 'Espaces' est un espace de nom différent.
    Chaque espace se manipule comme un dictionnaire.

    Le constructeur d'un évènement prend en paramètre :
        script -- le script qui possède l'évènement
        nom -- le nom de l'évènement
        parent -- si c'est un sous-évènement, l'évènement parent (optionnel)

    """

    def __init__(self, script, nom, parent=None):
        """Constructeur d'un évènement"""
        BaseObj.__init__(self)
        self.script = script
        self.nom = nom
        self.aide_courte = "non précisée"
        self.aide_longue = "non précisée"
        self.parent = parent
        self.variables = {}
        self.__evenements = {}
        self.__tests = []
        self.__sinon = None
        self.espaces = Espaces(self)
        self.nom_acteur = "personnage"
        self._construire()

    @property
    def nom_complet(self):
        """Retourne le nom complet de l'événement."""
        ret = self.nom
        parent = self.parent
        while parent is not None:
            ret = parent.nom + "." + ret
            parent = parent.parent
        return ret

    def __getnewargs__(self):
        return (None, "")

    def __getstate__(self):
        """Ne sauvegarde pas les variables en fichier."""
        dico_attr = self.__dict__.copy()
        del dico_attr["espaces"]
        return dico_attr

    def __getitem__(self, evenement):
        """Retourne l'évènement correspondant au nom passé en paramètre."""
        evenement = supprimer_accents(evenement).lower()
        return self.__evenements[evenement]

    @property
    def appelant(self):
        """Retourne l'appelant, c'est-à-dire le parent du script."""
        return self.script.parent

    @property
    def tests(self):
        """Retourne une liste déréférencée des tests."""
        return list(self.__tests)

    @property
    def sinon(self):
        """Retourne le test sinon."""
        return self.__sinon

    @property
    def evenements(self):
        """Retourne un dictionnaire déréférencé des évènements."""
        return self.__evenements.copy()

    @property
    def nb_lignes(self):
        """Retourne le nombre de lignes de l'évènement et sous-évènements."""
        if not self.evenements:
            sinon = len(self.sinon.instructions) if self.sinon else 0
            return sum(len(t.instructions) for t in self.tests) + sinon
        else:
            return sum(e.nb_lignes for e in self.evenements.values())

    def deduire_variables(self, *args, **kwargs):
        """Déduit les variables en fonction des arguments nommés ou non.

        Cette méthode retourne un dictionnaire si elle a pu déterminer
        les variables. La façon la plus simple de l'utiliser est de
        préciser toutes les variables nommées de l'évènement, sauf
        une (une dont on ne connaît pas le nom). Dans ce cas,
        l'évènement sera capable de retrouver la variable manquante.

        Par exemple, si l'évènement a les variables 'personnage',
        'message' et 'salle', si on veut appeler cet évènement en
        connaissant 'personnage' et 'message', mais sans connaître
        'salle', on peut faire :
            variables = evenement.deduire_variables(objet,
                    personnage=personnage, message=chaine)
            evenement.executer(**variables)

        """
        variables = {}
        args = list(args)

        for nom, variable in self.variables.items():
            if nom in kwargs:
                variables[nom] = kwargs[nom]
            elif len(args) == 0:
                raise ValueError("Évènement {} : impossible de " \
                        "constituer une liste des variables, il n'y " \
                        "a pas de paramètres non nommés disponibles. " \
                        "Variables actuelles : {}".format(self.nom_complet,
                        variables))
            else:
                variables[nom] = args[0]
                del args[0]

        return variables

    def copier_depuis(self, evenement):
        """Copie le script self depuis l'évènement."""
        for sous in evenement.evenements.values():
            sa_sous = supprimer_accents(sous.nom).lower()
            if sa_sous in self.__evenements.keys():
                evt = self.__evenements[sa_sous]
            else:
                evt = self.creer_evenement(sous.nom)

            evt.copier_depuis(sous)

        tests = list(evenement.tests)
        if evenement.sinon:
            tests.append(evenement.sinon)

        for ancien_test in tests:
            sc_test = ancien_test.sc_tests
            if ancien_test.tests:
                self.ajouter_test(sc_test)
                nouveau_test = self.tests[-1]
            else:
                self.creer_sinon()
                nouveau_test = self.__sinon

            lignes = []
            for instruction in reversed(ancien_test.instructions):
                ligne = instruction.sans_couleurs
                lignes.insert(0, ligne)

            nouveau_test.ajouter_instructions("\n".join(lignes))

    def creer_sinon(self):
        """Création du test sinon si il n'existe pas."""
        if self.__sinon is None:
            self.__sinon = Test(self)

    def ajouter_test(self, chaine_test):
        """Ajoute un test à l'évènement."""
        test = Test(self, chaine_test)
        self.__tests.append(test)
        self._enregistrer()
        return len(self.__tests) - 1

    def supprimer_test(self, indice):
        """Retire le test à l'indice spécifié."""
        test = self.__tests[indice]
        test.detruire()
        del self.__tests[indice]
        self._enregistrer()

    def remonter_test(self, indice):
        """Remonte le test indiqué."""
        tests = self.__tests
        test = tests[indice]
        if indice == 0:
            raise ValueError("Impossible de remonter ce test.")

        tests[:] = tests[:indice - 1] + [test, tests[indice - 1]] + \
                tests[indice + 1:]
        self._enregistrer()

    def descendre_test(self, indice):
        """Descend le test indiqué."""
        tests = self.__tests
        test = tests[indice]
        if indice == len(tests) - 1:
            raise ValueError("Impossible de descendre ce test.")

        tests[:] = tests[:indice] + [tests[indice + 1], test] + tests[indice + 2:]
        self._enregistrer()

    def ajouter_variable(self, nom, type):
        """Ajoute une variable au dictionnaire des variables.

        On précise :
        nom -- le nom (ne doit pas être déjà utilisé)
        type -- le nom du type sous la forme d'une chaîne de caractère

        """
        if nom in self.variables:
            variable = self.variables[nom]
            variable.nom_type = type
            for evt in self.__evenements.values():
                evt.substituer_variable(nom, variable)

            return variable

        variable = Variable(self, nom, type)
        self.variables[nom] = variable
        self._enregistrer()
        for evt in self.__evenements.values():
            evt.substituer_variable(nom, variable)

        return variable

    def substituer_variable(self, nom, variable):
        """Modifie la variable nom."""
        self.variables[nom] = variable
        self._enregistrer()

    def supprimer_variable(self, nom):
        """Supprime, si trouvé, la variable."""
        if nom in self.variables:
            self._enregistrer()
            self.variables.pop(nom).detruire()

        for evt in self.__evenements.values():
            evt.supprimer_variable(nom)

    def creer_evenement(self, evenement):
        """Crée et ajoute l'évènement dont le nom est précisé en paramètre.

        L'évènement doit être une chaîne de caractères non vide. Si
        l'évènement existe, le retourne. Sinon, retourne le créé.

        """
        if not evenement:
            raise ValueError("Un nom vide a été passé en paramètre de " \
                    "creer_evenement.")

        sa_evenement = supprimer_accents(evenement).lower()

        self._enregistrer()
        if sa_evenement in self.__evenements.keys():
            evt = self.evenements[sa_evenement]
            evt.nom = evenement
            evt.script = self.script
            evt.parent = self
            return evt

        nouv_evenement = Evenement(self.script, evenement, self)
        self.__evenements[sa_evenement] = nouv_evenement

        return nouv_evenement

    def supprimer_evenement(self, evenement):
        """Supprime l'évènement en le retirant de son parent."""
        evenement = supprimer_accents(evenement).lower()
        self.__evenements.pop(evenement).detruire()

    def renommer_evenement(self, ancien, nouveau):
        """Renomme un évènement.

        Ldes paramètres à entrer sont :

            ancien -- l'ancien nom de l'évènement
            nouveau -- le nouveau nom de l'évènement

        """
        evt = self.__evenements.pop(ancien)
        evt.nom = nouveau
        self.__evenements[nouveau] = evt
        self._enregistrer()

    def executer(self, forcer=False, **variables):
        """Exécution de l'évènement."""
        # On écrit le nouvel espace ainsi pour éviter l'enregistrement
        object.__setattr__(self, "espaces", Espaces(self))
        self.espaces.variables.update(variables)
        var_manquantes = tuple(v for v in self.variables \
                if v not in self.espaces.variables)
        if var_manquantes:
            raise ValueError("Des variables manquent à l'appel ({}).".format(
                    ", ".join(var_manquantes)))

        # On cherche le bon test
        for test in self.__tests:
            if test.tester(self, forcer):
                test.executer_instructions(self)
                return 1

        if self.sinon and self.sinon.tester(self, forcer):
            self.sinon.executer_instructions(self)

        return 0

    def detruire(self):
        """Destruction de l'évènement."""
        BaseObj.detruire(self)
        for variable in self.variables.values():
            variable.detruire()

        for evenement in self.__evenements.values():
            evenement.detruire()

        for test in self.__tests:
            test.detruire()

        if self.__sinon:
            self.__sinon.detruire()
