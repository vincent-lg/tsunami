# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la classe Transaction, détaillée plus bas."""

from math import ceil

from bases.exceptions.base import ExceptionMUD

class Transaction:

    """Cette classe représente une transaction entre deux acteurs.

    Certaines méthodes statiques sont utilisées sans créer de transaction :
        somme_argent(objets) -- retourne la somme totale
        get_argent(personnage) -- retourne les objets de type argent détenus

    D'autres méthodes nécessitent de créer une transaction. Pour
    créer une transaction, on n'utilise pas directement le constructeur
    mais la méthode initier_transaction.

    Les méthodes d'instances sont :
        payer() -- prélève l'argent dû à l'initiateur et paye le receveur

    """

    def __init__(self):
        """Constructeur, à ne pas appeler directement."""
        self.initiateur = None # l'initiateur de la transaction
        self.receveur = None # le receveur de la transaction
        self.somme = 0
        self.argent_donne = {}
        self.argent_rendu = {}

    def __repr__(self):
        return "<transaction entre {} et {} pour {}>".format(
                self.initiateur, self.receveur, self.somme)

    @staticmethod
    def aff_argent(argent):
        """Affiche l'argent."""
        if not argent:
            return "rien"

        argent = sorted(argent.items(), key=lambda a: a[0].valeur,
                reverse=True)
        argent = [a.get_nom(qtt) for a, qtt in argent]
        if len(argent) >= 2:
            return ", ".join(argent[:-1]) + " et " + argent[-1]

        return ", ".join(argent)

    @staticmethod
    def somme_argent(objets):
        """Retourne la somme de la valeur des objets.

        Le type attendu est un dictionnaire avec en clé l'objet (ou son
        prototype, indifféremment) et en valeur la quantité;

        """
        somme = 0
        for objet, qtt in objets.items():
            somme += objet.valeur * qtt

        return somme

    @staticmethod
    def get_argent(personnage):
        """Retourne tout l'argent détenu par le personnage.

        C'est un dictionnaire contenant tous les objets de type argent
        détenus par le personnage.

        """
        objets = personnage.equipement.inventaire_qtt
        objets = [(o, nb) for o, nb in objets if o.est_de_type("argent")]
        dct_objets = {}
        for o, nb in objets:
            dct_objets[o] = nb

        return dct_objets

    @classmethod
    def initier(cls, initiateur, receveur, somme):
        """Initie une transaction.

        Les paramètres à préciser sont :
            initiateur -- l'acteur initiant la transaction
            receveur -- le receveur de la transaction
            somme -- la somme de la transaction

        Les acteurs ne sont pas nécessairement des personnages.
        Dans le cas où un personnage achète un objet, la transaction
        initiée l'est par l'acheteur et le receveur est le magasin.

        """
        transaction = cls()
        transaction.initiateur = initiateur
        transaction.receveur = receveur
        transaction.somme = somme

        # On calcul l'argent dû et à rendre
        # Dans un cas simple, si on achète un produit à 1€ avec un billet de
        # 10€, l'argent donné est 10€ et l'argent rendu est 9€,
        # probablement décomposé en 9 pièces de 1€.
        if somme > 0:
            argent_dct = Transaction.get_argent(initiateur)
            somme_ini = Transaction.somme_argent(argent_dct)
            if somme_ini < somme:
                raise FondsInsuffisants("la somme d'argent de l'initiateur ({}) " \
                        "est insuffisante pour cette transaction".format(
                        somme_ini))

            # On trie la monnaie
            argent_tt = sorted(tuple(argent_dct.items()),
                    key=lambda t: t[0].valeur)
            argent_donne = []
            argent_rendu = []

            # On décompose la somme en fonction des valeurs
            t_somme = somme
            for argent, qtt in argent_tt:
                if t_somme == 0:
                    break

                valeur = argent.valeur
                valeur_max = valeur * qtt
                if valeur_max >= t_somme:
                    # On a le compte (ou plus), on s'arrête ici
                    qtt_min = t_somme // valeur
                    argent_donne.append((argent, qtt_min))
                    break
                else:
                    argent_donne.append((argent, qtt))
                    t_somme -= valeur_max

            somme_donnee = Transaction.somme_argent(dict(argent_donne))
        else:
            argent_donne = {}
            argent_rendu = []
            somme_donnee = 0

        # On s'occupe de rendre l'argent
        if somme_donnee > somme or somme < 0:
            monnaies = sorted([p for p in \
                    importeur.objet.prototypes.values() if p.est_de_type(
                    "argent") and p.valeur > 0], \
                    key=lambda m: m.valeur, reverse=True)
            t_somme = somme_donnee - somme
            for monnaie in monnaies:
                if t_somme == 0:
                    break

                d_somme = t_somme // monnaie.valeur
                if d_somme > 0:
                    argent_rendu.append((monnaie, d_somme))
                    t_somme -= d_somme * monnaie.valeur

        somme_rendue = Transaction.somme_argent(dict(argent_rendu))
        if somme != somme_donnee - somme_rendue:
            raise ValueError("la somme attendue ({}) n'est pas égale " \
                    "à la somme donnée ({}) moins la somme rendue ({})".format(
                    somme, somme_donnee, somme_rendue))

        transaction.argent_donne = dict(argent_donne)
        transaction.argent_rendu = dict(argent_rendu)

        return transaction

    def payer(self):
        """Prélève l'argent dû et paye le receveur."""
        # On liste les conteneurs contenant l'argent
        argent_donne = self.argent_donne.copy()
        conteneurs = [o for o in \
                self.initiateur.equipement.inventaire if o.est_de_type(
                "conteneur")]
        for conteneur in conteneurs:
            for objet, qtt in tuple(argent_donne.items()):
                t_qtt = conteneur.combien_dans(objet)
                if t_qtt >= qtt:
                    conteneur.conteneur.retirer(objet, qtt)
                    del argent_donne[objet]
                elif t_qtt > 0:
                    conteneur.conteneur.retirer(objet, t_qtt)
                    argent_donne[objet] = qtt - t_qtt

        # Le personnage doit ramasser l'argent à rendre
        for objet, qtt in self.argent_rendu.items():
            self.initiateur.ramasser_ou_poser(objet, qtt=qtt)

        if self.receveur:
            self.receveur.parent.zone.argent_total += self.somme

class FondsInsuffisants(ExceptionMUD):

    """Exception levée si les fonds ne sont pas suffisants pour acheter."""

    pass
