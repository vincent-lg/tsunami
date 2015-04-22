# -*-coding:Utf-8 -*
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


"""Fichier contenant la classe Guilde, détaillée plus bas."""

from math import ceil

from abstraits.obase import BaseObj
from corps.fonctions import valider_cle
from primaires.format.fonctions import supprimer_accents
from secondaires.crafting.atelier import Atelier
from secondaires.crafting.commande_dynamique import CommandeDynamique
from secondaires.crafting.exception import ExceptionCrafting
from secondaires.crafting.extension import Extension
from secondaires.crafting.progression import Progression
from secondaires.crafting.rang import Rang, RangIntrouvable
from secondaires.crafting.talent import Talent
from secondaires.crafting import type as def_type
from secondaires.crafting.type import Type

class Guilde(BaseObj):

    """Classe représentant une guilde.

    Dans le crafting, une guilde est une organisation, artisanale
    ou politique. Les guildes politiques ne sont que des organisations
    et permettent souvent de progresser grâce à des quêtes. Les
    guildes artisanales sont plus complexes, car elles gèrent des
    matières premières, une notion d'approvisionnement et d'opérations
    usuelles. Le détail des différents types de guilde se trouve
    à l'adresse http://redmine.kassie.fr/issues/130 .

    """

    enregistrer = True

    def __init__(self, cle):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.cle = cle
        self.nom = "une guilde"
        self.ouverte = False
        self.ateliers = []
        self.commandes = []
        self.types = []
        self.membres = {}
        self.rangs = []
        self.talents = {}
        self.extensions = []
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<Guilde {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

    @property
    def talents_ouverts_a_tous(self):
        """Retourne la liste des talents ouverts à tous."""
        return [t for t in self.talents.values() if t.ouvert_a_tous]

    @property
    def talents_fermes(self):
        """Retourne la liste des talents fermés (non ouverts à tous)."""
        return [t for t in self.talents.values() if not t.ouvert_a_tous]

    def ouvrir(self):
        """Ouverture de la guilde.

        Cette commande rend les commandes, talents, états, disponibles
        pour les joueurs. Elle doit donc être appelée soit à l'ouverture
        de la guilde en jeu, soit au moment de la récupération
        des guildes.

        """
        self.ouverte = True
        for talent in self.talents.values():
            importeur.perso.ajouter_talent(talent.cle, talent.nom,
                    talent.niveau, talent.difficulte, talent.ouvert_a_tous)

    def rejoindre(self, personnage):
        """Permet au personnage passé en paramètre de rejoindre la guilde.

        Cette méthode demande au personnage (joueur ou PNJ) passé
        en paramètre de rejoindre la guilde.

        Lève l'exception :
            GuildeSansRang si la guilde n'a aucun rang
            DejaMembre si le personnage est déjà membre de la guilde
            PointsGuildeInsuffisants si le membre manque de points de guilde

        """
        if len(self.rangs) == 0:
            raise GuildeSansRang("la guilde {} n'a aucun rang défini".format(
                    self.cle))

        if personnage in self.membres:
            raise DejaMembre("le personnage {} est déjà membre de " \
                    "la guilde {}".format(personnage, self.cle))

        rang = self.rangs[0]
        disponibles = importeur.crafting.get_points_guilde_disponibles(
                personnage)
        if disponibles < rang.points_guilde:
            raise PointsGuildeInsuffisants("le personnage {} n'a " \
                    "pas suffisamment de points de guilde ({} " \
                    "nécessaires contre {} disponibles)".format(
                    personnage, rang.points_guilde, disponibles))

        self.changer_rang(personnage, rang)

    def promouvoir(self, personnage):
        """Promeut un membre au rang suivant.

        Lève l'exception :
            GuildeSansRang si la guilde n'a aucun rang
            RangIntrouvable si le rang est introuvable
            NonMembre si le personnage n'est pas membre de la guilde
            PointsGuildeInsuffisants si le membre manque de points de guilde

        """
        if len(self.rangs) == 0:
            raise GuildeSansRang("la guilde {} n'a aucun rang défini".format(
                    self.cle))

        if personnage not in self.membres:
            raise NonMebre("le personnage {} n'est pas membre de " \
                    "la guilde {}".format(personnage, self.cle))

        progression = self.membres[personnage]
        rang = progression.rang

        # On cherche à identifier le rang suivant
        try:
            indice = self.rangs.index(rang)
        except ValueError:
            raise RangIntrouvable("le rang courant de {} dans la guilde " \
                    "{} est introuable".format(personnage, self.cle))

        try:
            suivant = self.rangs[indice + 1]
        except IndexError:
            raise RangIntrouvable("il n'y a pas de rang après {} " \
                    "dans la guilde {}".format(rang.cle, self.cle))

        disponibles = importeur.crafting.get_points_guilde_disponibles(
                personnage)
        if disponibles < suivant.points_guilde:
            raise PointsGuildeInsuffisants("le personnage {} n'a " \
                    "pas suffisamment de points de guilde ({} " \
                    "nécessaires contre {} disponibles)".format(
                    personnage, suivant.points_guilde, disponibles))

        self.changer_rang(personnage, suivant)
        return suivant

    def quitter(self, personnage):
        """Quitte la guilde.

        Lève l'exception :
            NonMembre si le personnage n'est pas membre de la guilde

        Déclare une partie des points de guilde récupérés en
        malus (5).

        """
        if personnage not in self.membres:
            raise NonMebre("le personnage {} n'est pas membre de " \
                    "la guilde {}".format(personnage, self.cle))

        progression = self.membres[personnage]
        points = progression.rang.total_points_guilde
        del self.membres[personnage]
        progressions = [p for p in importeur.crafting.membres.membres[
                personnage] if p.rang.guilde is not self]
        importeur.crafting.membres.membres[personnage] = progressions

        # Écriture du malus
        malus = ceil(points * 5 / 100)
        malus += importeur.crafting.membres.malus.get(personnage, 0)
        importeur.crafting.membres.malus[personnage] = malus

    def changer_rang(self, personnage, rang):
        """Change le rang du personnage précisé.

        À la différence des méthodes 'rejoindre', 'quitter', ou
        'promouvoir', cette méthode ne fait aucune vérification.

        """
        progression = Progression(personnage, rang)
        self.membres[personnage] = progression
        progressions = importeur.crafting.membres.membres.get(personnage, [])
        progressions = [p for p in progressions if p.rang.guilde is not self]
        progressions.append(progression)
        importeur.crafting.membres.membres[personnage] = progressions

    def get_rang(self, cle, exception=True):
        """Retourne le rang indiqué, si trouvé.

        Si le rang n'est pas trouvé, lève une exception ValueError,
        sauf si 'exception' est à False. Dans ce derneir cas,
        retourne simplement None.

        """
        cle = cle.lower()
        for rang in self.rangs:
            if rang.cle.lower() == cle:
                return rang

        if exception:
            raise ValueError("Rang {} introuvable".format(repr(cle)))

    def ajouter_rang(self, cle):
        """Ajoute le rang indiqué."""
        valider_cle(cle)
        if self.get_rang(cle, exception=False):
            raise ValueError("Le rang de clé {} existe déjà".format(
                    repr(cle)))

        rang = Rang(self, cle)
        self.rangs.append(rang)
        return rang

    def supprimer_rang(self, cle):
        """Supprime le rang dont la clé est indiquée.

        Si le rang en question comporte des membres, lève l'exception
        ValueError.

        """
        cle = cle.lower()
        for rang in list(self.rangs):
            if rang.cle.lower() == cle:
                # Vérifie qu'il n'y a pas de membres dans ce rang
                membres = [p for p in self.membres.values() if p.rang is rang]
                if len(membres) > 0:
                    s = "s" if len(membres) > 1 else ""
                    raise ValueError("Le rang {} possède {} membre{s}".format(
                            rang.cle, len(membres), s=s))

                self.rangs.remove(rang)
                rang.detruire()
                return

        raise ValueError("Rang {} introuvable".format(repr(cle)))

    def ajouter_talent(self, cle, nom, ouvert_a_tous=False):
        """Ajoute un talent à la guilde."""
        valider_cle(cle)
        if cle in importeur.perso.talents:
            raise ValueError("la clé de talent {} est déjà utilisée".format(
                    repr(cle)))

        if cle in self.talents:
            raise ValueError("la clé de talent {} existe déjà dans " \
                    "cette guilde".format(repr(cle)))

        talent = Talent(self, cle)
        talent.nom = nom
        talent.ouvert_a_tous = ouvert_a_tous
        self.talents[cle] = talent
        return talent

    def get_type(self, nom_type):
        """Cherche le type."""
        nom_type = supprimer_accents(nom_type).lower()
        for n_type in self.types:
            if supprimer_accents(n_type.nom).lower() == nom_type:
                return n_type

        raise ValueError("Le type de nom {} est introuvable.".format(
                repr(nçm_type)))

    def ajouter_type(self, nom_parent, nom_type):
        """Création du type précisé."""
        materiau = importeur.objet.get_type("matériau")
        outil = importeur.objet.get_type("outil")
        machine = importeur.objet.get_type("machine")

        try:
            parent = importeur.objet.get_type(nom_parent)
        except KeyError:
            raise ValueError("Le type parent {} est introuvable".format(
                    repr(nom_parent)))
        if not issubclass(parent, (materiau, outil, machine)):
            raise ValueError("Le type parent {} n'est pas de type " \
                    "matériau, outil ou machine".format(repr(nom_type)))

        nom_parent = parent.nom_type

        try:
            importeur.objet.get_type(nom_type)
        except KeyError:
            pass
        else:
            raise ValueError("le type {} existe déjà".format(
                    repr(nom_type)))

        type = Type(self, nom_parent, nom_type)
        self.types.append(type)
        importeur.crafting.enregistrer_YML()
        classe = type.creer()
        setattr(def_type, classe.__name__, classe)
        return type

    def get_extension(self, nom, exception=True):
        """Retourne l'extension précisée."""
        nom = supprimer_accents(nom).lower()

        for extension in self.extensions:
            if supprimer_accents(extension.nom).lower() == nom:
                return extension

        if exception:
            raise ValueError("L'extension {} n'existe pas".format(repr(nom)))

    def ajouter_extension(self, editeur, nom, nom_type="chaîne"):
        """Ajout d'une extension."""
        editeur = editeur.lower()
        if self.get_extension(nom, False):
            raise ValueError("L'extension {} existe déjà".format(repr(nom)))

        if editeur not in ("salle", "pnj", "objet"):
            raise ValueError("Type d'éditeur {} inconnu".format(
                    repr(editeur)))

        extension = Extension(self, editeur, nom)
        extension.type = nom_type
        self.extensions.append(extension)
        return extension

    def supprimer_extension(self, nom):
        """Supprime l'extension précisée."""
        extension = self.get_extension(nom)
        self.extensions.remove(extension)
        extension.detruire()

    def get_atelier(self, cle):
        """Retourne, si trouvé, l'atelier.

        Lève une exception ValueError si l'atelier n'est pas trouvé.

        """
        for atelier in self.ateliers:
            if atelier.cle.lower() == cle.lower():
                return atelier

        raise ValueError("Atelier {} introuvable".format(repr(cle)))

    def ajouter_atelier(self, cle):
        """Ajoute un atelier à la guilde."""
        if cle in [a.cle for a in self.ateliers]:
            raise AtelierExiste("Cette clé d'atlier est déjà utilisée".format(
                    repr(cle)))

        atelier = Atelier(self, cle)
        self.ateliers.append(atelier)
        return atelier

    def supprimer_atelier(self, cle):
        """Supprime l'atelier depuis la clé indiquée."""
        atelier = self.get_atelier(cle)
        self.ateliers.remove(atelier)
        atelier.detruire()

    def get_commande(self, nom, exception=True):
        """Cherche la commande indiquée."""
        sa_nom = supprimer_accents(nom).lower()
        for commande in self.commandes:
            if supprimer_accents(commande.nom_complet).lower() == sa_nom:
                return commande

        if exception:
            raise ValueError("La commande {} est introuvable".format(
                    repr(nom)))

    def ajouter_commande(self, nom):
        """Ajout d'une commande.

        Le nom est sous la forme 'nom_francais/nom_anglais'. Il
        peut être aussi sous la forme
        'commande:parametre_francais/parametre_anglais'.

        """
        if self.get_commande(nom, exception=False):
            raise ValueError("La commande {} existe déjà".format(repr(nom)))

        parent = ""
        if ":" in nom:
            noms = nom.split(":")
            parent = ":".join(noms[:-1])
            importeur.interpreteur.trouver_commande(parent)
            nom = noms[-1]

        if nom.count("/") != 1:
            raise ValueError("Précisez <nom_français/nom_anglais>")

        nom_francais, nom_anglais = nom.split("/")
        nom_francais = nom_francais.strip()
        nom_anglais = nom_anglais.strip()
        commande = CommandeDynamique(self, parent, nom_francais, nom_anglais)
        self.commandes.append(commande)
        return commande

    def supprimer_commande(self, nom):
        """Supprime la commande indiquée."""
        commande = self.get_commande(nom)
        if not commande.utilisable:
            self.commandes.remove(commande)
            commande.detruire()
        else:
            raise ValueError("Cette commande est déjà ouverte")

class GuildeSansRang(ExceptionCrafting):

    """Exception levée quand la guilde n'a aucun rang défini."""

    pass

class DejaMembre(ExceptionCrafting):

    """Exception levée quand le personnage est déjà membre de la guilde."""

    pass

class NonMembre(ExceptionCrafting):

    """Exception levée quand le personnage n'est pas membre de la guilde."""

    pass

class PointsGuildeInsuffisants(ExceptionCrafting):

    """Exception levée quand l'opération attendue attend trop de points.

    Les opérations consommant des points de guilde sont le fait
    de rejoindre une guilde ou de changer de rang.

    """

    pass

class AtelierExiste(ExceptionCrafting):

    """Exception levée quand l'atelier précisé existe déjà."""
