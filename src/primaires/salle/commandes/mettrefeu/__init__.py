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


"""Package contenant la commande 'mettrefeu'."""

from random import random, randint, choice
from math import sqrt

from primaires.interpreteur.commande.commande import Commande

class CmdMettreFeu(Commande):
    
    """Commande 'mettrefeu'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "mettrefeu", "setfire")
        self.nom_categorie = "objets"
        self.aide_courte = "allume ou entretient un feu"
        self.aide_longue = \
            "Cette commande permet d'allumer un feu si vous tenez une " \
            "pierre ou un briquet et qu'il y a du combustible dans la " \
            "salle ; si un feu est déjà allumé et qu'il y a du combustible, " \
            "elle le nourrit."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        combustibles = importeur.objet.prototypes.values()
        combustibles = [c for c in combustibles \
                if c.est_de_type("combustible")]
        objets_sol = list(salle.objets_sol)
        somme_combu = 0
        for objet in list(objets_sol):
            if objet.prototype in combustibles:
                somme_combu += objet.qualite
        if not somme_combu:
            personnage << "|err|Il n'y a rien qui puisse brûler par ici.|ff|"
            return
        # On tente d'allumer ou de nourrir le feu
        if salle.ident in importeur.salle.feux:
            feu = importeur.salle.feux[salle.ident]
            feu.puissance += somme_combu
            personnage << "Vous poussez du bois dans le feu et celui-ci " \
                    "gagne en vigueur et en éclat."
            for objet in objets_sol:
                if objet.prototype in combustibles:
                    objets_sol.retirer(objet)
                    if objet.identifiant:
                        importeur.objet.supprimer_objet(
                                objet.identifiant)
        else:
            pierre = None
            for objet, qtt, t_conteneur in \
                    personnage.equipement.inventaire.iter_objets_qtt(
                    conteneur=True):
                if objet.est_de_type("pierre à feu"):
                    pierre = objet
                    conteneur = t_conteneur
                    break
            if not pierre:
                personnage << "|err|Vous ne tenez rien pour allumer.|ff|"
                return
            personnage.pratiquer_talent("feu_camp")
            niveau = sqrt(personnage.get_talent("feu_camp") / 100)
            efficace = pierre.efficacite / 50
            if pierre.efficacite > 0:
                pierre.efficacite -= 1
            proba_marche = random()
            # Si la pierre fonctionne
            if proba_marche <= efficace:
                proba_reussit = round(random(), 1)
                if proba_reussit <= niveau:
                    personnage << "Une étincelle vole et le feu prend."
                    feu = importeur.salle.allumer_feu(salle, somme_combu)
                    personnage.gagner_xp("survie", somme_combu * 20)
                    for objet in objets_sol:
                        if objet.prototype in combustibles:
                            if objet.identifiant:
                                importeur.objet.supprimer_objet(
                                        objet.identifiant)
                    feu.stabilite = 1 - niveau ** (1/3)
                    return
            personnage << "Le feu refuse de démarrer."            
            proba_casse = random()
            solidite = efficace ** (1 / 5)
            if proba_casse >= solidite:
                personnage << "{} se brise en mille morceaux.".format(
                        pierre.nom_singulier)
                conteneur.retirer(pierre)
                importeur.objet.supprimer_objet(pierre.identifiant)
