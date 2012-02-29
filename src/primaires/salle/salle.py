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

from abstraits.obase import BaseObj
from corps.fonctions import lisser
from primaires.format.description import Description
from .chemins import Chemins
from .coordonnees import Coordonnees
from .sorties import Sorties, NOMS_SORTIES
from .details import Details
from .objets_sol import ObjetsSol
from .script import ScriptSalle

# Constantes
ZONE_VALIDE = r"^[a-z0-9_]{3,20}$"
MNEMONIC_VALIDE = r"^[a-z0-9_]{1,15}$"

class Salle(BaseObj):
    
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
    
    nom_scripting = "la salle"
    _nom = "salle"
    _version = 3
    
    enregistrer = True
    def __init__(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Constructeur de la salle"""
        BaseObj.__init__(self)
        self._nom_zone = zone
        self._mnemonic = mnemonic
        self.coords = Coordonnees(x, y, z, valide, self)
        self.nom_terrain = "ville"
        self.titre = ""
        self.description = Description(parent=self)
        self.sorties = Sorties(parent=self)
        self.details = Details(parent=self)
        self._personnages = []
        self.objets_sol = ObjetsSol(parent=self)
        self.script = ScriptSalle(self)
        self.interieur = False
        self.magasin = None
        
        # Repop
        self.pnj_repop = {}
    
    def __getnewargs__(self):
        return ("", "")
    
    def __repr__(self):
        """Affichage de la salle en mode debug"""
        return self._nom_zone + ":" + self._mnemonic
    
    def __str__(self):
        """Retourne l'identifiant 'zone:mnemonic'"""
        return self._nom_zone + ":" + self._mnemonic
    
    def _get_nom_zone(self):
        return self._nom_zone
    def _set_nom_zone(self, zone):
        ident = self.ident
        self._nom_zone = zone.lower()
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    def _get_mnemonic(self):
        return self._mnemonic
    def _set_mnemonic(self, mnemonic):
        ident = self.ident
        self._mnemonic = mnemonic.lower()
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    nom_zone = property(_get_nom_zone, _set_nom_zone)
    mnemonic = property(_get_mnemonic, _set_mnemonic)
    
    @property
    def zone(self):
        """Retourne la zone  correspondante."""
        return type(self).importeur.salle.get_zone(self._nom_zone)
    
    @property
    def ident(self):
        """Retourne l'identifiant, c'est-à-dire une chaîne 'zone:mnemonic'"""
        return "{}:{}".format(self._nom_zone, self._mnemonic)
    
    @property
    def personnages(self):
        """Retourne une liste déférencée des personnages"""
        return list(self._personnages)
    
    @property
    def exterieur(self):
        """Retourne True si la salle est extérieure, False sinon."""
        return not self.interieur
    
    @property
    def terrain(self):
        """Retourne l'objet terrain."""
        return type(self).importeur.salle.terrains[self.nom_terrain]
    
    def personnage_est_present(self, personnage):
        """Si le personnage est présent, retourne True, False sinon."""
        return personnage in self._personnages
    
    def ajouter_personnage(self, personnage):
        """Ajoute le personnage dans la salle"""
        if personnage not in self.personnages:
            self._personnages.append(personnage)
    
    def retirer_personnage(self, personnage):
        """Retire le personnage des personnages présents"""
        if personnage in self.personnages:
            self._personnages.remove(personnage)
    
    def salles_autour(self, rayon=15):
        """Retourne les chemins autour de self dans le rayon précisé."""
        return Chemins.salles_autour(self, rayon)
    
    def envoyer(self, message, *personnages, **kw_personnages):
        """Envoie le message aux personnages présents dans la salle.
        
        Les personnages dans les paramètres supplémentaires (nommés ou non)
        sont utilisés pour formatter le message et font figure d'exceptions.
        Ils ne recevront pas le message.
        
        """
        exceptions = personnages + tuple(kw_personnages.values())
        for personnage in self.personnages:
            if personnage not in exceptions:
                personnage.envoyer(message, *personnages, **kw_personnages)
    
    def envoyer_lisser(self, chaine, *personnages, **kw_personnages):
        """Méthode redirigeant vers envoyer mais lissant la chaîne."""
        self.envoyer(lisser(chaine), *personnages, **kw_personnages)
    
    def get_elements_observables(self, personnage):
        """Retourne une liste des éléments observables dans cette salle."""
        return []
    
    def regarder(self, personnage):
        """Le personnage regarde la salle"""
        res = ""
        if personnage.est_immortel():
            res += "# |rgc|" + self.nom_zone + "|ff|:|vrc|" + self.mnemonic
            res += "|ff| ({})".format(self.coords)
            res += "\n\n"
        res += "   |tit|" + (self.titre or "Une salle sans titre") + "|ff|\n\n"
        description = self.description.regarder(personnage, self)
        if not description:
            description = "   Vous êtes au milieu de nulle part."
        res += description + "\n"
        plus = self.decrire_plus(personnage)
        if plus:
            res += plus + "\n"
        
        liste_messages = []
        flags = 0
        type(self).importeur.hook["salle:regarder"].executer(self,
                liste_messages, flags)
        if liste_messages:
            res += "|cy|" + "\n".join(liste_messages) + "|ff|\n"
        res += "\nSorties : "
        res += self.afficher_sorties(personnage)
        
        # Personnages
        personnages = OrderedDict()
        # Si le personnage est un joueur, il se retrouve avec un nombre de 1
        # Si le personnage est un PNJ, on conserve son prototype avec
        # le nombre d'occurences de prototypes apparaissant
        for personne in self.personnages:
            if personne is not personnage:
                if not hasattr(personne, "prototype"):
                    personnages[personne] = 1
                else:
                    personnages[personne.prototype] = personnages.get(
                            personne.prototype, 0) + 1
        
        if len(personnages):
            res += "\n"
            
            for personne, nombre in personnages.items():
                res += "\n- {}".format(personne.get_nom_etat(personnage,
                        nombre))
        
        # Objets
        noms_objets = self.afficher_noms_objets()
        if len(noms_objets):
            res += "\n"
            for nom_objet in noms_objets:
                res += "\n+ {}".format(nom_objet)
        
        return res
    
    def afficher_sorties(self, personnage):
        """Affiche les sorties de la salle"""
        noms = []
        for nom in NOMS_SORTIES.keys():
            sortie = self.sorties[nom]
            if sortie:
                nom = sortie.nom
            
            nom_aff = self.sorties.get_nom_abrege(nom)
            if self.sorties.sortie_existe(nom):
                if sortie.porte and sortie.porte.fermee:
                    res = "[|rgc|" + nom_aff + "|ff|]"
                else:
                    res = "|vr|" + nom_aff + "|ff|"
                if sortie.cachee:
                    if personnage.est_immortel():
                        res = "|rg|(I)|ff|" + res                
                    else:
                        res = " ".ljust(len(self.sorties.get_nom_abrege(
                                sortie.direction)))
            else:
                res = " ".ljust(len(nom_aff))
            
            noms.append(res)
        
        return ", ".join(noms) + "."
    
    def afficher_noms_objets(self):
        """Retourne les noms et états des objets sur le sol de la salle"""
        objets = []
        for o, nb in self.objets_sol.get_objets_par_nom():
            objets.append(o.get_nom_etat(nb))
        
        return objets
    
    def decrire_plus(self, personnage):
        """Ajoute un message au-dessous de la description.
        
        Si cette méthode retourne une chaîne non vide, alors cette chaîne
        sera ajoutée sous la description quand un personnage regardera
        la salle.
        
        """
        pass
    
    def pop_pnj(self, pnj):
        """Méthode appelée quand un PNJ pop dans la salle."""
        pro = pnj.prototype
        if pro in self.pnj_repop:
            self.pnj_repop[pro] = self.pnj_repop[pro] - 1
    
    def det_pnj(self, pnj):
        """Méthode appelée quand un PNJ disparaît.."""
        pro = pnj.prototype
        if pro in self.pnj_repop:
            self.pnj_repop[pro] = self.pnj_repop[pro] + 1
    
    def repop(self):
        """Méthode appelée à chaque repop."""
        for pro, nb in self.pnj_repop.items():
            if nb > 0:
                for i in range(nb):
                    importeur.pnj.creer_PNJ(pro, self)
