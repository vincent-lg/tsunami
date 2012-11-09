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


"""Package contenant la commande 'meteo liste'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):
    
    """Commande 'meteo liste'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les perturbations actuelles"
        self.aide_longue = \
            "Cette commande affiche les perturbations actuelles dans un " \
            "tableau récapitulatif."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        pertus = list(importeur.meteo.perturbations_actuelles)
        if len(pertus) == 0:
            personnage << "Aucune perturbation n'existe pour l'instant."
            return
        
        res = [
            "+-----------------+-----+------+-------+--------------+",
            "| Nom             | Age | Vie  | Rayon | (   X,    Y) |",
            "+-----------------+-----+------+-------+--------------+",
        ]
        for perturbation in pertus:
            nom = perturbation.nom_pertu
            age = perturbation.age
            i_vie = int(age / perturbation.duree * 100)
            
            vie = "{}%".format(i_vie)
            rayon = perturbation.rayon
            x = perturbation.centre.x
            y = perturbation.centre.y
            res.append(
                "| {:<15} | {:>3} | {:>4} | {:>5} | ({:>4}, {:>4}) |".format(
                nom, age, vie, rayon, x, y))
        
        res.append(res[0])
        personnage << "\n".join(res)
