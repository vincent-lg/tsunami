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
from . import cherchables
from .editeurs.oedit import EdtOedit
from .types import types as o_types
from .types.base import BaseType
from .objet import Objet
from .potions_vente import PotionsVente
from .nourritures_vente import NourrituresVente

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire objet.
    Ce module gère les objets de l'univers.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "objet", "primaire")
        self._prototypes = {}
        self._objets = {}
    
    def config(self):
        """Configuration du module."""
        importeur.commerce.types_services["objet"] = self._prototypes
        importeur.commerce.aides_types["objet"] = \
            "Ce service se contente, à l'achat, de faire apparaître " \
            "l'objet précisé sur\nle sol de la salle."
        importeur.commerce.types_services["potion"] = PotionsVente()
        importeur.commerce.aides_types["potion"] = \
            "Ce service permet de proposer à la vente des potions " \
            "dans des conteneurs.\nPour cela, précisé un couple sous la " \
            "forme |cmd|<conteneur>/<potion>|ff| (par exemple,\n|ent|chope/" \
            "biere|ff| pour une chope de bière."
        importeur.commerce.types_services["nourriture"] = NourrituresVente()
        importeur.commerce.aides_types["nourriture"] = \
            "Ce service permet la vente de nourriture dans des plats, " \
            "dans un restaurant\npar exemple. Pour cela, précisez un " \
            "conteneur de nourriture puis une liste\nd'aliments sous la " \
            "forme |cmd|<conteneur>/<al1>(+<al2>+<al3>...)|ff| (par " \
            "exemple,\n|ent|assiette/patate+tomate+carotte|ff| pour une " \
            "assiette contenant ces trois légumes).\nSi le poids de la liste " \
            "d'aliments que vous proposez est supérieur au poids\nmaximum du " \
            "conteneur, l'ajout du service ne fonctionnera pas."
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        prototypes = self.importeur.supenr.charger_groupe(BaseType)
        for prototype in prototypes:
            self._prototypes[prototype.cle] = prototype
        
        objets = self.importeur.supenr.charger_groupe(Objet)
        for objet in objets:
            self._objets[objet.identifiant] = objet
        
        # Ajout de l'état repas
        etat = self.importeur.perso.ajouter_etat("repas")
        etat.msg_refus = "Vous êtes en train de manger."
        etat.msg_visible = "mange ici"
        etat.act_autorisees = ["regarder", "bouger"]
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.boire.CmdBoire(),
            commandes.donner.CmdDonner(),
            commandes.manger.CmdManger(),
            commandes.oedit.CmdOedit(),
            commandes.olist.CmdOlist(),
            commandes.opurge.CmdOpurge(),
            commandes.ospawn.CmdOspawn(),
            commandes.porter.CmdPorter(),
            commandes.poser.CmdPoser(),
            commandes.prendre.CmdPrendre(),
            commandes.puiser.CmdPuiser(),
            commandes.remplir.CmdRemplir(),
            commandes.retirer.CmdRetirer(),
            commandes.vider.CmdVider(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'oedit'
        self.importeur.interpreteur.ajouter_editeur(EdtOedit)
    
    def preparer(self):
        """Préparation du module."""
        if "cadavre" not in self._prototypes:
            self.creer_prototype("cadavre", "cadavre")
    
    @property
    def prototypes(self):
        return dict(self._prototypes)
    
    @property
    def objets(self):
        return dict(self._objets)
    
    @property
    def noms_types(self):
        """Retourne le nom des types d'objets actuels."""
        return [t.nom_type for t in o_types.values()]
    
    @property
    def types(self):
        """Retourne un dictionnaire des types."""
        return dict(o_types)
    
    @property
    def types_premier_niveau(self):
        """Retourne un dictionnaire des types du premier niveau."""
        return BaseType.types
    
    # @property
    # def conteneurs_potions(self):
        # """Retourne un dictionnaire pour la vente de potions.
        # Ce dictionnaire a pour clés tous les conteneur/potion de l'univers
        # et pour valeurs les objets PotionVente correspondants.
        
        # """
        # dico = {}
        # for c, o_c in [p for p in self.prototypes if p.est_de_type(
                # "conteneur de potion")]:
            # for po, o_po in [p for p in self.prototypes if p.est_de_type(
                    # "potion")]:
                # dico[c + "/" + po] = PotionVente(o_c, o_po)
        
        # return dico
    
    def creer_prototype(self, cle, nom_type="indéfini"):
        """Crée un prototype et l'ajoute aux prototypes existants"""
        if cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(cle))
        
        cls_type = o_types[nom_type]
        prototype = cls_type(cle)
        self.ajouter_prototype(prototype)
        return prototype
    
    def ajouter_prototype(self, prototype):
        """Ajoute un prototype au dictionnaire des prototypes"""
        if prototype.cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(prototype.cle))
        
        self._prototypes[prototype.cle] = prototype
    
    def supprimer_prototype(self, cle):
        """Supprime le prototype cle"""
        prototype = self._prototypes[cle]
        del self._prototypes[cle]
        prototype.detruire()
    
    def creer_objet(self, prototype):
        """Crée un objet depuis le prototype prototype.
        L'objet est ensuite ajouté à la liste des objets existants.
        
        """
        if not prototype.unique:
            return prototype
        
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
