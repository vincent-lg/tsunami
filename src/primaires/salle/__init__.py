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


"""Fichier contenant le module primaire salle."""

from math import sqrt
import re
from datetime import datetime

from abstraits.module import *
from primaires.format.fonctions import format_nb, supprimer_accents
from primaires.vehicule.vecteur import Vecteur
from .config import cfg_salle
from .coordonnees import Coordonnees
from .salle import Salle, ZONE_VALIDE, MNEMONIC_VALIDE
from .feu import Feu
from .sortie import Sortie
from .sorties import NOMS_SORTIES
from .porte import Porte
from .zone import Zone
from .templates.terrain import Terrain
from .editeurs.redit import EdtRedit
from .editeurs.zedit import EdtZedit
from . import cherchables
from . import commandes
from . import masques
from . import types

# Constantes
NB_MIN_NETTOYAGE = 20

class Module(BaseModule):
    
    """Classe utilisée pour gérer des salles.
    
    Dans la terminologie des MUDs, les salles sont des "cases" avec une
    description et une liste de sorties possibles, que le joueur peut
    emprunter. L'ensemble des salles consiste l'univers, auquel il faut
    naturellement rajouter des PNJ et objets pour qu'il soit riche un minimum.
    
    Pour plus d'informations, consultez le fichier
    src/primaires/salle/salle.py contenant la classe Salle.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "salle", "primaire")
        self._salles = {} # ident:salle
        self.feux = {} # ident:feu
        self._zones = {} # cle:zone
        self._coords = {} # coordonnee:salle
        self.commandes = []
        self.salle_arrivee = ""
        self.salle_retour = ""
        self.aliases = {
            "e": "est",
            "se": "sud-est",
            "s": "sud",
            "so": "sud-ouest",
            "o": "ouest",
            "no": "nord-ouest",
            "n": "nord",
            "ne": "nord-est",
            "b": "bas",
            "h": "haut",
            "s-e": "sud-est",
            "s-o": "sud-ouest",
            "n-o": "nord-ouest",
            "n-e": "nord-est",
        }
        
        self.logger = importeur.man_logs.creer_logger( \
                "salles", "salles")
        self.terrains = {}
        self.graph = {}
    
    @property
    def salles(self):
        """Retourne un dictionnaire déréférencé des salles."""
        return dict(self._salles)
    
    @property
    def zones(self):
        """Retourne un dictionnaire déréférencé des zones."""
        return dict(self._zones)
    
    def config(self):
        """Méthode de configuration du module"""
        importeur.anaconf.get_config("salle", \
            "salle/salle.cfg", "config salle", cfg_salle)
        importeur.hook.ajouter_hook("salle:regarder",
                "Hook appelé dès qu'on regarde une salle.")
        
        # Ajout des terrains
        self.ajouter_terrain("ville")
        self.ajouter_terrain("route")
        self.ajouter_terrain("forêt")
        self.ajouter_terrain("plaine")
        self.ajouter_terrain("rive")
        self.ajouter_terrain("désert")
        self.ajouter_terrain("caverne")
        self.ajouter_terrain("aquatique")
        self.ajouter_terrain("subaquatique")
        
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les portes
        portes = importeur.supenr.charger_groupe(Porte)
        # On récupère les salles
        salles = importeur.supenr.charger_groupe(Salle)
        for salle in salles:
            self.ajouter_salle(salle)
        
        nb_salles = len(self._salles)
        self.logger.info(format_nb(nb_salles, "{nb} salle{s} récupérée{s}", \
                fem=True))
        
        # On récupère les feux
        feux = importeur.supenr.charger_groupe(Feu)
        for feu in feux:
            self.feux[feu.salle.ident] = feu
        # On implémente le hook correspondant
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.feu_present)
        
        # On récupère les zones
        zones = importeur.supenr.charger_groupe(Zone)
        for zone in zones:
            self._zones[zone.cle] = zone
        
        nb_zones = len(self._zones)
        self.logger.info(format_nb(nb_zones, "{nb} zone{s} récupérée{s}", \
                fem=True))
        
        importeur.diffact.ajouter_action("net_salles", 300,
                self.nettoyer_salles)
        importeur.diffact.ajouter_action("repop_salles", 900,
                self.repop_salles)
        importeur.diffact.ajouter_action("repop_feux", 5, Feu.repop)
        
        # On ajoute les niveaux et talents
        importeur.perso.ajouter_niveau("survie", "survie")
        importeur.perso.ajouter_talent("collecte_bois", "collecte de bois",
                "survie", 0.55)
        importeur.perso.ajouter_talent("feu_camp", "feu de camp", "survie",
                0.23)
        
        # On ajoute de l'état
        etat = importeur.perso.ajouter_etat("collecte_bois")
        etat.msg_refus = "Vous êtes en train de ramasser du bois."
        etat.msg_visible = "ramasse du bois"
        etat.act_interdites = ["combat", "prendre", "poser", "deplacer",
            "chercher"]
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.addroom.CmdAddroom(),
            commandes.carte.CmdCarte(),
            commandes.chercherbois.CmdChercherBois(),
            commandes.chsortie.CmdChsortie(),
            commandes.deverrouiller.CmdDeverrouiller(),
            commandes.fermer.CmdFermer(),
            commandes.goto.CmdGoto(),
            commandes.mettrefeu.CmdMettreFeu(),
            commandes.ouvrir.CmdOuvrir(),
            commandes.redit.CmdRedit(),
            commandes.regarder.CmdRegarder(),
            commandes.supsortie.CmdSupsortie(),
            commandes.verrouiller.CmdVerrouiller(),
            commandes.zone.CmdZone(),
        ]
        
        for cmd in self.commandes:
            importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des l'éditeurs 'redit' et 'zedit'
        importeur.interpreteur.ajouter_editeur(EdtRedit)
        importeur.interpreteur.ajouter_editeur(EdtZedit)
    
    def preparer(self):
        """Préparation du module.
        
        On vérifie que :
        -   Les salles de retour et d'arrivée sont bien créés (sinon,
            on les recrée)
        -   On recrée le lien entre sorties et salles
        -   Les personnages présents dans self._personnages soient
            toujours là
        -   Chaque salle est dans une zone
        
        """
        # On récupère la configuration
        conf_salle = importeur.anaconf.get_config("salle")
        salle_arrivee = conf_salle.salle_arrivee
        salle_retour = conf_salle.salle_retour
        
        if salle_arrivee not in self:
            # On crée la salle d'arrivée
            zone, mnemonic = salle_arrivee.split(":")
            salle_arrivee = self.creer_salle(zone, mnemonic, valide=False)
            salle_arrivee.titre = "La salle d'arrivée"
            salle_arrivee = salle_arrivee.ident
        
        if salle_retour not in self:
            # On crée la salle de retour
            zone, mnemonic = salle_retour.split(":")
            salle_retour = self.creer_salle(zone, mnemonic, valide=False)
            salle_retour.titre = "La salle de retour"
            salle_retour = salle_retour.ident
        
        self.salle_arrivee = salle_arrivee
        self.salle_retour = salle_retour
        
        # On prépare les sorties
        for salle in self.salles.values():
            for sortie in salle.sorties:
                salle_dest = self.salles[sortie.salle_dest]
                sortie.salle_dest = salle_dest
                self.ajouter_chemin(salle, salle_dest, sortie.direction)
        
        for salle in self._salles.values():
            zone = salle.zone
            zone.ajouter(salle)
            for personnage in salle.personnages:
                if personnage.salle is not salle:
                    salle.retirer_personnage(personnage)
    
    def detruire(self):
        """Destruction du module.
        
        * On détruit toutes les zones vides
        
        """
        for zone in self._zones.values():
            if not zone.salles:
                zone.detruire()
    
    def __len__(self):
        """Retourne le nombre de salles"""
        return len(self._salles)
    
    def __getitem__(self, cle):
        """Retourne la salle correspondante à la clé.
        Celle-ci peut être de différents types :
        *   une chaîne : c'est l'identifiant 'zone:mnemonic'
        *   un objet Coordonnees
        *   un tuple représentant les coordonnées
        
        """
        if type(cle) is str:
            return self._salles[cle]
        elif type(cle) is Coordonnees:
            return self._coords[cle.tuple()]
        elif type(cle) is tuple:
            return self._coords[cle]
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))
    
    def __contains__(self, cle):
        """Retourne True si la clé se trouve dans l'un des dictionnaires de
        salles. Voir la méthode __getitem__ pour connaître les types acceptés.
        
        """
        if type(cle) is str:
            return cle in self._salles.keys()
        elif type(cle) is Coordonnees:
            return cle.tuple() in self._coords.keys()
        elif type(cle) is tuple:
            return cle in self._coords.keys()
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))
    
    def ajouter_salle(self, salle):
        """Ajoute la salle aux deux dictionnaires
        self._salles et self._coords.
        
        """
        self._salles[salle.ident] = salle
        if salle.coords.valide:
            self._coords[salle.coords.tuple()] = salle
    
    def creer_salle(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Permet de créer une salle"""
        ident = zone + ":" + mnemonic
        if ident in self._salles.keys():
            raise ValueError("la salle {} existe déjà".format(ident))
        if not re.search(ZONE_VALIDE, zone):
            raise ValueError("Zone {} invalide".format(zone))
        if not re.search(MNEMONIC_VALIDE, mnemonic):
            raise ValueError("Mnémonic {} invalide ({})".format(mnemonic,
                    MNEMONIC_VALIDE))
        
        salle = Salle(zone, mnemonic, x, y, z, valide)
        self.ajouter_salle(salle)
        return salle
    
    def supprimer_salle(self, cle):
        """Supprime la salle.
        La clé est l'identifiant de la salle.
        
        """
        salle = self._salles[cle]
        coords = salle.coords
        if coords.valide and coords.tuple() in self._coords.keys():
            del self._coords[coords.tuple()]
        del self._salles[cle]
        salle.detruire()
    
    def traiter_commande(self, personnage, commande):
        """Traite les déplacements"""
        
        # Si la commande est vide, on ne se déplace pas
        if len(commande) == 0:
            return False
        
        commande = supprimer_accents(commande).lower()
        salle = personnage.salle
        try:
            sortie = salle.sorties.get_sortie_par_nom(commande,
                    cachees=False)
        except KeyError:
            pass
        else:
            personnage.deplacer_vers(sortie.nom)
            return True
        
        for nom, sortie in salle.sorties.iter_couple():
            if sortie and sortie.salle_dest:
                nom = supprimer_accents(sortie.nom).lower()
                if (sortie.cachee and nom == commande) or ( \
                        not sortie.cachee and nom.startswith(commande)):
                    personnage.deplacer_vers(sortie.nom)
                    return True
        
        if commande in NOMS_SORTIES.keys():
            personnage << "Vous ne pouvez aller par là..."
            return True
        
        return False
    
    def changer_ident(self, ancien_ident, nouveau_ident):
        """Change l'identifiant d'une salle"""
        salle = self._salles[ancien_ident]
        del self._salles[ancien_ident]
        self._salles[nouveau_ident] = salle
        
        # On change la salle de zone si la zone est différente
        a_zone = ancien_ident.split(":")[0]
        n_zone = nouveau_ident.split(":")[0]
        if a_zone != n_zone:
            self.get_zone(a_zone).retirer(salle)
            self.get_zone(n_zone).ajouter(salle)
    
    def changer_coordonnees(self, ancien_tuple, nouvelles_coords):
        """Change les coordonnées d'une salle.
        Les anciennes coordonnées sont données sous la forme d'un tuple
            (x, y, z, valide)
        Les nouvelles sont un objet Coordonnees.
        
        """
        a_x, a_y, a_z, a_valide = ancien_tuple
        salle = nouvelles_coords.parent
        if a_valide and (a_x, a_y, a_z) in self._coords:
            # on va supprimer les anciennes coordonnées
            del self._coords[a_x, a_y, a_z]
        if salle and nouvelles_coords.valide:
            self._coords[nouvelles_coords.tuple()] = salle
    
    def ajouter_terrain(self, nom):
        """Ajoute un terrain."""
        if nom in self.terrains:
            raise KeyError("le terrain {] existe déjà".format(repr(nom)))
        
        terrain = Terrain(nom)
        self.terrains[nom] = terrain
    
    def get_zone(self, cle):
        """Retourne la zone correspondante ou la crée."""
        zone = self._zones.get(cle)
        if zone is None:
            zone = Zone(cle)
            self._zones[cle] = zone
        
        return zone
    
    def nettoyer_salles(self):
        """Nettoyage des salles et des objets trop vieux."""
        importeur.diffact.ajouter_action("net_salles", 300,
                self.nettoyer_salles)
        maintenant = datetime.now()
        for s in self.salles.values():
            objets = [o for o in s.objets_sol._objets if o.nettoyer]
            for o in objets:
                if (maintenant - o.ajoute_a).seconds >= NB_MIN_NETTOYAGE * 60:
                    o.contenu.retirer(o)
                    o.detruire()
    
    def repop_salles(self):
        """Méthode chargée de repop les salles."""
        importeur.diffact.ajouter_action("repop_salles", 900,
                self.repop_salles)
        for s in self.salles.values():
            s.repop()
    
    def allumer_feu(self, salle, puissance=10):
        """Allume un feu dans salle."""
        if not salle.ident in self.feux:
            feu = Feu(salle, puissance)
            self.feux[salle.ident] = feu
        else:
            feu = salle.feux[salle.ident]
        return feu
    
    def eteindre_feu(self, salle):
        """Eteint un éventuel feu dans salle."""
        if salle.ident in self.feux:
            self.feux[salle.ident].detruire()
            del self.feux[salle.ident]
    
    def feu_present(self, salle, liste_messages, flags):
        """Si un feu se trouve dans la salle, on l'affiche"""
        if self.feux:
            for feu in self.feux.values():
                if salle == feu.salle:
                    liste_messages.insert(0, str(feu))
                    return
    
    def ajouter_chemin(self, origine, destination, direction):
        """Ajoute un chemin dans le graph entre deux salles.
        
        Le graph représente TOUS les chemins possibles entre deux salles.
        la forme du graph (self.graph) est un dictionnaire contenant en
        clé la salle d'origine et en valeur un dictionnaire contenant
        en clé la destination et en valeur la sortie.
        
        """
        for t_graph in self.graph.values():
            t_chemin = t_graph.get(origine)
            if t_chemin:
                t_graph[destination] = t_chemin
        
        d_origine = self.graph.get(origine, {})
        d_origine[destination] = direction
        self.graph[origine] = d_origine

