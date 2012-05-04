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


"""Fichier contenant l'action donner_xp_rel."""

from primaires.scripting.action import Action
from primaires.format.fonctions import supprimer_accents

class ClasseAction(Action):
    
    """Donne de l'XP relative à un personnage.
    
    L'XP relative est calculée en fonction de deux informations :
      * Le niveau prévu
      * Le pourcentage d'XP attendue.
    
    Quand on précise gagner 10% du niveau 5, un personnage niveau
    5 gagnera 10% de l'XP nécessaire pour passer son niveau mais
    un personnage niveau 4 gagnera moins de 10% du niveau 4,
    un personnage niveau 8 gagnera peut-être 6% seulement du niveau
    8, ainsi de suite.
    
    """
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.xp_principal, "Personnage", "Fraction",
                "Fraction")
        cls.ajouter_types(cls.xp_secondaire, "Personnage", "str", "Fraction",
                "Fraction")
    
    @staticmethod
    def xp_principal(personnage, niveau_prevu, pourcentage):
        """Donne l'XP relative au personnage dans le niveau principal."""
        niveau_prevu = int(niveau_prevu)
        if niveau_prevu < 1 or niveau_prevu > \
                importeur.perso.gen_niveaux.nb_niveaux:
            raise ErreurExecution("le niveau prévu doit être entre 1 et " \
                    "{}".format(importeur.perso.gen_niveaux.nb_niveaux))
        
        personnage.gagner_xp_rel(niveau_prevu, int(pourcentage))
    
    @staticmethod
    def xp_secondaire(personnage, niveau_secondaire, niveau_prevu,
            pourcentage):
        """Donne l'XP absolue au personnage dans le niveau secondaire.
        
        Le nom du niveau secondaire doit être donné en son entier.
        Une partie de l'XP est automatiquement transmise au niveau principal.
        
        Note : l'XP relative est calculée pour le niveau secondaire
        mais pas pour le niveau principal. Le niveau principal actuel
        n'est pas pris en compte dans le calcul de l'XP relative.
        
        """
        niveaux = [n for n in importeur.perso.niveaux.values() if \
                supprimer_accents(n.nom).lower() == supprimer_accents(
                niveau_secondaire)]
        if not niveaux:
            raise ErreurExecution("le niveau {} est introuvable".format(
                    niveau_secondaire))
        
        niveau_prevu = int(niveau_prevu)
        if niveau_prevu < 1 or niveau_prevu > \
                importeur.perso.gen_niveaux.nb_niveaux:
            raise ErreurExecution("le niveau prévu doit être entre 1 et " \
                    "{}".format(importeur.perso.gen_niveaux.nb_niveaux))
        
        personnage.gagner_xp_rel(niveau_prevu, int(pourcentage),
                niveaux[0].cle)
