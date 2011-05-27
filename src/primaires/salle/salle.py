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


"""Fichier contenant la classe Salle, détaillée plus bas."""

from collections import OrderedDict

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID
from primaires.format.description import Description
from .coordonnees import Coordonnees
from .sorties import Sorties, NOMS_SORTIES
from .details import Details
from .objets_sol import ObjetsSol

# Constantes
ZONE_VALIDE = r"^[a-z0-9_]{3,20}$"
MNEMONIC_VALIDE = r"^[a-z0-9_]{1,15}$"

class Salle(ObjetID):
    
    """Classe représentant une salle de l'univers.
    Une salle est un élément détaillant la géographie locale d'une petite
    portion de l'univers. Bien que cela dépende des MUDs, les salles décrivent
    généralement un espace d'environ 5 mètres sur 5.
    
    Ces salles comportent une description détaillant les alentours proches.
    Cette description est envoyée à chaque fois qu'un personnage se déplace
    dans l'univers, pour lui donner une idée de son nouvel environnement.
    
    Note sur le positionnement des salles :
        Les salles peuvent être caractérisées par des coordonnées. Ces
        coordonnées sont en soi facultatives. Il est possible de créer un
        univers sans aucune coordonnée. Il s'agit d'une facilité
        lors de la constitution de votre univers qui permet à certains
        modules, comme 'vehicule', de fonctionner. Si votre salle n'a pas de
        coordonnées, vous devrez créer chaque sortie "à la main".
        Les salles ne sont donc pas identifiées par leurs coordonnées, sauf
        dans certains cas, mais bien par leur zone et mnémonic. Ce couple
        caractérise de façon unique une salle dans l'univers.
        Exemple : une ssalle ayant pour zone 'picte' et pour mnémonic '1'
        sera accessible depuis la clé 'picte:1' ; aucune autre salle de
        l'univers ne pourra posséder cette clé 'picte:1'.
    
    """
    
    groupe = "salles"
    sous_rep = "salles"
    _nom = "salle"
    _version = 1
    
    def __init__(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Constructeur de la salle"""
        ObjetID.__init__(self)
        self._zone = zone
        self._mnemonic = mnemonic
        self.coords = Coordonnees(x, y, z, valide, self)
        self.titre = ""
        self.description = Description(parent=self)
        self.sorties = Sorties(parent=self)
        self.details = Details(parent=self)
        self._personnages = ListeID() # personnages présents
        self.objets_sol = ObjetsSol(parent=self)
    
    def __getnewargs__(self):
        return ("", "")
    
    def __getattribute__(self, nom_attr):
        obj = ObjetID.__getattribute__(self, nom_attr)
        return obj
    def __setattr__(self, nom_attr, val_attr):
        ObjetID.__setattr__(self, nom_attr, val_attr)
    def __str__(self):
        """Retourne l'identifiant 'zone:mnemonic'"""
        return self._zone + ":" + self._mnemonic
    
    def _get_zone(self):
        return self._zone
    def _set_zone(self, zone):
        ident = self.ident
        self._zone = zone.lower()
        self.enregistrer()
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    def _get_mnemonic(self):
        return self._mnemonic
    def _set_mnemonic(self, mnemonic):
        ident = self.ident
        self._mnemonic = mnemonic.lower()
        self.enregistrer()
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    zone = property(_get_zone, _set_zone)
    mnemonic = property(_get_mnemonic, _set_mnemonic)
    
    @property
    def ident(self):
        """Retourne l'identifiant, c'est-à-dire une chaîne 'zone:mnemonic'"""
        return "{}:{}".format(self._zone, self._mnemonic)
    
    @property
    def personnages(self):
        """Retourne une liste déférencée des personnages"""
        return list(self._personnages)
    
    def __repr__(self):
        """Affichage de la salle en mode debug"""
        res = "Salle ({}, {})".format(self.ident, self.coords)
        # Sorties
        for nom, sortie in self.sorties.iter_couple():
            if sortie:
                res += "\n  {} : {}".format(nom, sortie.salle_dest.ident)
        return res
    
    def personnage_est_present(self, personnage):
        """Si le personnage est présent, retourne True, False sinon."""
        return personnage in self._personnages
    
    def ajouter_personnage(self, personnage):
        """Ajoute le personnage dans la salle"""
        if personnage not in self.personnages:
            self._personnages.append(personnage)
            self.enregistrer()
    
    def retirer_personnage(self, personnage):
        """Retire le personnage des personnages présents"""
        if personnage in self.personnages:
            self._personnages.remove(personnage)
            self.enregistrer()
    
    def envoyer(self, message, exceptions=()):
        """Envoie le message aux personnages présents dans la salle.
        Les personnages présents dans l'exception ne recevront pas le
        message.
        
        """
        for personnage in self.personnages:
            if personnage not in exceptions:
                personnage.envoyer(message)
    
    def get_objets_nombres(self):
        """Retourne un tuple contenant des couples prototype, nombre"""
        prototypes = OrderedDict()   # {prototype: nombre}
        # On parcourt les objets de la salle
        for objet in self.objets_sol:
            prototype = objet.prototype
            if prototype not in prototypes:
                prototypes[prototype] = 1
            else:
                prototypes[prototype] += 1
        
        return tuple(prototypes.items())
    
    def regarder(self, personnage):
        """Le personnage regarde la salle"""
        res = ""
        res += "# |rgc|" + self.zone + "|ff|:|vrc|" + self.mnemonic + "|ff|\n\n"
        res += "|tit|" + self.titre + "|ff|\n\n"
        description = str(self.description)
        if not description:
            description = "Vous êtes au milieu de nulle part."
        
        res += description + "\n\n"
        res += "Sorties : "
        res += self.afficher_sorties(personnage)
        
        # Personnages
        personnages = []
        for personne in self.personnages:
            if personne is not personnage:
                personnages.append(personne)
        
        if len(personnages):
            res += "\n"
            for personne in personnages:
                res += "\n- {} est là".format(personne.nom)
        
        # Objets
        noms_objets = self.afficher_noms_objets()
        if len(noms_objets):
            res += "\n"
            for nom_objet in noms_objets:
                res += "\n+ {}".format(nom_objet)
        
        return res
    
    def afficher_sorties(self, personnage):
        """Affiche les sorties de la salle"""
        res = ""
        for nom in NOMS_SORTIES.keys():
            sortie = self.sorties[nom]
            if sortie:
                nom = sortie.nom
            
            nom_aff = self.sorties.get_nom_abrege(nom)
            if self.sorties.sortie_existe(nom):
                if sortie.cache:
                    res += " ".ljust(len(self.sorties.get_nom_abrege(
                            sortie.direction)))
                else:
                    res += "|vr|" + nom_aff + "|ff|"
            else:
                res += " ".ljust(len(nom_aff))
            res += ", "
        
        res = res[:-2] + "."
        return res
    
    def afficher_noms_objets(self):
        """Retourne les noms et états des objets sur le sol de la salle"""
        # On récupère les couples prototype, nombre
        prototypes = self.get_objets_nombres()
        
        # On parcourt à présent les prototypes pour récupérer leur nom et état
        noms_etats = []
        for prototype, nombre in prototypes:
            noms_etats.append(prototype.get_nom_etat(nombre))
        
        return noms_etats

# On ajoute le groupe à ObjetID
ObjetID.ajouter_groupe(Salle)
