# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le module secondaire botanique."""

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from .plante import Plante
from .prototype import PrototypePlante
from .detail import DetailMod

class Module(BaseModule):
    
    """Module secondaire définissant la botanique.
    
    Y sont définis :
    -   Les plantes, arbres
    -   Les différents éléments récoltables
    -   Les commandes recolter et planter
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "botanique", "secondaire")
        self.commandes = []
        self.prototypes = {}
        self.plantes = {}
        self.salles = {}
        self.logger = importeur.man_logs.creer_logger(
                "botanique", "botanique")
    
    def config(self):
        """Configuration du module."""
        importeur.temps.met_changer_annee.append(self.actualiser_cycles)
        importeur.temps.met_changer_jour.append(self.actualiser_periodes)
        importeur.salle.details_dynamiques.append(self.detailler_salle)
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module."""
        # On récupère les prototypes
        prototypes = importeur.supenr.charger_groupe(PrototypePlante)
        for prototype in prototypes:
            self.ajouter_prototype(prototype)
            if prototype.plantes:
                prototype.n_id = max(p.n_id for p in \
                        prototype.plantes) + 1
        
        nb_prototypes = len(prototypes)
        self.logger.info(format_nb(nb_prototypes, "{nb} prototype{s} " \
                "de plante récupéré{s}"))
        
        # On récupère les plantes
        plantes = self.importeur.supenr.charger_groupe(Plante)
        for plante in plantes:
            self.ajouter_plante(plante)
        
        nb_plantes = len(plantes)
        self.logger.info(format_nb(nb_plantes, "{nb} plante{s} " \
                "récupérée{s}", fem=True))
        
        BaseModule.init(self)
    
    def creer_prototype(self, cle):
        """Création du prototype de plante."""
        if cle in self.prototypes:
            raise KeyError("la clé {} existe déjà".format(cle))
        
        prototype = PrototypePlante(cle)
        self.ajouter_prototype(prototype)
        return prototype
    
    def ajouter_prototype(self, prototype):
        """Ajout du prototype au dictionnaire."""
        self.prototypes[prototype.cle] = prototype
    
    def supprimer_prototype(self, cle):
        """Suppression du prototype."""
        prototype = self.prototypes[cle]
        prototype.detruire()
        del self.prototypes[cle]
    
    def creer_plante(self, prototype, salle):
        """Création de la plante."""
        plante = Plante(prototype, salle)
        self.ajouter_plante(plante)
        return plante
    
    def ajouter_plante(self, plante):
        """Ajout de la plante au dictionnaire."""
        self.plantes[plante.identifiant] = plante
        ls_plantes = self.salles.get(plante.salle, [])
        ls_plantes.append(plante)
        self.salles[plante.salle] = ls_plantes
    
    def supprimer_plante(self, cle):
        """Suppression de la plante."""
        plante = self.plantes[cle]
        if plante.salle in self.salles and plante in \
                self.salles[plante.salle]:
            self.salles[plante.salle].remove(plante)
        
        plante.detruire()
        del self.plantes[cle]
    
    def actualiser_cycles(self):
        """Actualise les cycles de TOUTES les plantes.
        
        Cette méthode n'est censée être appelée qu'à chaque nouvelle année.
        
        """
        for plante in list(self.plantes.values()):
            plante.age += 1
            if plante.age >= plante.cycle.fin:
                n_cycle = plante.cycle.cycle_suivant
                if n_cycle is None:
                    self.supprimer_plante(plante.identifiant)
                else:
                    plante.periode = cycle.periodes[0]
    
    def actualiser_periodes(self):
        """Actualise les périodes de TOUTES les plantes.
        
        Cette méthode n'est censée être appelée qu'à chaque nouveau jour.
        
        """
        for plante in list(self.plantes.values()):
            if plante.periode.finie:
                plante.periode = plante.periode.periode_suivante
            plante.actualiser_elements()
    
    def detailler_salle(self, salle, personnage):
        """Détailler la salle salle pour personnage.
        
        On ajoute :
        -   Le détail végétation
        -   Les différents végétaux observabes.
        
        """
        det = DetailMod(salle)
        print("Ajout de", det.nom)
        return [det]
