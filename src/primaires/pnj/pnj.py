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


"""Fichier contenant la classe PNJ, détaillée plus bas."""

import sys

from abstraits.obase import BaseObj
from primaires.perso.personnage import Personnage

class PNJ(Personnage):
    
    """Classe représentant un PNJ, c'est-à-dire un personnage virtuel.
    
    Ce personnage est géré par l'univers et n'est pas connecté, à
    la différence d'un joueur.
    
    """
    
    enregistrer = True
    def __init__(self, prototype, salle=None):
        """Constructeur du PNJ"""
        Personnage.__init__(self)
        self._nom = ""
        self.prototype = prototype
        self.salle = salle
        self.salle_origine = salle
        self.controle_par = None
        self.instance_connexion = None
        if salle:
            salle.pop_pnj(self)
        
        if prototype:
            prototype.no += 1
            self.identifiant = prototype.cle + "_" + str(
                    prototype.no)
            prototype.pnj.append(self)
            
            # On copie les attributs propres à l'objet
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                setattr(self, nom, val.construire(self))
            
            # On force l'écriture de la race
            self.race = prototype.race
            for stat in prototype.stats:
                t_stat = getattr(self.stats, "_{}".format(stat.nom))
                t_stat.defaut = stat.defaut
                t_stat.courante = stat.defaut
            self.lier_equipement(prototype.squelette)
            
            # Copie de l'équipement
            for membre, p_objet in prototype.equipement.items():
                if self.equipement.squelette.a_membre(membre):
                    objet = importeur.objet.creer_objet(p_objet)
                    self.equipement.equiper_objet(membre, objet)
    
    def __getnewargs__(self):
        return (None, )
    
    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype
        
        """
        if nom_attr == "prototype":
            return object.__getattr__(self, nom_attr)
        else:
            try:
                return Personnage.__getattr__(self, nom_attr)
            except AttributeError:
                return getattr(self.prototype, nom_attr)
    
    def __repr__(self):
        return "<pnj {}>".format(self.identifiant)
    
    def _get_nom(self):
        """Retourne le nom singulier définit dans le prototype.
        
        Toutefois, si le nom est définit dans le PNJ lui-même
        (l'attribut _nom n'est pas vide), retourne celui-ci.
        
        """
        nom = self._nom
        if not nom:
            nom = self.prototype.nom_singulier
        
        return nom
    def _set_nom(self, nouveau_nom):
        """Ecrit le nom dans self._nom.
        
        Note contextuelle : si le nouveau nom est vide, le nom redeviendra
        le nom singulier du prototype.
        
        """
        self._nom = nouveau_nom
    nom = property(_get_nom, _set_nom)
    
    def _set_race(self, race):
        self._race = race
    race = property(Personnage._get_race, _set_race)
    
    def _get_contextes(self):
        return self.controle_par and self.controle_par.contextes or \
                None
    def _set_contextes(self, contextes):
        pass
    contextes = property(_get_contextes, _set_contextes)
    
    def _get_alias(self):
        alias = {}
        if self.controle_par:
            return self.controle_par.alias
        return alias
    def _set_alias(self, alias):
        pass
    alias = property(_get_alias, _set_alias)
    
    def _get_langue_cmd(self):
        if self.controle_par:
            return self.controle_par.langue_cmd
        else:
            return "francais"
    def _set_langue_cmd(self, langue):
        pass
    langue_cmd = property(_get_langue_cmd, _set_langue_cmd)
    
    def envoyer(self, msg, *personnages, **kw_personnages):
        """Envoie un message"""
        if self.controle_par:
            self.controle_par.envoyer(msg, *personnages,
                    **kw_personnages)
    
    def get_nom_pour(self, personnage):
        """Retourne le nom pour le personnage passé en paramètre."""
        return self.nom_singulier
    
    def mourir(self):
        """La mort d'un PNJ signifie sa destruction."""
        Personnage.mourir(self)
        type(self).importeur.pnj.supprimer_PNJ(self.identifiant)
    
    @property
    def nom_unique(self):
        return self.identifiant
    
    def get_distinction_audible(self):
        return self.nom_singulier
    
    def tick(self):
        """Méthode appelée à chaque tick."""
        Personnage.tick(self)
    
    def regarder(self, personnage):
        """personnage regarde self."""
        self.script["regarde"]["avant"].executer(personnage=personnage,
                pnj=self)
        Personnage.regarder(self, personnage)
        self.script["regarde"]["après"].executer(personnage=personnage,
                pnj=self)
    
    def detruire(self):
        """Destruction du PNJ."""
        self.decontroller()
        Personnage.detruire(self)
        if self in self.prototype.pnj:
            self.prototype.pnj.remove(self)
        
        if self.salle_origine:
            self.salle_origine.det_pnj(self)
    
    def decontroller(self):
        """Arrête de contrôler self."""
        if self.controle_par:
            try:
                contexte = \
                    self.controle_par.contextes.get_contexte_par_unom(
                    "ctrl_pnj(" + self.identifiant + ")")
            except KeyError:
                pass
            else:
                self.controle_par.contextes.retirer(contexte)
                self.controle_par = None
                self.instance_connexion = None
