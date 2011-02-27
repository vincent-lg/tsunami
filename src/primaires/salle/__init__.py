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

from abstraits.module import *
from .salle import Salle
from .sorties import NOMS_SORTIES
from .config import cfg_salle
import primaires.salle.commandes

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
        
        ###DEBUG
        if len(salles) == 0:
            s1 = self.creer_salle("picte", "1", 0, 0, 0)
            s1.titre = "La salle Picte 1"
            s1.description = "Une description."
            s2 = self.creer_salle("picte", "2", 0, 1, 0)
            s1.sorties.ajouter_sortie("est", "est", salle_dest=s2)
            s2.titre = "La salle Picte 2"
            s2.description = "Une autre description."
            s2.sorties.ajouter_sortie("ouest", "ouest", salle_dest=s1)
        print(self._salles, self._coords)
        
        # On récupère la configuration
        conf_salle = type(self.importeur).anaconf.get_config("salle")
        salle_arrivee = conf_salle.salle_arrivee
        salle_retour = conf_salle.salle_retour
        
        if salle_arrivee not in self:
            # On crée la salle d'arrivée
            zone, mnemonic = salle_arrivee.split(":")
            salle_arrivee = self.creer_salle(zone, mnemonic, valide=False)
            salle_arrivee.titre = "La salle d'arrivée"
            salle_arrivee.description = "Vous êtes au milieu de nulle part."
            print("Création de la salle d'arrivée :", salle_arrivee)
            salle_arrivee = salle_arrivee.ident
        
        if salle_retour not in self:
            # On crée la salle de retour
            zone, mnemonic = salle_retour.split(":")
            salle_retour = self.creer_salle(zone, mnemonic, valide=False)
            salle_retour.titre = "La salle de retour"
            salle_arrivee.description = "Vous êtes au milieu de nulle part."
            print("Création de la salle de retour :", salle_retour)
            salle_retour = salle_retour.ident
        
        self.salle_arrivee = salle_arrivee
        self.salle_retour = salle_retour

        s = ""
        nb_salles = (len(self._salles) != 0) and len(self._salles) or "Aucune"
        if len(self._salles) > 1:
            s = "s"
        self.logger.info("{} salle{s} récupérée{s}".format(nb_salles, s = s))
        
        # On ajoute les commandes du module
        self.commandes = [
            commandes.redit.CmdRedit(),
            commandes.regarder.CmdRegarder(),
        ]
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        BaseModule.init(self)
    
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
        salle = personnage.salle
        for nom, sortie in salle.sorties.iter_couple():
            if salle.sorties.sortie_existe(nom) and sortie.nom.startswith(
                    commande):
                personnage.deplacer_vers(sortie.nom)
                return True
        
        if commande in NOMS_SORTIES.keys():
            personnage << "Vous ne pouvez aller par là..."
            return True
        
        return False
