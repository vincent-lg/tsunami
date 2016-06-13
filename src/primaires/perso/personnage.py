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


"""Fichier contenant la classe Personnage, détaillée plus bas."""

from fractions import Fraction
import random
from textwrap import wrap

from abstraits.obase import BaseObj
from corps.aleatoire import varier
from corps.fonctions import lisser
from primaires.affection.affection import Affection
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.file import FileContexte
from primaires.interpreteur.groupe.groupe import *
from primaires.objet.conteneur import SurPoids
from primaires.scripting.structure import StructureSimple

from .race import Race
from .equipement import Equipement
from .quetes import Quetes
from .stats import Stats
from .exceptions.stat import DepassementStat
from .etats import Etats
from .prompt import prompts

class Personnage(BaseObj):

    """Classe représentant un personnage.

    C'est une classe abstraite. Elle doit être héritée pour faire des joueurs
    et PNJs. Ces autres classes peuvent être également héritées, à leur tour.

    Note: on précise bel et bien un nom de groupe, mais on ne l'ajoute pas à
    ObjetID puisqu'il s'agit d'une classe abstraite.

    """

    _nom = "personnage"
    _version = 7

    def __init__(self):
        """Constructeur d'un personnage"""
        BaseObj.__init__(self)
        self.nom = ""
        self.nom_groupe = "pnj"
        self.contextes = FileContexte(self) # file d'attente des contexte
        self.langue_cmd = "francais"
        self._salle = None
        self.stats = Stats(self)
        self.prompts_selectionnes = []
        self.prompts = {}
        self.equipement = None
        self._race = None
        self.genre = "aucun"

        # Faim et soif
        self.soif = 0
        self.faim = 0
        self.estomac = 0 # Maxi : 3 kg

        # Quêtes
        self.quetes = Quetes(self)

        # Talents et sorts
        self.talents = {}
        self.l_talents = {}
        self.malus = 0
        self.points_malus = 0
        self._element = ""
        self.sorts = {}
        self.sorts_verrouilles = []
        self.sorts_oublies = []
        self.points_tribut = 0

        # Etat
        self.etats = Etats(self)
        self.super_invisible = False
        self.affections = {}

        # Noyade
        self.degre_noyade = 0

        # Niveau primaire et niveaux secondaires
        self.niveau = 1
        self.niveaux = {}
        self.xp = 0 # xp dans le niveau principal
        self.xps = {}

        # Système de tips
        self.tips = False

        self.pk = True
        self._construire()

    def __getnewargs__(self):
        """Retourne les arguments à passer au constructeur"""
        return ()

    def __lshift__(self, msg):
        """Redirige vers 'envoyer'"""
        self.envoyer(msg)
        return self

    def __getattr__(self, nom_attr):
        """Cherche l'attribut dans 'self.stats."""
        if nom_attr.startswith("_") or nom_attr == "stats":
            pass
        elif hasattr(self, "stats") and hasattr(self.stats,
                    nom_attr):
            return getattr(self.stats, nom_attr)

        raise AttributeError("le type {} n'a pas d'attribut {}".format(
                type(self), nom_attr))

    def __setattr__(self, nom_attr, val_attr):
        """Si nom_attr est dans 'self.stats', modifie 'self.stats'"""
        if not nom_attr.startswith("_") and hasattr(self, "stats") and \
                nom_attr in self.stats.to_dict:
            setattr(self.stats, nom_attr, val_attr)
        else:
            BaseObj.__setattr__(self, nom_attr, val_attr)

    def _get_contexte_actuel(self):
        """Retourne le contexte actuel, c'est-à-dire le premier de la file"""
        return self.contextes.actuel
    def _set_contexte_actuel(self, nouveau_contexte):
        """Ajoute le nouveau contexte à la file des contextes.
        Note : la file peut très bien être manipulée par un contexte qui
        utilisera dans ce cas les méthodes 'ajouter' et 'retirer' de la file
        des contextes.

        """
        self.contextes.ajouter(nouveau_contexte)
    contexte_actuel = property(_get_contexte_actuel, _set_contexte_actuel)

    def _get_salle(self):
        return self._salle
    def _set_salle(self, salle):
        """Redéfinit la salle du joueur.
        On en profite pour :
        -   s'assurer que le joueur a bien été retiré de son ancienne
            salle, si existante
        -   ajouter le joueur dans la nouvelle salle

        """
        anc_salle = self._salle
        if anc_salle:
            anc_salle.retirer_personnage(self)

        self._salle = salle

        if salle:
            salle.ajouter_personnage(self)
    salle = property(_get_salle, _set_salle)

    def _get_race(self):
        return self._race
    def _set_race(self, race):
        self._race = race

        for stat in race.stats:
            t_stat = getattr(self.stats, "_{}".format(stat.nom))
            t_stat.defaut = stat.defaut
            t_stat.courante = stat.defaut

        self.lier_equipement(race.squelette)
    race = property(_get_race, _set_race)

    @property
    def genres_possibles(self):
        """Retourne les genres disponibles pour le personnage"""
        if self.race is not None:
            return self.race.genres.str_genres
        else:
            return "masculin, féminin"

    def est_masculin(self):
        """Retourne True si le personnage est masculin, False sinon"""
        if self.race is not None:
            try:
                return self.race.genres[self.genre] == "masculin"
            except KeyError:
                return self.genre == "aucun"
        else:
            return self.genre == "masculin" or self.genre == "aucun"

    def est_feminin(self):
        return not self.est_masculin()

    @property
    def prompt(self):
        """Retourne le prompt formatté"""
        selectionne = self.prompts_selectionnes and \
                self.prompts_selectionnes[0] or "défaut"
        prompt = self.prompts.get(selectionne)
        prompt = prompts[selectionne].calculer(self, prompt)
        if self.super_invisible:
            prompt = "[i] " + prompt

        return prompt

    @property
    def grp(self):
        """Retourne le groupe du joueur."""
        groupes = type(self).importeur.interpreteur.groupes
        return groupes[self.nom_groupe]

    @property
    def etat(self):
        """Retourne le dernier état ou None."""
        if self.etats:
            return self.etats[-1]

        return None

    @property
    def poids(self):
        """Retourne le poids du personnage."""
        return self.equipement and self.equipement.poids or 0

    @property
    def poids_max(self):
        """Retourne le poids que peut porter le personnage."""
        return self.stats.force * 5

    @property
    def nom_unique(self):
        return self.nom

    @property
    def points_apprentissage(self):
        """Retourne les points d'apprentissages du personnage."""
        return sum(v for v in self.talents.values()) + self.points_malus

    @property
    def points_apprentissage_max(self):
        return importeur.perso.get_points_apprentissage(self)

    @property
    def argent_total(self):
        """Retourne l'argent contenu dans l'inventaire."""
        total = 0
        if not self.equipement:
            return total

        for o, qtt in self.equipement.inventaire.iter_objets_qtt():
            if o.est_de_type("argent"):
                total += qtt * o.valeur

        return total

    @property
    def points_entrainement_max(self):
        """Retourne le nombre de points d'entraînement total."""
        return importeur.perso.gen_niveaux.points_entrainement_disponibles(
                self.niveau)

    @property
    def points_entrainement_consommes(self):
        """Retourne le nombre de points d'entraînement consommés."""
        return importeur.perso.gen_niveaux.points_entrainement_consommes(self)

    @property
    def points_entrainement(self):
        """Retourne le nombre de points d'entraînement du personnage."""
        nb = self.points_entrainement_max - \
                self.points_entrainement_consommes
        if nb < 0:
            nb = 0

        return nb

    @property
    def nb_mains_libres(self):
        """Retourne le nombre de mains libres de self."""
        nb = 0
        if self.equipement is None:
            return nb

        for membre in self.equipement.membres:
            if membre.peut_tenir() and not membre.tenu and \
                    not membre.equipe:
                nb += 1

        return nb

    def possede_type(self, type_objet):
        """Retourne le premier objet du type indiqué ou None.

        Pour chaque objet dans l'inventaire du personnage, on
        cherche l'objet de type spécifié. Ce eput être un type parent
        (par exemple, on recherche tous les types vêtement).

        """
        if self.equipement is None:
            return None

        inventaire = self.equipement.inventaire
        for objet in inventaire:
            if objet.est_de_type(type_objet):
                return objet

        return None

    def _get_element(self):
        """Retourne l'élément."""
        return self._element
    def _set_element(self, element):
        """Change l'élément (chaîne vide pour effacer)."""
        if element:
            if element not in ("eau", "air", "terre", "feu"):
                raise ValueError("élément {} inconnu".format(repr(element)))
        else:
            element = ""

        self._element = element
        if element and not self.est_immortel():
            for cle, niveau in tuple(self.talents.items()):
                talent = importeur.perso.talents.get(cle)
                if talent and talent.cle_niveau == "combat" and niveau > 15:
                    self.talents[cle] = 15
    element = property(_get_element, _set_element)

    @property
    def armure(self):
        """Retourne l'armure globale calculée sur l'équipoement."""
        armure = 0
        if self.equipement is None:
            return armure

        for membre in self.equipement.membres:
            for objet in membre.equipe:
                if objet.est_de_type("armure"):
                    armure += random.randint(objet.encaissement_fixe,
                            objet.encaissement_fixe + \
                            objet.encaissement_variable)

        return armure

    def peut_voir(self, personnage):
        """Retourne True si peut voir le personnage, False sinon."""
        if self.est_immortel():
            return True

        salle = self.salle
        if not salle.voit_ici(self):
            return False

        return not personnage.super_invisible

    def sans_prompt(self):
        if self.controle_par:
            self.controle_par.sans_prompt()

    def get_etat(self):
        """Retourne l'état visible du personnage."""
        if self.etat:
            return self.etat.message_visible()

        return "est là"

    def get_armes(self):
        """Retourne les armes portées par le personnage.
        Ces armes sont celles portées.

        """
        armes = []
        for membre in self.equipement.membres:
            objet = membre.equipe and membre.equipe[-1] or None
            if objet and objet.est_de_type("arme"):
                armes.append(objet)

        return tuple(armes)

    def lier_equipement(self, squelette):
        """Crée un nouvel équipement pour le personnage en fonction
        du squelette.

        """
        self.equipement = Equipement(self, squelette)

    def get_nom(self, nombre):
        """Retourne le nom du personnage"""
        return self.nom

    def get_nom_etat(self, personnage, nombre):
        """Retourne le nom et un état par défaut."""
        return self.nom + " est là"

    def est_immortel(self):
        """Retourne True si le personnage est immortel.

        Note : cette information se trouve dans le groupe du personnage.

        """
        return IMMORTELS & self.grp.flags != 0

    def est_mort(self):
        """Retourne True si le personnage est mort, False sinon."""
        if not self.e_existe:
            return True

        return self.stats.vitalite == 0 or "mort" in self.etats

    def est_vivant(self):
        return not self.est_mort()

    def est_connecte(self):
        return False

    def est_en_combat(self):
        """Retourne True si le personnage est en combat, False sinon."""
        combat = importeur.combat.combats.get(self.salle.ident)
        if combat is None:
            return False

        return self in combat.combattants

    def selectionner_prompt(self, prompt):
        """Sélectionne le prompt du nom indiqué.

        Par exemple : personnage.selectionner_prompt("combat")

        """
        if self.prompts_selectionnes and self.prompts_selectionnes[0] == \
                prompt:
            return

        selectionnes = [p for p in self.prompts_selectionnes if p != prompt]
        selectionnes.insert(0, prompt)
        self.prompts_selectionnes[:] = selectionnes

    def deselectionner_prompt(self, prompt):
        """Déselectionne le prompt indiqué.

        Par exemple : personnage.deselectionner_prompt("combat")

        """
        if not self.prompts_selectionnes:
            return

        selectionnes = [p for p in self.prompts_selectionnes if p != prompt]
        self.prompts_selectionnes[:] = selectionnes

    def deselectionner_tous_prompts(self):
        """Déselectionne tous les prompts."""
        self.prompts_selectionnes[:] = []

    def peut_etre_attaque(self):
        """Retourne True si le personnage peut être attaéqué.

        Cela dépend de l'état.

        """
        if self.etat:
            return self.etat.peut_etre_attaque

        return True

    def detruire(self):
        """Méthode appelée lors de la destruction du personage.
        -   On supprime le personnage de la liste des personnages du squelette
        -   On supprime le personnage de la salle

        """
        BaseObj.detruire(self)
        if self.equipement and self.equipement.squelette and \
                self in self.equipement.squelette.personnages:
            self.equipement.squelette.personnages.remove(self)
        if self.salle:
            self.salle.retirer_personnage(self)

        if self.equipement:
            for membre in self.equipement.membres:
                for objet in membre.equipe:
                    try:
                        importeur.objet.supprimer_objet(objet.identifiant)
                    except KeyError:
                        pass
                if membre.tenu and hasattr(membre.tenu, "identifiant"):
                    try:
                        importeur.objet.supprimer_objet(
                                membre.tenu.identifiant)
                    except KeyError:
                        pass

    def get_nom_pour(self, personnage, retenu=True):
        """Retourne le nom pour le personnage passé en paramètre."""
        raise NotImplementedError

    def envoyer(self, msg, *personnages, **kw_personnages):
        """Méthode envoyer"""
        raise NotImplementedError

    def envoyer_lisser(self, chaine, *personnages, **kw_personnages):
        """Méthode redirigeant vers envoyer mais lissant la chaîne."""
        self.envoyer(lisser(chaine), *personnages, **kw_personnages)

    def deplacer_vers(self, sortie, escalade=False, nage=False, fuite=True):
        """Déplacement vers la sortie 'sortie'"""
        salle = self.salle
        o_sortie = self.salle.sorties.get_sortie_par_nom(sortie)
        salle_dest = salle.sorties.get_sortie_par_nom(sortie).salle_dest

        # Calcul de l'endurance
        if escalade:
            end = min(8, o_sortie.diff_escalade * 2)
        elif nage:
            end = 10
        else:
            end = self.salle.terrain.perte_endurance_dep

        # Vérifie que le personnage peut se déplacer (hook)
        retours = importeur.hook["personnage:peut_deplacer"].executer(
                self, salle_dest, o_sortie, end)

        if any(not r for r in retours):
            return

        # Modification de l'endurance
        retours = importeur.hook["personnage:calculer_endurance"].executer(
                self, end)
        n_endurance = end
        if retours:
            n_endurance = retours[0]

        if not self.est_en_combat():
            self.agir("bouger")

        if o_sortie.diff_escalade and o_sortie.direction in ("haut", "bas") \
                and not self.est_immortel() and not escalade:
            self << "|err|Vous devez escalader pour aller dans cette " \
                    "direction.|ff|"
            return

        if self.salle.nom_terrain in ("aquatique", "subaquatique") and \
                not self.est_immortel() and not nage and not \
                o_sortie.diff_escalade:
            self << "|err|Vous devez nager pour aller dans cette " \
                    "direction.|ff|"
            return

        try:
            self.stats.endurance -= n_endurance
        except DepassementStat:
            self << "|err|Vous êtes trop fatigué.|ff|"
            return

        if not self.est_immortel() and salle_dest.zone.fermee:
            self << "|err|Vous ne pouvez pas aller par là...|ff|"
            return

        if escalade:
            valeur_talent = self.get_talent("escalade")
            # note : la proba d'apprentissage du talent diminue si la pente
            # est trop facile par rapport au talent déjà possédé.
            # Si la connaissance dépasse la difficulté de plus de deux niveaux,
            # on divise par quatre la proba d'apprentissage
            if (valeur_talent / 10 > (o_sortie.diff_escalade + 2)):
                diviseur_proba = 4
            # Si la connaissance dépasse la difficulté de plus d'un niveau,
            # on divise par deux la proba d'apprentissage
            elif (valeur_talent / 10 > (o_sortie.diff_escalade + 1)):
                diviseur_proba = 2
            else:
                diviseur_proba = 1
            valeur_talent = self.pratiquer_talent("escalade", diviseur_proba)
            # on rajoute une valeur entre -10 et +10 au talent aléatoirement
            # ainsi à partir de 10 en-dessous de la difficulté fois 10, on
            # commence à avoir une petite chance (si on est nu). À partir de
            # 10 au-dessus de la difficulté fois 10, on ne peut plus échouer
            # (si on est nu).
            tentative = varier(valeur_talent, 10)
            importeur.salle.logger.debug(
                "{} essaye d'escalader (réussir={}, difficulté={})".format(
                self.nom, round(tentative / 10, 2), o_sortie.diff_escalade))
            reussir = tentative / 10 >= o_sortie.diff_escalade
            if not reussir:
                self.tomber()
                return

        if nage:
            reussir = self.essayer_nage(self.salle, salle_dest)
            if not reussir:
                self << "|err|Vous battez des bras et des jambes mais " \
                        "n'avancez pas.|ff|"
                self.salle.envoyer("{} bat des bras et des jambes mais " \
                        "n'avance pas.", self)
                return

        sortie = salle.sorties.get_sortie_par_nom(sortie)
        sortie_opp = sortie.sortie_opposee
        nom_opp = sortie_opp and sortie_opp.nom or ""
        fermer = False

        if not self.est_immortel() and sortie.porte and \
                sortie.porte.verrouillee:
            self << "Cette porte semble fermée à clef.".format(
                    sortie.nom_complet)
            return

        if not self.est_immortel() and sortie.porte and \
                sortie.porte.fermee and not sortie.porte.verrouillee and \
                not salle_dest.peut_entrer(self):
            self << "|err|Vous ne pouvez ouvrir cette porte.|ff|"
            return

        if self.est_en_combat():
            reussite = self.essayer_fuir()
            if reussite:
                self << "Vous vous enfuyez..."
                self.etats.retirer("combat")
                combat = type(self).importeur.combat.get_combat_depuis_salle(
                        self.salle)
                combat.supprimer_combattant(self)
            else:
                self << "|err|Vous ne parvenez pas à vous enfuir !|ff|"
                return

        # On appelle l'évènement sort des affections du personnage
        for affection in list(self.affections.values()):
            duree = affection.duree
            force = affection.force
            affection.affection.script["sort"].executer(personnage=self,
                    salle=salle, force=force, duree=duree)

        # On appelle l'évènement 'sort' des affections de la salle
        for affection in list(salle.affections.values()):
            duree = affection.duree
            force = affection.force
            affection.affection.script["sort"].executer(personnage=self,
                    salle=salle, force=force, duree=duree)

        # On appelle l'événement sort.avant de la salle
        salle.script["sort"]["avant"].executer(vers=sortie.nom,
                salle=salle, personnage=self, destination=salle_dest)
        # On appelle l'événement personnage.sort si nécessaire
        if hasattr(self, "script"):
            if self.salle is salle_dest:
                personnage.script["sort"].executer(vers=sortie.nom,
                        salle=salle, destination=salle_dest, pnj=self)

        # On appelle les pnj.part des PNJs de la salle
        for perso in self.salle.personnages:
            if perso is not self and hasattr(perso, "script") and \
                    perso.peut_voir(self):
                perso.script["part"].executer(vers=sortie.nom,
                        destination=salle_dest, pnj=perso, personnage=self)

        # Si la porte est fermée (pas verrouillée), on l'ouvre
        if not self.est_immortel() and sortie.porte and \
                sortie.porte.fermee and not sortie.porte.verrouillee:
            self << "Vous ouvrez {}.".format(sortie.nom_complet)
            self.salle.envoyer("{{}} ouvre {}.".format(sortie.nom_complet),
                    self)
            sortie.porte.ouvrir()
            fermer = True

        verbe = "s'en va vers"
        if escalade:
            verbe = "escalade"
        elif nage:
            verbe = "nage vers"
        else:
            retours = importeur.hook["personnage:verbe_deplacer"].executer(
                    self, salle_dest)
            if retours:
                verbe = retours[0]

        if sortie.cachee:
            for personnage in salle.personnages:
                msg = "{{personnage}} {verbe}... Vous ne voyez pas " \
                        "très bien où."
                if personnage.est_immortel():
                    msg = "{{personnage}} {verbe} {sortie}."
                msg = msg.format(sortie=sortie.nom_complet, verbe=verbe)
                if personnage is not self:
                    personnage.envoyer(msg, personnage=self)
        else:
            salle.envoyer("{{}} {} {}.".format(verbe, sortie.nom_complet),
                    self)

        # On appelle l'évènement sort.apres
        salle.script["sort"]["apres"].executer(vers=sortie.nom,
                salle=salle, personnage=self, destination=salle_dest)

        if fermer:
            self.salle.envoyer("Vous entendez une porte se refermer.",
                    self)
            sortie.porte.fermer()
            self.envoyer("Vous passez {} et refermez derrière vous.".format(
                    sortie.nom_complet))

        # Plonger sous l'eau
        if salle.nom_terrain != "subaquatique" and \
                salle_dest.nom_terrain == "subaquatique":
            self.plonger()

        # Emerger de sous l'eau
        if salle.nom_terrain == "subaquatique" and \
                salle_dest.nom_terrain != "subaquatique":
            self.emerger()

        self.salle = salle_dest

        # On appelle l'hook de déplacement
        importeur.hook["personnage:deplacer"].executer(
                self, salle_dest, o_sortie, end)

        # On appelle l'évènement entre.avant
        if self.salle is salle_dest:
            salle_dest.script["entre"]["avant"].executer(
                    depuis=nom_opp, salle=salle_dest, personnage=self)

        verbe = "arrive"
        retours = importeur.hook["personnage:verbe_arriver"].executer(
                    self, salle_dest)
        if retours:
            verbe = retours[0]

        self.envoyer(self.salle.regarder(self))
        salle_dest.envoyer("{{}} {verbe}.".format(verbe=verbe), self)

        # Envoi de tips
        if salle_dest.magasin:
            self.envoyer_tip("Entrez %lister%|vr| pour voir les produits " \
                    "en vente dans ce magasin.")
        if salle_dest in importeur.commerce.questeurs:
            self.envoyer_tip("Entrez %questeur%|vr| pour interagir avec " \
                    "le questeur présent.")
        if salle.nom_terrain != "subaquatique" and \
                salle_dest.nom_terrain == "subaquatique":
            self.envoyer_tip("Vous êtes sous l'eau. " \
                    "Attention au manque d'air !")

        # On appelle l'évènement entre.apres
        if self.salle is salle_dest:
            salle_dest.script["entre"]["apres"].executer(
                    depuis=nom_opp, salle=salle_dest, personnage=self)

            if salle.nom_zone != salle_dest.nom_zone:
                salle_dest.zone.script["entre"].executer(
                    origine=salle, salle=salle_dest, personnage=self)

            # On appelle l'évènement 'sort' des affections de la salle
            for affection in list(salle_dest.affections.values()):
                duree = affection.duree
                force = affection.force
                affection.affection.script["entre"].executer(personnage=self,
                        salle=salle_dest, force=force, duree=duree)

        # On appelle l'événement personnage.entre si nécessaire
        if hasattr(self, "script"):
            if self.salle is salle_dest:
                self.script["entre"].executer(depuis=nom_opp,
                        salle=salle_dest, pnj=self)

        # On appelle les pnj.arrive des PNJs de la salle
        for perso in salle_dest.personnages:
            if perso is not self and hasattr(perso, "script") and \
                    perso.peut_voir(self):
                perso.script["arrive"].executer(depuis=nom_opp, pnj=perso,
                        personnage=self, salle=salle)
                importeur.hook["pnj:arrive"].executer(perso,
                        self)

    def noyable(self):
        """Retourne True si le personnage est noyable, False sinon."""
        return not self.est_immortel()

    def essayer_nage(self, origine, destination):
        """Essaye de nager et retourne un booléen de réussite.

        Le calcul compare la connaissance du talent nage, légèrement varié,
        au pourcentage porté par le joueur. Il est donc complètement lié
        à la force du joueur et à ce qu'il porte.

        Pour aider les nouveaux cela dit, le calcul est plus favorable :
        -   Si le joueur tente d'aller vers le bord
        -   Si le joueur est relativement bas niveau (entre 1 et 30).

        """
        pc_poids = varier(int(self.poids / self.poids_max * 100), 5)
        connaissance = varier(self.pratiquer_talent("nage"), 15)

        # Si le joueur va vers le bord
        if destination.nom_terrain not in ("aquatique", "subaquatique"):
            connaissance += varier(40, 10)

        # Si le joueur est relativement bas niveau
        if self.niveau < 30:
            connaissance += varier(30 - self.niveau, 5)

        reussir = connaissance >= pc_poids
        return reussir

    def get_talent(self, cle_talent):
        """Retourne la valeur du talent ou 0 si le talent n'est pas trouvé."""
        return self.talents.get(cle_talent, 0)

    def pratiquer_talent(self, cle_talent, proba=1):
        """Pratique le talent et peut potentiellement l'apprendre.

        Retourne la connaissance actuelle du personnage dans le talent.
        L'argument facultatif proba permet d'introduire une probabilité
        supplémentaire.

        """
        talent = type(self).importeur.perso.talents[cle_talent]
        avancement = self.get_talent(cle_talent)
        if self.points_apprentissage >= self.points_apprentissage_max \
                or (cle_talent in self.l_talents \
                and self.l_talents[cle_talent] <= avancement):
            return avancement

        if avancement and avancement >= 15 and self._element and \
                talent.cle_niveau == "combat" and not self.est_immortel():
            return avancement

        configuration = type(self).importeur.perso.cfg_talents
        apprendre = talent.estimer_difficulte(configuration, avancement)
        if random.random() < apprendre and random.random() < 1 / proba:
            avancement += 1
            self.talents[cle_talent] = avancement
            self.envoyer("Vous progressez dans l'apprentissage du " \
                    "talent {}.".format(talent.nom))

        return avancement

    def pratiquer_sort(self, cle_sort):
        """Pratique un sort et peut l'apprendre."""
        sort = type(self).importeur.magie.sorts[cle_sort]
        maitrise = self.sorts.get(cle_sort, 0)
        if maitrise >= 100:
            return maitrise
        restant = (100 - maitrise) / 100
        difficulte = (100 - sort.difficulte) / 100
        if random.random() < difficulte * restant:
            maitrise += 1
            self.sorts[cle_sort] = maitrise
            self.envoyer("Vous sentez votre confiance grandir.")

        return maitrise

    def agir(self, cle_action):
        """Fait l'action cle_action.

        Si l'état interdit de faire cette action, une exception est levée.

        """
        for etat in self.etats:
            etat.peut_faire(cle_action)

    def mourir(self, adversaire=None, recompenser=True):
        """Méthode appelée quand le personage meurt."""
        combat = type(self).importeur.combat.get_combat_depuis_salle(
                self.salle)
        if combat and self in combat.combattants:
            combat.supprimer_combattant(self)

        self.etats.ajouter("mort", vider=True)
        self.envoyer_tip("Vous reprendrez conscience d'ici 10 à 15 minutes.",
                "inconscience", True)

    def gagner_xp(self, niveau=None, xp=0, retour=True):
        """Le personnage gagne de l'expérience.

        Paramètres attendus :
            niveau -- le nom du niveau (si principal, None)
            xp -- le nombre d'xp reçus
            retour -- laisser à True par défaut

        Le nombre d'xp est un nombre absolu, pas relatif en fonction
        du niveau. Voir gagner_xp_rel.

        Retourne le nombre de niveaux gagnés.

        """
        if niveau and niveau not in type(self).importeur.perso.niveaux:
            raise ValueError("le niveau {} n'existe pas".format(niveau))

        if niveau and niveau not in self.niveaux:
            self.niveaux[niveau] = 1
            self.xps[niveau] = 0

        xp = int(xp)
        if xp <= 0:
            return

        xp_actuel = int(self.xps[niveau]) if niveau else int(self.xp)
        niveau_actuel = self.niveaux[niveau] if niveau else self.niveau
        nb_niveaux = type(self).importeur.perso.gen_niveaux.nb_niveaux
        if niveau_actuel >= nb_niveaux:
            return 0

        grille = list(importeur.perso.gen_niveaux.grille_xp)
        xp_nec = grille[niveau_actuel - 1][1]
        if niveau:
            self.xps[niveau] = self.xps[niveau] + xp
            xp_total = self.xps[niveau]
        else:
            self.xp += xp
            xp_total = self.xp

        nb_gagne = 0
        while niveau_actuel < nb_niveaux and xp_total >= xp_nec:
            if niveau:
                self.niveaux[niveau] = self.niveaux[niveau] + 1
                self.xps[niveau] = self.xps[niveau] - xp_nec
                xp_total = self.xps[niveau]
            else:
                self.niveau += 1
                self.xp -= xp_nec
                xp_total = self.xp
            niveau_actuel += 1
            xp_nec = grille[niveau_actuel - 1][1]
            nb_gagne += 1

        if hasattr(self, "script") and nb_gagne > 0:
            self.script["gagne_niveau"].executer(pnj=self)

        if not retour:
            return nb_gagne

        if niveau:
            niveau_actuel = self.niveaux[niveau]
            facteur = niveau_actuel / importeur.perso.gen_niveaux.nb_niveaux
            n_xp = xp - int((xp * facteur))
            principal_gagne = self.gagner_xp(None, n_xp, False)

        nom_niveau = type(self).importeur.perso.niveaux[niveau].nom if \
                niveau else "principal"
        if niveau:
            self << "Vous recevez {} xp dans le niveau {} et {} dans " \
                    "le niveau principal.".format(xp, nom_niveau, n_xp)
        else:
            self << "Vous recevez {} xp dans le niveau principal.".format(xp)

        if nb_gagne > 0:
            nb = str(nb_gagne) if nb_gagne > 1 else "un"
            x = "x" if nb_gagne > 1 else ""
            msg = "|rg|Vous gagnez "
            if niveau:
                msg += "{} niveau{} en {}".format(nb, x, nom_niveau)
                nb = str(principal_gagne) if principal_gagne > 1 else "un"
                x = "x" if nb_gagne > 1 else ""
                if principal_gagne > 0:
                    msg += " !|ff|\nVous gagnez {} niveau{}".format(nb, x)
            else:
                msg += "{} niveau{}".format(nb, x)
            msg += " !|ff|"
            self << msg
        elif niveau and principal_gagne > 0:
            nb = str(nb_gagne) if nb_gagne > 1 else "un"
            x = "x" if nb_gagne > 1 else ""
            msg = "|rg|Vous gagnez {} niveau{} !|ff|".format(nb, x)
            self << msg

    def gagner_xp_rel(self, niveau, pourcentage, niv_secondaire=None):
        """Gagne de l'XP relatif.

        Les paramètres à entrer sont :
            niveau -- le niveau attendu comme base de l'XP relative
            pourcentage -- le pourcentage d'XP du niveau gagné
            niv_secondaire -- le nom du niveau secondaire ou None.

        L'XP relative est calculée sur la base d'un pourcentage d'XP
        d'un certain niveau. Si le niveau est 10 et que le pourcentage
        est 5%, un joueur niveau 10 gagnera 5% de l'XP attendue.
        Mais un joueur ayant un niveau inférieur ou supérieur
        gagnera moins de 10% de SON niveau.
        Par exemple, un joueur niveau 8 gagnera quelque chose comme
        9% du niveau 8.

        Si le niveau_secondaire est None, l'XP est reçue en niveau principal.

        """
        p_niveau = self.niveau
        if niv_secondaire:
            if niv_secondaire not in importeur.perso.niveaux:
                raise ValueError("niveau secondaire {} inconnu".format(
                        niv_secondaire))

            p_niveau = self.niveaux.get(niv_secondaire, 1)

        # On calcul l'XP relative en se basant sur niveau et p_niveau
        xp = importeur.perso.gen_niveaux.calculer_xp_rel(niveau, pourcentage,
                p_niveau)
        if xp > 0:
            self.gagner_xp(niv_secondaire, xp)

    def gagner_stat(self, nom_stat):
        """Gagne un point dans une statistique.

        ATTENTION : si le nombre de points d'entraînement disponibles n'est
        pas suffisant, lève une exception ValueError.

        """
        if self.points_entrainement <= 0:
            raise ValueError("le personnage {} ne peut rien apprendre de " \
                    "plus".format(self))

        stat = self.stats[nom_stat]
        if stat.base >= stat.marge_max:
            raise ValueError("la stat {} de {} est déjà au maximum".format(
                    nom_stat, self))

        stat.courante = stat.courante + 1

        # On entraîne la stat liée
        liee = importeur.perso.cfg_stats.entrainement_liees.get(nom_stat)
        if liee:
            stat_liee = self.stats[liee]
            stat_liee.courante = stat_liee.courante + stat.courante

    def retirer(self, objet, qtt=1):
        """Retire l'objet indiqué de l'inventaire."""
        if self.equipement:
            for membre in self.equipement.membres:
                objets = list(membre.equipe) + [membre.tenu]
                for o in objets:
                    if hasattr(o, "conteneur"):
                        try:
                            qtt -= o.conteneur.retirer(objet, qtt)
                        except ValueError:
                            continue

                        if qtt <= 0:
                            break

                if qtt <= 0:
                    break

    def ramasser(self, objet, exception=None, qtt=1):
        """Ramasse l'objet objet.

        On cherche à placer l'objet de préférence :
        1   Dans un conteneur dédié à ce type
        2   Dans un autre conteneur
        3   Dans les mains du joueur si le reste échoue.

        """
        for o in self.equipement.inventaire:
            if o is not objet and o is not exception and o.est_de_type(
                    "conteneur") and o.prefere_type(objet) and \
                    o.peut_contenir(objet, qtt):
                o.conteneur.ajouter(objet, qtt)
                return o

        for o in self.equipement.inventaire:
            if o is not objet and o is not exception and o.est_de_type(
                    "conteneur") and o.accepte_type(objet) and \
                    o.peut_contenir(objet, qtt):
                o.conteneur.ajouter(objet, qtt)
                return o

        if not objet.unique:
            return None

        if not self.est_immortel() and (self.poids + objet.poids) * qtt > \
                self.poids_max:
            raise SurPoids("C'est bien trop lourd !")

        for membre in self.equipement.membres:
            if membre.peut_tenir() and membre.tenu is None:
                membre.tenu = objet
                objet.contenu = self.equipement.tenus
                return membre

        return None

    def ramasser_ou_poser(self, objet, exception=None, qtt=1):
        """Ramasse ou pose un objet si ne peut pas prendre."""
        try:
            conteneur = self.ramasser(objet, exception, qtt)
            assert conteneur is not None
        except SurPoids as err:
            self.envoyer(str(err))
            self << "{} tombe sur le sol".format(
                    objet.get_nom(qtt).capitalize())
            self.salle.objets_sol.ajouter(objet, qtt)
        except AssertionError:
            self << "{} tombe sur le sol".format(
                    objet.get_nom(qtt).capitalize())
            self.salle.objets_sol.ajouter(objet, qtt)

    def affecte(self, cle, duree, force):
        """Affecte le personnage avec une affection.

        Si l'affection est déjà présente, la force est modulée.

        """
        affection = importeur.affection.get_affection("personnage", cle)
        if cle in self.affections:
            concrete = self.affections[cle]
            affection.moduler(concrete, duree, force)
        else:
            concrete = Affection(affection, self, duree, force)
            self.affections[cle] = concrete
            self._enregistrer()
            concrete.affection.executer_script("cree", concrete)
            concrete.prevoir_tick()

    def tick(self):
        """Méthode appelée à chaque tick (chaque minute)."""
        stats = {
            "vitalite": "force",
            "mana": "intelligence",
            "endurance": "agilite",
        }

        # Récupère le facteur de récupération
        facteurs = [e.get_facteur() for e in self.etats]
        facteur = 1
        for f in facteurs:
            facteur *= f

        for nom, liee in stats.items():
            stat = self.stats[nom]
            courante = stat.courante
            max = stat.max
            if courante < max:
                courante_liee = self.stats[liee].courante
                plus = int(courante_liee * facteur * 0.9)
                stat.courante = stat.courante + plus

        # Traitement des affections
        for affection in self.affections.values():
            affection.affection.dec_duree(affection)

        for cle, affection in list(self.affections.items()):
            if not affection.e_existe or affection.duree <= 0:
                del self.affections[cle]

    def envoyer_tip(self, message, cle=None, unique=False):
        """Envoie un message de tip (aide contextuel) au personnage."""
        if not self.tips:
            return

        if unique and not cle:
            raise ValueError("une tip unique avec une clé vide a été envoyée.")

        if unique and importeur.information.entree_tip(self, cle):
            return

        message = Commande.remplacer_mots_cles(self, message)
        paragraphes = []
        for paragraphe in message.split("\n"):
            paragraphes.append("\n      ".join(wrap(paragraphe, 69)))

        message = "\n      ".join(paragraphes).replace("|ff|", "|att|")
        message = "|att|TIP : " + message + "|ff|"
        self.envoyer(message)
        if unique:
            importeur.information.noter_tip(self, cle)

    def essayer_fuir(self):
        """Retourne True si le personnage peut fuir, False sinon.

        Il est pris pour acquis que le personnage est en combat.

        """
        fuite = 3
        if self.stats.endurance < fuite:
            self << "|err|Vous êtes trop fatigué.|ff|"
            return False
        self.stats.endurance -= fuite
        combat = type(self).importeur.combat.get_combat_depuis_salle(
                self.salle)
        combattu = combat.combattus[self]
        plus = random.randint(1, 25)
        return self.stats.agilite + plus >= combattu.stats.agilite

    def crier(self, message):
        """Crie le message dans la salle courante et les salles alentours.

        La transmission du message se fait grâce à des actions différées
        programmées pour s'exécuter instantanément (au prochain cycle du WD).

        """
        salle = self.salle
        self << "Vous vous écriez : " + message
        salle.envoyer("{} s'écrie : " + message, self)
        importeur.diffact.ajouter_action("yell({}).{}:{}".format(self.nom,
                salle.ident, id(message)), 0, self.act_crier, salle, [salle],
                message)

    def act_crier(self, salle, salles, message, dist=0):
        """Crie le message.

        On parle de salle et on transmet le message à
        toutes les salles autour de salle dans un rayon de 1. On appelle
        ensuite récursivement l'action.

        """
        if dist >= 8:
            return

        for chemin in salle.salles_autour(1).chemins:
            t_salle = chemin.destination
            if t_salle not in salles:
                salles.append(t_salle)
                t_salle.envoyer("{} s'écrie: {}".format(
                        self.get_distinction_audible(), message))
                importeur.diffact.ajouter_action("yell({}).{}:{}".format(
                        self.nom, t_salle.ident, id(message)), 0, self.act_crier,
                        t_salle, salles, message, dist + 1)

    def attaquer(self, personnage):
        """Attaque le personnage spécifié."""
        self.etats.ajouter("combat", vider=True)
        personnage.etats.ajouter("combat", vider=True)
        importeur.combat.creer_combat(self.salle,
                self, personnage)
        self.envoyer("Vous attaquez {}.", personnage)
        personnage.envoyer("{} vous attaque.", self)
        personnage.reagir_attaque(self)

    def reagir_attaque(self, personnage):
        """Réagit à l'attaque."""
        pass

    def tuer(self, victime):
        """Le personnage self vient de tuer la victime."""
        pass

    def regarder(self, personnage, notifier=True):
        """personnage regarde self."""
        equipement = self.equipement
        msg = ""
        if notifier:
            msg = "Vous regardez {} :".format(self.get_nom_pour(
                    personnage, retenu=False))
            if personnage.est_immortel():
                msg += self.ajout_description_pour_imm()
            msg += "\n"
        if hasattr(self, "description"):
            msg += "\n" + self.description.regarder(personnage=personnage,
                    elt=self) + "\n\n"

        # Affections
        aff_msg = []
        for cle, affection in self.affections.items():
            aff_msg.append(lisser(affection.affection.message(
                    affection)) + ".")

        if aff_msg:
            msg += "\n".join(aff_msg) + "\n\n"

        objets = []
        for membre in equipement.membres:
            # on affiche l'objet tenu prioritairement, sinon l'objet équipé
            objet = membre.tenu or membre.equipe and membre.equipe[-1] or None
            if objet:
                objets.append("{} [{}]".format(membre.nom.capitalize(),
                        objet.get_nom()))

        if self.est_masculin():
            genre = "Il"
            genre2 = "lui."
        elif self.est_feminin():
            genre = "Elle"
            genre2 = "elle."
        else:
            genre = "Il"
            genre2 = "lui."

        if not objets:
            msg += genre + " ne porte rien sur " + genre2
        else:
            msg += genre + " porte :\n\n  " + "\n  ".join(objets)

        if notifier:
            personnage.envoyer(msg, perso=self)
            self.envoyer("{} vous regarde.", personnage)
            personnage.salle.envoyer("{} regarde {}.", personnage, self)
        else:
            return msg

    def ajout_description_pour_imm(self):
        """ Complément d'information pour l'imm qui regarde le personnage """
        return ""

    def tomber(self):
        """self tombe de salles en salles."""
        def get_chute(salle, salles):
            """Cherche récursivement la dernière salle de la chute."""
            salles.append(salle)
            try:
                bas = salle.sorties["bas"]
                assert bas is not None
            except (KeyError, AssertionError):
                return salles

            if bas._diff_escalade:
                salle = bas.salle_dest
                return get_chute(salle, salles)
            return salles

        salles = get_chute(self.salle, [])
        if len(salles) == 1:
            self << "Vous tentez d'escalader la paroi... sans succès."
            self.salle.envoyer("{} tente d'escalader la paroi... " \
                    "sans succès.", self)
            return

        self << "Vous vacillez... |att|et tombez dans le vide !|ff|"
        self.salle.envoyer("{} vacille... et tombe dans le vide !", self)
        for salle in salles[1:-1]:
            salle.envoyer("Le corps de {} passe en plongeant devant vous.",
                    self)

        f_salle = salles[-1]
        self.salle = f_salle
        degats = int(self.vitalite_max / 3 * (len(salles) - 1))
        try:
            self.vitalite -= degats
        except DepassementStat:
            self.mourir()
            self.salle.envoyer("Le corps sans vie de {} s'écrase au sol.",
                    self)
        else:
            self << "Vous vous redressez en grimaçant."
            self.salle.envoyer("{} heurte le sol et se redresse.", self)

    def plonger(self):
        """self plonge."""
        self << "|att|Vous prenez une grande inspiration avant " \
                "de plonger.|ff|"
        nom = "noyade_" + self.nom_unique
        if self.noyable() and nom not in \
                importeur.diffact.actions:
            importeur.diffact.ajouter_action(nom, 5, self.act_noyer)

    def emerger(self):
        """self émerge."""
        self << "|att|Vous sortez la tête de l'eau et emplissez enfin " \
                "vos poumons d'air frais.|ff|"
        self.degre_noyade = 0

    def act_noyer(self):
        """Noie progressivement le joueur."""
        if self.salle.nom_terrain != "subaquatique":
            self.degre_noyade = 0
            return

        if self.est_mort():
            self.degre_noyade = 0
        else:
            self.degre_noyade += 5

        nom = "noyade_" + self.nom_unique
        importeur.diffact.ajouter_action(nom, 5, self.act_noyer)

        if self.est_mort():
            return

        if self.degre_noyade >= 90:
            try:
                self.vitalite = 0
            except DepassementStat:
                self << "|err|Vos poumons vides se remplissent d'eau...|ff|"
                self.mourir()
        elif self.degre_noyade == 80:
            self.sans_prompt()
            self << "|att|Vos poumons sont presque vides et vous commencez " \
                    "à étouffer.|ff|"
        elif self.degre_noyade == 60:
            self.sans_prompt()
            self << "|att|Il ne vous reste plus beaucoup d'air...|ff|"

    def get_structure(self):
        """Retourne la structure simple du personnage."""
        structure = StructureSimple()
        structure.groupe = self.nom_groupe
        structure.salle = self._salle
        structure.race = self._race and self._race.nom or ""
        structure.genre = self.genre
        structure.soif = Fraction(self.soif)
        structure.faim = Fraction(self.faim)
        structure.estomac = Fraction(self.estomac)
        structure.niveau = Fraction(self.niveau)
        structure.xp = Fraction(self.xp)
        structure.pk = Fraction(self.pk)
        return structure

    def appliquer_structure(self, structure):
        """Applique la structure passée en paramètre."""
        for cle, valeur in structure.donnees.items():
            if cle == "salle":
                self._salle = valeur
            elif cle == "race":
                race = importeur.perso.get_race(structure.race)
                self._race = race
            elif cle == "soif":
                self.soif = round(float(valeur), 2)
            elif cle == "faim":
                self.faim = round(float(valeur), 2)
            elif cle == "estomac":
                self.estomac = round(float(valeur), 2)
            elif cle == "niveau":
                self.niveau = int(valeur)
            elif cle == "xp":
                self.xp = int(valeur)
            elif cle == "pk":
                self.pk = bool(valeur)
