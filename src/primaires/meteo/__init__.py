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


"""Fichier contenant le module primaire meteo."""

from random import choice, randint
from math import ceil

from abstraits.module import *
from .config import cfg_meteo
from .perturbations import perturbations
from .perturbations.base import BasePertu, AUCUN_FLAG

class Module(BaseModule):
    
    """Cette classe représente le module primaire meteo.
    
    Comme son nom l'indique, ce module gère la météorologie dans l'univers.
    La météo est régie par un ensemble de perturbations se déplaçant
    de façon semi-aléatoire dans l'univers. Ces perturbations sont décrites
    dans le dossier correspondant ; une partie de leur comportement
    est configurable.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "meteo", "primaire")
        self.perturbations_actuelles = []
    
    def config(self):
        """Configuration du module"""
        self.cfg = type(self.importeur).anaconf.get_config("config_meteo",
                "meteo/config.cfg", "config meteo", cfg_meteo)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""        
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.donner_meteo)
        self.perturbations_actuelles = self.importeur.supenr.charger_groupe(
                BasePertu)
        BaseModule.init(self)
    
    def preparer(self):
        """Préparation du module"""
        self.cycle_meteo()
    
    def cycle_meteo(self):
        self.importeur.diffact.ajouter_action("cycle_meteo", 60,
                self.cycle_meteo)
        # On tue les perturbations trop vieilles
        for pertu in self.perturbations_actuelles:
            if pertu.age >= pertu.duree:
                i = randint(0, 100)
                nom_pertu_enchainer = ""
                msg_enchainement = ""
                for fin in pertu.fins_possibles:
                    if i <= fin[2]:
                        nom_pertu_enchainer = fin[0]
                        msg_enchainement = fin[1]
                        break
                if not nom_pertu_enchainer:
                    for salle in pertu.liste_salles_sous:
                        if salle.exterieur:
                            salle.envoyer("|cy|" + pertu.message_fin + "|ff|",
                                    prompt=False)
                else:
                    for salle in pertu.liste_salles_sous:
                        if salle.exterieur:
                            salle.envoyer("|cy|" + msg_enchainement + "|ff|",
                                    prompt=False)
                    cls_pertu_enchainer = None
                    for pertu_existante in perturbations:
                        if pertu_existante.nom_pertu == nom_pertu_enchainer:
                            cls_pertu_enchainer = pertu_existante
                            break
                    if cls_pertu_enchainer is not None:
                        pertu_enchainer = cls_pertu_enchainer(pertu.centre)
                        pertu_enchainer.rayon = pertu.rayon
                        pertu_enchainer.dir = pertu.dir
                        self.perturbations_actuelles.append(pertu_enchainer)
                    else:
                        print("la perturbation {} n'existe pas". \
                                format(nom_pertu_enchainer))
                pertu.detruire()
                self.perturbations_actuelles.remove(pertu)
            # On fait bouger les perturbations existantes
            pertu.cycle()
        # On tente de créer une perturbation
        if len(self.perturbations_actuelles) < self.cfg.nb_pertu_max:
            salles = list(self.importeur.salle._salles.values())
            try:
                salle_dep = choice(salles)
                cls_pertu = choice(perturbations)
            except IndexError:
                pass
            else:
                deja_pertu = False
                for pertu in self.perturbations_actuelles:
                    if pertu.est_sur(salle_dep):
                        deja_pertu = True
                        break
                if salle_dep.coords.valide and not deja_pertu:
                    pertu = cls_pertu(salle_dep.coords.get_copie())
                    self.perturbations_actuelles.append(pertu)
                    for salle in pertu.liste_salles_sous:
                        if salle.exterieur:
                            salle.envoyer("|cy|" + pertu.message_debut + "|ff|",
                                    prompt=False)
    
    def donner_meteo(self, salle, liste_messages, flags):
        """Affichage de la météo d'une salle"""
        if salle.exterieur:
            res = ""
            for pertu in self.perturbations_actuelles:
                if pertu.est_sur(salle):
                    res += pertu.message_pour(salle)
                    break
            if not res:
                res += self.cfg.beau_temps
            liste_messages.append("|cy|" + res + "|ff|")
