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


"""Fichier contenant la classe CommandeDynamique détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.parametre import Parametre
from primaires.scripting.script import Script
from primaires.scripting import types

class CommandeDynamique(BaseObj):

    """Classe décrivant les commandes dynamiques du crafting.

    Il existe deux types de commandes dynamiques : celles définies
    dans le scripting, qui font systématiquement référence à
    des éléments observables, et celles définies dans le crafting,
    qui sont plus configurables et permettent presque autant de
    liberté que les commandes standard.

    Ces dernières sont intégralement scriptables et permettent
    de configurer un véritable schéma, ce qui rend leur puissance
    encore plus importante. Le schéma est généralement convertit
    en paramètres scripting, ce qui permet une plus grande
    flexibilité.

    """

    nom_scripting = "la commande dynamique"

    def __init__(self, guilde, parent, nom_francais, nom_anglais):
        """Constructeur d'une commande dynamique."""
        BaseObj.__init__(self)
        self.guilde = guilde
        self.parent = parent
        self.nom_francais = nom_francais
        self.nom_anglais = nom_anglais
        self.commande = None # commande statique liée
        self._utilisable = False
        self.doit_etre_membre = True
        self._groupe = "pnj"
        self._nom_categorie = "divers"
        self._aide_courte = "à renseigner..."
        self.aide_longue = Description(parent=self, scriptable=False,
                callback="maj")
        self._schema = ""
        self.etats = {}
        self.script = ScriptCommande(self)
        self._construire()

    def __getnewargs__(self):
        return (None, "", "", "")

    def __repr__(self):
        parent = "{}:".format(self.parent) if self.parent else ""
        return "<CommandeDynamique '{}{}/{}'>".format(
                parent, self.nom_francais, self.nom_anglais)

    def __str__(self):
        parent = "{}:".format(self.parent) if self.parent else ""
        return parent + self.nom_francais + "/" + self.nom_anglais

    def __getstate__(self):
        dico_attr = self.__dict__.copy()
        if "commande" in dico_attr:
            del dico_attr["commande"]

        return dico_attr

    @property
    def nom_complet(self):
        """Retourne le nom complet (<parent>:)<fr>/<an>."""
        parent = "{}:".format(self.parent) if self.parent else ""
        return parent + self.nom_francais + "/" + self.nom_anglais

    def _get_aide_courte(self):
        return self._aide_courte
    def _set_aide_courte(self, aide):
        if len(aide) > 70:
            aide = aide[:70]
        self._aide_courte = aide
        self.maj()
    aide_courte = property(_get_aide_courte, _set_aide_courte)

    def _get_nom_categorie(self):
        return self._nom_categorie
    def _set_nom_categorie(self, categorie):
        self._nom_categorie = categorie
        self.maj()
    nom_categorie = property(_get_nom_categorie, _set_nom_categorie)

    def _get_groupe(self):
        return self._groupe
    def _set_groupe(self, groupe):
        self._groupe = groupe
        if self.commande:
            importeur.interpreteur.groupes.changer_groupe_commande(
                    self.commande.adresse, groupe)
    groupe = property(_get_groupe, _set_groupe)

    def _get_utilisable(self):
        return self._utilisable
    def _set_utilisable(self, utilisable):
        self._utilisable = utilisable
        if utilisable and self.commande is None:
            self.ajouter()
    utilisable = property(_get_utilisable, _set_utilisable)

    def _get_schema(self):
        return self._schema
    def _set_schema(self, schema):
        self._schema = schema
        if self.commande:
            self.commande.noeud.construire_arborescence(schema)
            self.maj_variables()
    schema = property(_get_schema, _set_schema)

    def maj_variables(self):
        """Met à jour les variables en fonction du schéma."""
        # Supprime les variables scripting
        evt = self.script["exécute"]
        for nom in list(evt.variables.keys()):
            if nom not in ("personnage", "commande"):
                evt.supprimer_variable(nom)

        noeud = self.commande.noeud
        masques = noeud.extraire_masques()

        # Parcourt des masques
        for masque in masques.values():
            n_type = getattr(type(masque), "nom", "")
            if n_type == "message":
                var = evt.ajouter_variable(masque.nom, "str")
                var.aide = "le message entré"
            elif n_type == "texte_libre":
                nom = masque.nom
                if nom == "texte_libre":
                    nom = "texte"

                var = evt.ajouter_variable(nom, "str")
                var.aide = "le texte libre entré"
            elif n_type == "nom_joueur":
                nom = masque.nom
                if nom == "nom_joueur":
                    nom = "joueur"

                var = evt.ajouter_variable(nom, "Personnage")
                var.aide = "le joueur dont le nom a été entré"
            elif n_type == "nombre":
                var = evt.ajouter_variable(masque.nom, "Fraction")
                var.aide = "le nombre entré"
            elif n_type in ("objet_equipe", "objet_inventaire", "objet_sol"):
                nom = masque.nom
                if nom in ("objet_equipe", "objet_inventaire", "objet_sol"):
                    nom = "objets"

                var = evt.ajouter_variable(nom, "list")
                var.aide = "la liste des objets entrée"

    def ajouter(self):
        """Ajoute la commande dans l'interpréteur.

        Il est préférable de faire cela après l'insertion des commandes
        statiques dans l'interpréteur, c'est-à-dire durant la phase de
        préparation du module.

        Si la commande a un parent, on va créer à la place son
        paramètre.

        """
        parent = None
        if self.parent:
            parent = importeur.interpreteur.trouver_commande(self.parent)
            commande = Parametre(self.nom_francais, self.nom_anglais)
        else:
            commande = Commande(self.nom_francais, self.nom_anglais)

        commande.schema = self.schema
        commande.groupe = self._groupe
        commande.nom_categorie = self.nom_categorie
        commande.aide_courte = self.aide_courte
        commande.aide_longue = str(self.aide_longue)
        commande.peut_executer = self.peut_executer
        commande.interpreter = self.interpreter
        if parent:
            parent.ajouter_parametre(commande)
        else:
            importeur.interpreteur.ajouter_commande(commande)

        self.commande = commande
        return commande

    def peut_executer(self, personnage):
        """Retourne True si le personnage peut ecuter la commande."""
        if self.doit_etre_membre:
            guilde = self.guilde
            if personnage not in guilde.membres:
                return False

        return True

    def interpreter(self, personnage, dic_masques):
        """Méthode outre-passant l'interprétation de la commande statique.

        On exécute le script de la commande, évènement 'exécute'.
        Les masques interprétés se retrouvent en partie dans les
        variables du script.

        """
        variables = {}

        # On parcourt tous les masques
        for masque in dic_masques.values():
            n_type = getattr(type(masque), "nom", "")
            if n_type == "message":
                variables[masque.nom] = masque.message
            elif n_type == "texte_libre":
                nom = masque.nom
                if nom == "texte_libre":
                    nom = "texte"

                variables[nom] = masque.texte
            elif n_type == "nom_joueur":
                nom = masque.nom
                if nom == "nom_joueur":
                    nom = "joueur"

                variables[nom] = masque.joueur
            elif n_type == "nombre":
                variables[masque.nom] = masque.nombre
            elif n_type in ("objet_equipe", "objet_inventaire", "objet_sol"):
                nom = masque.nom
                if nom in ("objet_equipe", "objet_inventaire", "objet_sol"):
                    nom = "objets"

                variables[nom] = masque.objets

        evenement = self.script["exécute"]
        for nom in evenement.variables:
            if nom in ("personnage", "commande"):
                continue

            if nom not in variables:
                variables[nom] = None

        evenement.executer(personnage=personnage, commande=self,
                **variables)

    def maj(self):
        """Mise à jour de la commande dynamique."""
        if self.commande:
            self.commande.nom_categorie = self.nom_categorie
            self.commande.aide_courte = self._aide_courte
            self.commande.aide_longue = str(self.aide_longue)

        # Ajout des états
        for cle, couple in self.etats.items():
            refus = couple[0]
            visible = couple[1]
            actions = couple[2]
            if cle in importeur.perso.etats:
                etat = importeur.perso.etats[cle]
            else:
                etat = importeur.perso.ajouter_etat(cle)

            etat.msg_refus = refus.capitalize()
            if not etat.msg_refus.endswith((".", "?", "!")):
                etat.msg_refus += "."

            etat.msg_visible = visible.lower().strip(" .?!")
            etat.act_autorisees = actions.split(" ")


class ScriptCommande(Script):

    """Script et évènements propres aux commandes dynamiques."""

    def init(self):
        """Initialisation du script"""
        # Événement exécute
        evt_execute = self.creer_evenement("exécute")
        evt_execute.aide_courte = "un personnage exécute la commande"
        evt_execute.aide_longue = \
            "Cet évènement est appelé quand un personnage exécute " \
            "la commande. Il doit en avoir le droit (être membre " \
            "de la guilde si la commande est limitée aux membres, " \
            "par exemple). Le schéma de la commande est interprété " \
            "et disponible grâce à des variables, listées ci-dessous."

        # Configuration des variables de l'évènement exécute
        var_perso = evt_execute.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage exécutant la commande"
        var_commande = evt_execute.ajouter_variable("commande", "Commande")
        var_commande.aide = "la commande-même (utile pour les blocs)"


types.Commande = CommandeDynamique
