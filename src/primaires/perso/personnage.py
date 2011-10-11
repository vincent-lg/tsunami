# -*-coding:Utf-8 -*
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

from abstraits.id import ObjetID, propriete_id
from bases.collections.enr_dict import EnrDict
from primaires.interpreteur.file import FileContexte
from primaires.interpreteur.groupe.groupe import *

from .race import Race
from .equipement import Equipement
from .quetes import Quetes
from .stats import Stats

class Personnage(ObjetID):
    
    """Classe représentant un personnage.
    C'est une classe abstraite. Elle doit être héritée pour faire des joueurs
    et PNJ. Ces autres classes peuvent être également héritées, à leur tour.
    
    Note: on précise bel et bien un nom de groupe, mais on ne l'ajoute pas à
    ObjetID puisqu'il s'agit d'une classe abstraite.
    
    """
    
    groupe = "personnages"
    sous_rep = "personnages"
    _nom = "personnage"
    _version = 4
    
    def __init__(self):
        """Constructeur d'un personnage"""
        ObjetID.__init__(self)
        self.nom = ""
        self.nom_groupe = "pnj"
        self.contextes = FileContexte(self) # file d'attente des contexte
        self.langue_cmd = "francais"
        self._salle = None
        self.stats = Stats()
        self._prompt = "Vit   {stats.vitalite}     Man   {stats.mana}     " \
                "End   {stats.endurance}"
        self.equipement = None
        self._race = None
        self.genre = "aucun"
        
        # Quêtes
        self.quetes = Quetes(self)
        self._construire()
        
        # Talents
        self.talents = EnrDict(self)
    
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
            ObjetID.__setattr__(self, nom_attr, val_attr)
    
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
    @propriete_id
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
        self.enregistrer()
        
        if salle:
            salle.ajouter_personnage(self)
    
    salle = property(_get_salle, _set_salle)
    
    def _get_race(self):
        return self._race
    def _set_race(self, race):
        race = race.get_objet()
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
            return self.race.genres[self.genre] == "masculin" or \
                    self.genre == "aucun"
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
    
    def lier_equipement(self, squelette):
        """Crée un nouvel équipement pour le personnage en fonction
        du squelette.
        
        """
        self.equipement = Equipement(self, squelette)
    
    def get_nom(self, nombre):
        """Retourne le nom du personnage"""
        return self.nom
    
    def get_nom_etat(self, nombre):
        """Retourne le nom et un état par défaut."""
        return self.nom + " est là"
    
    def est_immortel(self):
        """Retourne True si le personnage est immortel.
        
        Note : cette information se trouve dans le groupe du personnage.
        
        """
        return IMMORTELS & self.grp.flags != 0
    
    def detruire(self):
        """Méthode appelée lors de la destruction du personage.
        -   On supprime le personnage de la liste des personnages du squelette
        
        """
        if self.equipement:
            self.equipement.squelette.personnages.remove(self)
    
    def envoyer(self, msg):
        """Méthode envoyer"""
        raise NotImplementedError
    
    def deplacer_vers(self, sortie):
        """Déplacement vers la sortie 'sortie'"""
        salle = self.salle
        salle_dest = salle.sorties.get_sortie_par_nom(sortie).salle_dest
        sortie = salle.sorties.get_sortie_par_nom(sortie)
        salle.envoyer("{} s'en va vers {}.".format(self.nom,
                sortie.nom_complet), (self, ))
        self.salle = salle_dest
        self.envoyer(self.salle.regarder(self))
        salle_dest.envoyer("{} arrive.".format(self.nom), (self, ))
        
        # On appelle l'évènement arrive
        sortie_opp = sortie.sortie_opposee
        nom_opp = sortie_opp and sortie_opp.nom or None
        salle_dest.script.evenements["arrive"].executer(depuis=nom_opp,
                salle=salle_dest, personnage=self)
    
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
        if random < apprendre:
            avancement += 1
            self.talents[cle_talent] = avancement
        
        return avancement
    
    @staticmethod
    def regarder(moi, personnage):
        """personnage regarde moi."""
        equipement = moi.equipement
        msg = "Vous regardez {} :\n".format(personnage.nom)
        objets = []
        for membre in equipement.membres:
            objet = membre.equipe and membre.equipe[-1] or membre.tenu
            if objet:
                objets.append("{} [{}]".format(membre.nom.capitalize(),
                        objet.nom_singulier))
        
        if not objets:
            msg += "Il ne porte rien sur lui."
        else:
            msg += "Il porte :\n\n  " + "\n  ".join(objets)
        
        moi << "{} vous regarde.".format(personnage.nom)
        personnage.salle.envoyer("{} regarde {}.".format(personnage.nom,
                moi.nom), (personnage, moi))
        return msg
