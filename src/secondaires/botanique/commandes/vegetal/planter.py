﻿# -*-coding:Utf-8 -*

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


"""Fichier contenant le paramètre 'planter' de la commande 'vegetal'."""

from random import random

from primaires.interpreteur.masque.parametre import Parametre

class PrmPlanter(Parametre):
    
    """Commande 'vegetal planter'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "planter", "plant")
        self.schema = "<options>"
        self.aide_courte = "plante un végétal"
        self.aide_longue = \
            "Cette commande permet de planter un ou plusieurs végétaux, " \
            "dans une salle, répartis aléatoirement sur une zone " \
            "et avec de nombreux paramètres. Elle permet par exemple " \
            "de planter entre 5 et 7 pommiers dans les terrains " \
            "forêt de la zone picte en les répartissant équitablement. " \
            "Elle permet aussi de planter un unique pommier dans " \
            "la salle où on se trouve."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        options = self.noeud.get_masque("options")
        options.proprietes["options_courtes"] = "'c:n:t:z:m:a:s'"
        options.proprietes["options_longues"] = "['cle=', 'nombre=', " \
                "'terrains=', 'zone=', 'mnemo=', 'age=', 'salle-courante']"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # Paramètres par défaut
        salles = []
        nb_plantes = 1
        terrains = ["forêt", "plaine", "rive"]
        cle = ""
        age = 0
        zone = ""
        mnemo = ""
        
        # Traitement des options
        if dic_masques["options"] is not None:
            options = dic_masques["options"].options
            if "cle" in options:
                cle = options["cle"]
            if "nombre" in options:
                nombre = options["nombre"]
                try:
                    nombre = int(nombre)
                    assert nombre > 0
                except (ValueError, AssertionError):
                    personnage << "|err|Nombre invalide.|ff|"
                    return
                else:
                    nb_plantes = nombre
            if "terrains" in options:
                terrains = options["terrains"].split(",")
                terrains = [t.strip() for t in terrains if t.strip()]
            if "salle-courante" in options:
                salles = [personnage.salle]
                nb_plantes = 1
            if "zone" in options:
                zone = options["zone"]
            if "mnemo" in options:
                mnemo = options["mnemo"]
            if "age" in options:
                nombre = options["age"]
                try:
                    nombre = int(nombre)
                    assert nombre >= 0
                except (ValueError, AssertionError):
                    personnage << "|err|Nombre invalide.|ff|"
                    return
                else:
                    age = nombre
        
        print("salles =", salles, "nb_plantes =", nb_plantes, "terrains =",
                terrains, "zone =", zone, "mnémo =", mnemo, "age =", age)
        personnage << "ok"
        
        # Convertion des terrains
        nom_terrains = terrains
        terrains = []
        for terrain in nom_terrains:
            try:
                terrain = importeur.salle.terrains[terrain]
            except KeyError:
                personnage << "|err|Terrain {} introuvable.|ff|".format(
                        terrain)
                return
            
            if terrain.nom not in importeur.botanique.terrains_recoltables:
                personnage << "|err|Vous ne pouvez rien planter en " \
                        "terrain {}.|ff|".format(terrain.nom)
                return
            
            terrains.append(terrain)
        
        if not cle:
            personnage << "|err|Aucune clé de prototype végétal n'a " \
                    "été précisée.|ff|"
            return
        
        if not terrains:
            personnage << "|err|Aucun terrain n'a été défini.|ff|"
            return
        
        if zone:
            salles = list(importeur.salle.salles.values())
        
        salles = [s for s in salles if s.terrain in terrains]
        if not salles:
            personnage << "|err|Aucune salle n'a été trouvée.|ff|"
            return
        
        try:
            prototype = importeur.botanique.prototypes[cle]
        except KeyError:
            personnage << "|err|Prototype végétal {} inconnu.|ff|".format(
                    cle)
            return
        
        if zone:
            salles = [s for s in salles if s.nom_zone == zone]
            if not salles:
                personnage << "|err|Aucune salle n'est trouvée " \
                        "dans la zone spécifiée.|ff|"
                return
        
        if mnemo:
            salles = [s for s in salles if s.mnemonic.startswith(mnemo)]
            if not salles:
                personnage << "|err|Aucune salle n'est trouvée " \
                        "commençant par le mnémonique spécifié.|ff|"
                return
        
        # On plante maintenant les plantes dans les salles spécifiées
        nb = 0
        nb_par_salle = int(nb_plantes / len(salles))
        if nb_par_salle < 1:
            nb_par_salle = 1
        
        fact = nb_plantes / len(salles) * nb_par_salle
        for salle in salles:
            for i in range(nb_par_salle):
                if random() <= fact:
                    plante = importeur.botanique.creer_plante(prototype, salle)
                    plante.age = age
                    nb += 1
        
        personnage << "{} plante(s) créée(s).".format(nb)