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


"""Fichier contenant le module secondaire navigation."""

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from .navire import Navire
from .elements import types as types_elements
from .elements.base import BaseElement
from .vent import Vent
from . import commandes
from . import masques
from . import editeurs
from .modele import ModeleNavire

class Module(BaseModule):
    
    """Module secondaire définissant la navigation.
    
    Ce module définit les navires, modèles de navires et objets liés.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "navigation", "secondaire")
        self.commandes = []
        self.modeles = {}
        self.nav_logger = type(self.importeur).man_logs.creer_logger(
                "navigation", "navires", "navires.log")
        self.navires = {}
        self.elements = {}
        self.types_elements = types_elements
        self.vents = {}
        self.vents_par_etendue = {}
    
    def config(self):
        """Configuration du module."""
        his_voile = self.importeur.perso.ajouter_etat("hisser_voile")
        his_voile.msg_refus = "Vous êtes en train de hisser la voile"
        his_voile.msg_visible = "{personnage} hisse une voile ici"
        his_voile.act_interdites = ["combat", "prendre", "poser", "deplacer",
                "plier_voile", "tenir_gouvernail"]
        pli_voile = self.importeur.perso.ajouter_etat("plier_voile")
        pli_voile.msg_refus = "Vous êtes en train de replier la voile"
        pli_voile.msg_visible = "{personnage} replie une voile ici"
        pli_voile.act_interdites = ["combat", "prendre", "poser", "deplacer",
                "hisser_voile", "tenir_gouvernail"]
        ten_gouv = self.importeur.perso.ajouter_etat("tenir_gouvernail")
        ten_gouv.msg_refus = "Vous tenez actuellement le gouvernail"
        ten_gouv.msg_visible = "{personnage} tient le gouvernail ici"
        ten_gouv.act_interdites = ["combat", "prendre", "poser", "deplacer",
                "hisser_voile", "plier_voile"]
        
        BaseModule.config(self)
    
    def init(self):
        """Chargement des navires et modèles."""
        # On récupère les modèles
        modeles = self.importeur.supenr.charger_groupe(ModeleNavire)
        for modele in modeles:
            self.modeles[modele.cle] = modele
        
        nb_modeles = len(modeles)
        self.nav_logger.info(format_nb(nb_modeles,
                "{nb} modèle{s} de navire récupéré{s}"))
        
        # On récupère les navires
        navires = self.importeur.supenr.charger_groupe(Navire)
        for navire in navires:
            self.navires[navire.cle] = navire
        
        nb_navires = len(navires)
        self.nav_logger.info(format_nb(nb_navires,
                "{nb} navire{s} récupéré{s}"))
        
        # On récupère les éléments
        elements = self.importeur.supenr.charger_groupe(BaseElement)
        for element in elements:
            self.elements[element.cle] = element
        
        nb_elements = len(elements)
        self.nav_logger.info(format_nb(nb_elements,
                "{nb} élément{s} de navire récupéré{s}"))
        
        # On récupère les vents
        vents = self.importeur.supenr.charger_groupe(Vent)
        for vent in vents:
            self.ajouter_vent(vent)
        
        nb_vents = len(self.vents)
        self.nav_logger.info(format_nb(nb_vents,
                "{nb} vent{s} récupéré{s}"))
        
        # Ajout de l'action différée
        self.importeur.diffact.ajouter_action("dep_navire", 3,
                self.avancer_navires)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.ancre.CmdAncre(),
            commandes.detailler.CmdDetailler(),
            commandes.eltedit.CmdEltedit(),
            commandes.gouvernail.CmdGouvernail(),
            commandes.navire.CmdNavire(),
            commandes.passerelle.CmdPasserelle(),
            commandes.shedit.CmdShedit(),
            commandes.vent.CmdVent(),
            commandes.voile.CmdVoile(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.eltedit.EdtEltedit)
        self.importeur.interpreteur.ajouter_editeur(editeurs.shedit.EdtShedit)
    
    def creer_modele(self, cle):
        """Crée un modèle de navire et l'ajoute dans le dictionnaire.
        
        Retourne le modèle créé.
        
        Lève une exception KeyError si le modèle existe déjà.
        
        """
        valider_cle(cle)
        if cle in self.modeles:
            raise KeyError("le modèle de navire {} existe déjà".format(cle))
        
        modele = ModeleNavire(cle)
        self.ajouter_modele(modele)
        return modele
    
    def ajouter_modele(self, modele):
        """Ajoute le modèle de navire dans le dictionnaire."""
        self.modeles[modele.cle] = modele
    
    def supprimer_modele(self, cle):
        """Supprime le modèle de navire portant la clé passée en paramètre."""
        if cle not in self.modeles:
            raise KeyError("le modèle de navire de clé {} est inconnue".format(
                    cle))
        
        modele = self.modeles[cle]
        del self.modeles[cle]
        modele.detruire()
    
    def creer_navire(self, modele):
        """Crée un navire sur le modèle.
        
        Retourne le navire créé.
        
        """
        navire = Navire(modele)
        print("Navire {} créé".format(navire.cle))
        self.ajouter_navire(navire)
        return navire
    
    def ajouter_navire(self, navire):
        """Ajoute le navire à la liste."""
        self.navires[navire.cle] = navire
    
    def supprimer_navire(self, cle):
        """Supprime le navire dont la clé est passée en paramètre."""
        if cle not in self.navires:
            raise KeyError("le navire de clé {} est introuvable".format(cle))
        
        navire = self.navires[cle]
        navire.detruire()
        del self.navires[cle]
    
    def creer_element(self, cle, type_elt):
        """Crée un élément du type indiqué.
        
        Retourne l'élément créé.
        
        """
        elt = type_elt(cle)
        self.ajouter_element(elt)
        return elt
    
    def ajouter_element(self, element):
        """Ajoute l'élément au dictionnaire."""
        self.elements[element.cle] = element
    
    def supprimer_element(self, cle):
        """Supprime l'élément dont la clé est passée en paramètre."""
        if cle not in self.elements:
            raise KeyError("l'élément de clé {} est introuvable".format(cle))
        
        element = self.elements[cle]
        element.detruire()
        del self.elements[cle]
    
    def get_vents_etendue(self, cle):
        """Retourne une liste des vents de l'étendue."""
        return self.vents_par_etendue.get(cle, [])
    
    def creer_vent(self, etendue, x, y, z, vitesse=1, direction=0):
        """Crée un vent dans une étendue.
        
        Pour les paramètres, se référez au constructeur de la classe Vent.
        
        """
        vent = Vent(etendue, x, y, z, vitesse, direction)
        self.ajouter_vent(vent)
        return vent
    
    def ajouter_vent(self, vent):
        """Ajoute le vent."""
        self.vents[vent.cle] = vent
        self.vents_par_etendue[vent.etendue.cle] = self.vents_par_etendue.get(
                vent.etendue.cle, []) + [vent]
    
    def supprimer_vent(self, cle):
        """Supprime le vent."""
        vent = self.vents[cle]
        self.vents_par_etendue[vent.etendue.cle].remove(vent)
        del self.vents[cle]
        vent.detruire()
    
    def avancer_navires(self):
        """Fait avancer les navires."""
        self.importeur.diffact.ajouter_action("dep_navire", 3,
                self.avancer_navires)
        for navire in self.navires.values():
            if navire.etendue:
                navire.avancer(0.4)
