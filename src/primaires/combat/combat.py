# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant la classe Combat, détaillée plus bas."""

from random import choice, randint

from corps.aleatoire import varier
from .attaque import Coup

CLE_TALENT_ESQUIVE = "esquive"
CLE_TALENT_PARADE = "parade"
CLE_TALENT_MAINS_NUES = "combat_mains_nues"

class Combat:
    
    """Classe représentant un combat dans une salle.
    
    Un combat est constitué :
        combattants -- D'une liste de combattants
        combattus -- d'un dictionnaire combattant: combattu
    
    A chaque tour (appelle à la méthode tour), les combattants combattent
    selon des règles définies dans ce module. Voir la méthode 'tour'
    pour plus d'informations.
    
    """
    
    def __init__(self, salle):
        """Constructeur d'un combat."""
        self.salle = salle
        self.__combattants = []
        self.__combattus = {}
    
    @property
    def combattants(self):
        """Retourne une liste déréférencée des combattants."""
        return list(self.__combattants)
    
    @property
    def combattus(self):
        """Retourne un dictionnaire déréférencé des combattus."""
        return dict(self.__combattus)
    
    def ajouter_combattants(self, combattant, combattu):
        """Ajoute les combattants."""
        if combattant not in self.__combattants:
            self.__combattants.append(combattant)
            self.__combattus[combattant] = combattu
        
        if combattu not in self.__combattants:
            self.__combattants.append(combattu)
            self.__combattus[combattu] = combattant
    
    def verifier_combattants(self):
        """VVérifie que tous les combattants sont bien dans la salle."""
        for combattant in self.combattants:
            if combattant.salle != self.salle:
                self.__combattants.remove(combattant)
        
        for combattant, combattu in self.combattus.items():
            if combattant.salle != self.salle:
                del self.__combattus[combattant]
            elif combattu.salle != self.salle:
                self.__combattus[combattant] = None
        
        # Les combattants ne combattant personne essayent de trouver une
        # autre cible
        for combattant, combattus in self.combattus.items():
            if combattu is None:
                # On liste les cibles possibles du combattant
                # (ceux qui le combattent)
                cibles = [cbt for cbt, cbu in self.combattus.items() if \
                        cbu == combattant]
                if cibles:
                    cible = choice(cibles)
                    self.__combattus[combattant] = cible
    
    def get_attaques(self, personnage):
        """Retourne les attaques du personnage."""
        return (Coup(personnage), )
    
    def defendre(self, combattant, combattu, attaque, membre, degats, arme):
        """combattu tente de se défendre.
        
        Retourne les dégâts finalement infligés.
        
        Si la défense est totale, retourne 0.
        
        """
        if varier(combattu.pratiquer_talent(CLE_TALENT_ESQUIVE), 15) >= \
                randint(1, 80):
            attaque.envoyer_msg_tentative(combattant, combattu, membre, arme)
            combattant.envoyer("{} esquive votre coup.", combattu)
            combattu.envoyer("Vous esquivez le coup porté par {}.",
                    combattant)
            combattant.salle.envoyer("{} esquive le coup porté par {}.",
                    combattu, combattant)
            degats = 0
        elif membre:
            objet = membre.equipe
            if objet.est_de_type("armure"):
                encaisse = objet.encaisser(arme, degats)
                degats -= encaisse
        
        return degats
    
    def tour(self, importeur):
        """Un tour de combat."""
        self.verifier_combattants()
        for combattant, combattu in self.combattus.items():
            armes = combattant.get_armes()
            armes = armes if armes else [None]
            for arme in armes:
                attaques = self.get_attaques(combattant)
                attaque = choice(attaques)
                membre = attaque.get_membre(combattant, combattu, arme)
                if attaque.essayer(combattant, combattu, arme):
                    degats = attaque.calculer_degats(combattant, combattu,
                            membre, arme)
                    
                    # Défense
                    degats = self.defendre(combattant, combattu, attaque,
                            membre, degats, arme)
                    if degats:
                        attaque.envoyer_msg_reussite(combattant, combattu,
                                membre, degats, arme)
                else:
                    attaque.envoyer_msg_tentative(combattant, combattu,
                            membre, arme)
        
        self.verifier_combattants()
        importeur.diffact.ajouter_action(
            "combat:{}".format(self.salle.ident), 3, self.tour, importeur)
