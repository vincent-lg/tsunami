# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Fichier contenant la classe Feu, détaillée plus bas."""

from random import randint, choice, random

from abstraits.obase import BaseObj

class Feu(BaseObj):
    
    """Classe représentant une feu.
    
    Un feu est, aussi simplement que son nom l'indique, un feu de camp, un
    incendie ou autre. Il est caractérisé par une salle parente, et une 
    puissance entre 1 et 100 dont dépendent sa durée de vie et une propension
    à se propager. Les feux sont gérés par le module salle via une action
    différée qui permet leur évolution dans le temps.
    
    Un feu peut en outre être allumé, puis alimenté via deux commandes.
    
    """
    
    _nom = "feu"
    enregistrer = True
    
    def __init__(self, salle, puissance=10):
        """Constructeur d'un feu"""
        BaseObj.__init__(self)
        self.puissance = puissance
        self.salle = salle
        self.stabilite = 0
    
    def __getnewargs__(self):
        return (None, )
    
    def __str__(self):
        """Méthode d'affichage du feu (fonction de la puissance)"""
        cfg_salle = importeur.anaconf.get_config("salle")
        messages_feu = cfg_salle.messages_feu
        for puissance_max, msg in messages_feu:
            if self.puissance <= puissance_max:
                return msg
    
    def bruler(self):
        """Méthode d'action de base du feu"""
        messages_standard = [
            "Une bûche cède soudain dans un grand craquement.",
            "Quelques étincelles volent joyeusement.",
            "Le feu redouble d'ardeur et les flammes montent.",
            "Un crépitement sec retentit.",
            "Une ou deux flammes tentent de s'échapper du foyer.",
            "Les flammes dansent sous un léger coup de vent.",
            "Le feu vascille, hésite et reprend de plus belle.",
            "Les flammes montent à l'assaut d'un nouveau bout de bois.",
            "Une langue de feu s'échappe vers le ciel dans un souffle.",
            "Une branche un peu verte proteste bruyamment.",
        ]
        messages_fin = [
            "Le feu crachote comme un vieillard malade.",
            "Quelques flammes faiblardes tentent de s'extirper de la cendre.",
            "Les flammes se ravivent un instant, puis retombent, vaincues.",
        ]
        if random() < self.stabilite:
            if self.puissance <= 20:
                self.salle.envoyer("Le feu s'éteint sans crier gare, à la " \
                        "faveur d'un souffle d'air.", prompt=False)
                importeur.salle.eteindre_feu(self.salle)
                return
            elif self.puissance <= 40:
                # Entre 20 et 40, on laisse osciller un peu la puissance
                if random() < 0.33:
                    self.puissance += randint(1, 5)
            else:
                self.propager()
                # plus
        # Cas standard, sans tenir compte de l'instabilité
        if self.puissance == 1:
            if random() < 0.20:
                self.salle.envoyer("Un petit nuage de cendres annonce la " \
                        "mort définitive du feu.", prompt=False)
                importeur.salle.eteindre_feu(self.salle)
        elif self.puissance <= 5:
            self.salle.envoyer(choice(messages_fin), prompt=False)
            # On rend le feu instable
            self.stabilite += 1 - self.puissance / 5
            self.puissance -= 1
        elif self.puissance <= 40:
            self.salle.envoyer(choice(messages_standard), prompt=False)
            self.puissance -= 1
        else:
            # Cas de l'incendie
            self.puissance -= 10
    
    def propager(self):
        """Méthode de propagation.
        
        Un feu est maîtrisé jusqu'à une puissance de 40 ; au-delà la
        probabilité qu'il gonfle spontanément et se propage est multipliée.
        Un feu se propage de proche en proche en perdant 10 de puissance à
        chaque fois, mais rien n'empêche qu'il reprenne de la puissance une
        fois installé dans la salle de destination, et ainsi de suite en
        fonction de la météo et d'autres conditions.
        
        Il faudra alors avoir certains talents et faire certaines actions
        (par exemple verser de l'eau) pour endiguer un incendie.
        
        """
        if self.puissance > 30:
            pass
    
    @classmethod
    def repop(cls):
        """Méthode de repop des feux ; boucle sur les feux en déclenchant
        leur méthode bruler.
        
        """
        for feu in list(importeur.salle.feux.values()):
            feu.bruler()
        importeur.diffact.ajouter_action("repop_feux", 5, cls.repop)
