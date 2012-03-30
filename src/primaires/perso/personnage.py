# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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

import random

from abstraits.obase import BaseObj
from corps.fonctions import lisser
from primaires.interpreteur.file import FileContexte
from primaires.interpreteur.groupe.groupe import *

from .race import Race
from .equipement import Equipement
from .quetes import Quetes
from .stats import Stats

class Personnage(BaseObj):
    
    """Classe représentant un personnage.
    
    C'est une classe abstraite. Elle doit être héritée pour faire des joueurs
    et PNJs. Ces autres classes peuvent être également héritées, à leur tour.
    
    Note: on précise bel et bien un nom de groupe, mais on ne l'ajoute pas à
    ObjetID puisqu'il s'agit d'une classe abstraite.
    
    """
    
    _nom = "personnage"
    _version = 5
    
    def __init__(self):
        """Constructeur d'un personnage"""
        BaseObj.__init__(self)
        self.nom = ""
        self.nom_groupe = "pnj"
        self.contextes = FileContexte(self) # file d'attente des contexte
        self.langue_cmd = "francais"
        self._salle = None
        self.stats = Stats(self)
        self._prompt = "Vit   {stats.vitalite}     Man   {stats.mana}     " \
                "End   {stats.endurance}"
        self.equipement = None
        self._race = None
        self.genre = "aucun"
        
        # Quêtes
        self.quetes = Quetes(self)
        
        # Talents et sorts
        self.talents = {}
        self.sorts = {}
        
        # Etat
        self._cle_etat = ""
        
        # Position occupé
        self.position = ""
        self.occupe = ""
        
        # Nveau prmiaire et niveaux secondaires
        self.niveau = 1
        self.niveaux = {}
        self.xp = 0 # xp dans le niveau principal
        self.xps = {}
        
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
                hasattr(self.stats,nom_attr):
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
        return self._prompt.format(stats=self.stats)
    
    @property
    def grp(self):
        """Retourne le groupe du joueur."""
        groupes = type(self).importeur.interpreteur.groupes
        return groupes[self.nom_groupe]
    
    def _get_cle_etat(self):
        return self._cle_etat
    def _set_cle_etat(self, cle):
        """On vérifie que l'état existe."""
        if cle:
            try:
                etat = type(self).importeur.perso.etats[cle]
            except KeyError:
                raise KeyError(cle)
        
        self._cle_etat = cle
    cle_etat = property(_get_cle_etat, _set_cle_etat)
    
    @property
    def etat(self):
        """Retourne l'état correspondant à 'cle_etat'."""
        if self._cle_etat:
            return type(self).importeur.perso.etats[self._cle_etat]
        else:
            return None
    
    @property
    def poids_max(self):
        """Retourne le poids que peut porter le personnage."""
        return self.stats.force * 5
    
    def get_etat(self):
        """Retourne l'état visible du personnage."""
        if self.position and not self.occupe:
            return self.get_position().message
        
        if self.occupe:
            return self.get_position().etat + " " + \
                    self.salle.details[self.occupe].positions[self.position]
        
        return "est là"
    
    def get_position(self):
        """Retourne la position actuelle du personnage."""
        return type(self).importeur.perso.positions[self.position]
    
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
        return self.vitalite == 0
    
    def detruire(self):
        """Méthode appelée lors de la destruction du personage.
        -   On supprime le personnage de la liste des personnages du squelette
        -   On supprime le personnage de la salle
        
        """
        BaseObj.detruire(self)
        if self.equipement:
            self.equipement.squelette.personnages.remove(self)
        if self.salle:
            self.salle.retirer_personnage(self)
    
    def get_nom_pour(self, personnage):
        """Retourne le nom pour le personnage passé en paramètre."""
        raise NotImplementedError
    
    def envoyer(self, msg, *personnages, **kw_personnages):
        """Méthode envoyer"""
        raise NotImplementedError
    
    def envoyer_lisser(self, chaine, *personnages, **kw_personnages):
        """Méthode redirigeant vers envoyer mais lissant la chaîne."""
        self.envoyer(lisser(chaine), *personnages, **kw_personnages)
    
    def deplacer_vers(self, sortie):
        """Déplacement vers la sortie 'sortie'"""
        self.agir("deplacer")
        salle = self.salle
        salle_dest = salle.sorties.get_sortie_par_nom(sortie).salle_dest
        if not self.est_immortel() and salle_dest.zone.fermee:
            self << "|err|Vous ne pouvez pas aller par là...|ff|"
            return
        
        sortie = salle.sorties.get_sortie_par_nom(sortie)
        fermer = False
        
        if not self.est_immortel() and sortie.porte and \
                sortie.porte.verrouillee:
            self << "Cette porte semble fermée à clef.".format(
                    sortie.nom_complet)
            return
        
        # Si la porte est fermée (pas verrouillée), on l'ouvre
        if not self.est_immortel() and sortie.porte and \
                sortie.porte.fermee and not sortie.porte.verrouillee:
            self << "Vous ouvrez {}.".format(sortie.nom_complet)
            self.salle.envoyer("{{}} ouvre {}.".format(sortie.nom_complet),
                    self)
            sortie.porte.ouvrir()
            fermer = True
        
        # On appelle l'événement sort.avant
        salle.script["sort"]["avant"].executer(vers=sortie.nom,
                salle=salle, personnage=self, destination=salle_dest)
        
        if sortie.cachee:
            for personnage in salle.personnages:
                msg = "{{personnage}} s'en va vers... Vous ne voyez pas " \
                        "très bien où."
                if personnage.est_immortel():
                    msg = "{{personnage}} s'en va vers {sortie}."
                msg = msg.format(sortie=sortie.nom_complet)
                if personnage is not self:
                    personnage.envoyer(msg, personnage=self)
        else:
            salle.envoyer("{{}} s'en va vers {}.".format(sortie.nom_complet),
                    self)
        
        if fermer:
            self.salle.envoyer("Vous entendez une porte se refermer.",
                    self)
            sortie.porte.fermer()
            self.envoyer("Vous passez {} et refermez derrière vous.".format(
                    sortie.nom_complet))
        
        # On appelle l'évènement sort.apres
        salle.script["sort"]["apres"].executer(vers=sortie.nom,
                salle=salle, personnage=self, destination=salle_dest)
        
        self.salle = salle_dest
        sortie_opp = sortie.sortie_opposee
        nom_opp = sortie_opp and sortie_opp.nom or None
        
        # On appelle l'évènement arrive.avant
        if self.salle is salle_dest:
            salle_dest.script["arrive"]["avant"].executer(
                    depuis=nom_opp, salle=salle_dest, personnage=self)
        
        self.envoyer(self.salle.regarder(self))
        salle_dest.envoyer("{} arrive.", self)
        
        # On appelle l'évènement arrive.apres
        if self.salle is salle_dest:
            salle_dest.script["arrive"]["apres"].executer(
                    depuis=nom_opp, salle=salle_dest, personnage=self)
    
    def get_talent(self, cle_talent):
        """Retourne la valeur du talent ou 0 si le talent n'est pas trouvé."""
        return self.talents.get(cle_talent, 0)
    
    def pratiquer_talent(self, cle_talent):
        """Pratique le talent et peut potentiellement l'apprendre.
        
        Retourne la connaissance actuelle du personnage dans le talent.
        
        """
        talent = type(self).importeur.perso.talents[cle_talent]
        avancement = self.get_talent(cle_talent)
        configuration = type(self).importeur.perso.cfg_talents
        apprendre = talent.estimer_difficulte(configuration, avancement)
        if random.random() < apprendre:
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
        etat = self.etat
        if etat:
            etat.peut_faire(cle_action)
    
    def mourir(self):
        """Méthode appelée quand le personage meurt."""
        self.cle_etat = ""
        combat = type(self).importeur.combat.get_combat_depuis_salle(
                self.salle)
        if combat and self in combat.combattants:
            combat.supprimer_combattant(self)
        
        self << "Vous vous effondrez sur le sol."
        self.salle.envoyer("{} s'effondre sur le sol.", self)
    
    def gagner_xp(self, niveau=None, xp=0):
        """Le personnage gagne de l'expérience.
        
        Paramètres attendus :
            niveau -- le nom du niveau (si principal, None)
            xp -- le nombre d'xp reçus
        
        Le nombre d'xp est un nombre absolu, pas relatif en fonction
        du niveau. Voir gagner_xp_rel.
        
        """
        if niveau and niveau not in type(self).importeur.perso.niveaux:
            raise ValueError("le niveau {} n'existe pas".format(niveau))
        
        xp_actuel = self.xps[niveau] if niveau else self.xp
        niveau_actuel = self.niveaux[niveau] if niveau else self.niveau
        nb_niveaux = type(self).importeur.perso.gen_niveaux.nb_niveaux
        if xp > 0 and niveau_actuel >= nb_niveaux:
            return
        
        grille = type(self).importeur.perso.gen_niveaux.grille_xp
        xp_nec = grille[niveau_actuel - 1][1]
        if niveau:
            self.xps[niveau] = self.xps.get(niveau, 0) + xp
            xp_total = self.xps[niveau]
        else:
            self.xp += xp
            xp_total = self.xp
        
        nb_gagne = 0
        while niveau_actuel < nb_niveaux and xp_total >= xp_nec:
            if niveau:
                self.niveaux[niveau] = self.niveaux.get(niveau, 0) + 1
                self.xps[niveau] = self.xps.get(niveau, 0) - xp_nec
                xp_total = self.xps[niveau]
            else:
                self.niveau += 1
                self.xp -= xp_nec
                xp_total = self.xp
            niveau_actuel += 1
            xp_nec = grille[niveau_actuel - 1][1]
            nb_gagne += 1
        
        nom_niveau = type(self).importeur.perso.niveaux[niveau].nom if \
                niveau else "principal"
        self << "Vous recevez {} xp dans le niveau {}.".format(xp, nom_niveau)
        if nb_gagne > 0:
            nb = str(nb_gagne) if nb_gagne > 1 else "un"
            x = "x" if nb_gagne > 1 else ""
            if niveau:
                self << "|rg|Vous gagnez {} niveau{} en {}.|ff|".format(nb, x,
                        nom_niveau)
            else:
                self << "|rg|Vous gagnez {} niveau{}.|ff|".format(nb, x)
    
    def ramasser(self, objet, exception=None, qtt=1):
        """Ramasse l'objet objet.
        
        On cherche à placer l'objet de préférence :
        1   Dans un conteneur dédié à ce type
        2   Dans un autre conteneur
        3   Dans les mains du joueur si le reste échoue.
        
        """
        for o in self.equipement.inventaire:
            if o is not exception and o.est_de_type("conteneur") and \
                    o.prefere_type(objet):
                o.conteneur.ajouter(objet, qtt)
                return o
        
        for o in self.equipement.inventaire:
            if o is not exception and o.est_de_type("conteneur") and \
                    o.accepte_type(objet):
                o.conteneur.ajouter(objet, qtt)
                return o
        
        if qtt > 1:
            return None
        
        for membre in self.equipement.membres:
            if membre.peut_tenir() and membre.tenu is None:
                membre.tenu = objet
                objet.contenu = self.equipement.tenus
                return membre
        
        return None
    
    def tick(self):
        """Méthode appelée à chaque tick (chaque minute)."""
        stats = {
            "vitalite": "force",
            "mana": "intelligence",
            "endurance": "agilite",
        }
        for nom, liee in stats.items():
            stat = self.stats[nom]
            courante = stat.courante
            max = stat.max
            if courante < max:
                courante_liee = self.stats[liee].courante
                plus = int(courante_liee * 0.9)
                stat.courante = stat.courante + plus
    
    def regarder(self, personnage):
        """personnage regarde self."""

        equipement = self.equipement
        msg = "Vous regardez {} :\n".format(self.get_nom_pour(personnage))
        objets = []
        for membre in equipement.membres:
            objet = membre.equipe and membre.equipe[-1] or membre.tenu
            if objet:
                objets.append("{} [{}]".format(membre.nom.capitalize(),
                        objet.nom_singulier))
        
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
        
        self.envoyer("{} vous regarde.", personnage)
        personnage.salle.envoyer("{} regarde {}.", personnage, self)
        return msg
