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

import re

from abstraits.module import *
from .salle import Salle, ZONE_VALIDE, MNEMONIC_VALIDE
from .sorties import NOMS_SORTIES
from .config import cfg_salle
import primaires.salle.commandes
from .editeurs.redit import EdtRedit
from .coordonnees import Coordonnees
from . import masques

class Module(BaseModule):
    
    """Classe utilisée pour gérer des salles.
    Dans la terminologie des MUDs, les salles sont des "cases" avec une
    description et une liste de sorties possibles, que le joueur peut
    emprunter. L'ensemble des salles consiste l'univers, auquel il faut
    naturellement rajouter des NPCs et objets pour qu'il soit riche un minimum.
    
    Pour plus d'informations, consultez le fichier
    src/primaires/salle/salle.py contenant la classe Salle.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "salle", "primaire")
        self._salles = {} # ident:salle
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
        
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "salles", "salles")
    
    def config(self):
        """Méthode de configuration du module"""
        type(self.importeur).anaconf.get_config("salle", \
            "salle/salle.cfg", "config salle", cfg_salle)
        
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les salles
        salles = self.importeur.supenr.charger_groupe(Salle)
        for salle in salles:
            self.ajouter_salle(salle)
        
        # On récupère la configuration
        conf_salle = type(self.importeur).anaconf.get_config("salle")
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

        s = ""
        nb_salles = (len(self._salles) != 0) and len(self._salles) or "Aucune"
        if len(self._salles) > 1:
            s = "s"
        self.logger.info("{} salle{s} récupérée{s}".format(nb_salles, s = s))
        
        BaseModule.init(self)
    
    def ajouter_masques(self):
        """Ajout des masques dans l'interpréteur"""
        self.importeur.interpreteur.ajouter_masque(
                masques.direction.Direction)
        self.importeur.interpreteur.ajouter_masque(
                masques.nv_ident.NvIdent)
        self.importeur.interpreteur.ajouter_masque(
                masques.ident.Ident)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.addroom.CmdAddroom(),
            commandes.chsortie.CmdChsortie(),
            commandes.goto.CmdGoto(),
            commandes.redit.CmdRedit(),
            commandes.regarder.CmdRegarder(),
            commandes.supsortie.CmdSupsortie(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'redit'
        self.importeur.interpreteur.ajouter_editeur(EdtRedit)
    
    def preparer(self):
        """Préparation du module.
        On vérifie que :
        -   les personnages présents dans self._personnages soient
            toujours là
        -   les objets du sol existent toujours
        
        """
        for salle in self._salles.values():
            salle._personnages.supprimer_doublons()
            salle._personnages.supprimer_none()
            salle.objets_sol.nettoyer()
            for personnage in salle.personnages:
                if personnage.salle is not salle:
                    salle.retirer_personnage(personnage)
    
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
            raise ValueError("Mnémonic {} invalide ({})".format(mnemonic, MNEMONIC_VALIDE))
        
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
        commande = commande.lower()
        if commande in self.aliases.keys():
            commande = self.aliases[commande]
        
        salle = personnage.salle
        for nom, sortie in salle.sorties.iter_couple():
            if sortie and sortie.nom.startswith(commande):
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
    
    def changer_coordonnees(self, ancien_tuple, nouvelles_coords):
        """Change les coordonnées d'une salle.
        Les anciennes coordonnées sont données sous la forme d'un tuple
            (x, y, z, valide)
        Les nouvelles sont un objet Coordonnees.
        
        """
        a_x, a_y, a_z, a_valide = ancien_tuple
        salle = nouvelles_coords.parent
        if a_valide: # on va supprimer les anciennes coordonnées
            del self._coords[a_x, a_y, a_z]
        if salle and nouvelles_coords.valide:
            self._coords[nouvelles_coords.tuple()] = salle
