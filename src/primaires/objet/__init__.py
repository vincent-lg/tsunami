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


"""Fichier contenant le module primaire objet."""

from abstraits.module import *
from . import types
from . import commandes
from . import editeurs
from . import masques
from .editeurs.oedit import EdtOedit
from .types import types as o_types
from .types.base import BaseType
from .objet import Objet

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire objet.
    Ce module gère les objets de l'univers.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "diffact", "primaire")
        self._prototypes = {}
        self._objets = {}
    
    def init(self):
        """Initialisation du module"""
        prototypes = self.importeur.supenr.charger_groupe(BaseType)
        for prototype in prototypes:
            self._prototypes[prototype.identifiant] = prototype
        
        objets = self.importeur.supenr.charger_groupe(Objet)
        for objet in objets:
            self._objets[objet.identifiant] = objet
        
        BaseModule.init(self)
    
    def ajouter_masques(self):
        """Ajout des masques dans l'interpréteur"""
        self.importeur.interpreteur.ajouter_masque(
                masques.ident_prototype_objet.IdentPrototypeObjet)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.oedit.CmdOedit(),
            commandes.olist.CmdOlist(),
            commandes.opurge.CmdOpurge(),
            commandes.ospawn.CmdOspawn(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'redit'
        self.importeur.interpreteur.ajouter_editeur(EdtOedit)
    
    def preparer(self):
        """Préparation du module"""
        for prototype in self.prototypes.values():
            prototype.objets.supprimer_none()
    
    @property
    def prototypes(self):
        return dict(self._prototypes)
    
    @property
    def objets(self):
        return dict(self._objets)
    
    def creer_prototype(self, identifiant, nom_type="indéfini"):
        """Crée un prototype et l'ajoute aux prototypes existants"""
        if identifiant in self._prototypes:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "prototype".format(identifiant))
        
        cls_type = o_types[nom_type]
        prototype = cls_type(identifiant)
        self.ajouter_prototype(prototype)
        return prototype
    
    def ajouter_prototype(self, prototype):
        """Ajoute un prototype au dictionnaire des prototypes"""
        if prototype.identifiant in self._prototypes:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "prototype".format(prototype.identifiant))
        
        self._prototypes[prototype.identifiant] = prototype
    
    def supprimer_prototypes(self, identifiant):
        """Supprime le prototype identifiant"""
        prototype = self._prototypes[identifiant]
        del self._prototypes[identifiant]
        prototype.detruire()
    
    def creer_objet(self, prototype):
        """Crée un objet depuis le prototype prototype.
        L'objet est ensuite ajouté à la liste des objets existants.
        
        """
        objet = Objet(prototype)
        self.ajouter_objet(objet)
        return objet
    
    def ajouter_objet(self, objet):
        """Ajoute l'objet à la liste des objets"""
        if objet.identifiant in self._objets:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "objet".format(objet.identifiant))
        
        self._objets[objet.identifiant] = objet
    
    def supprimer_objet(self, identifiant):
        """Supprime l'objet de la liste des objets"""
        objet = self._objets[identifiant]
        del self._objets[identifiant]
        objet.detruire()
