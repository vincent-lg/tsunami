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


"""Fichier contenant le type jeu."""

from bases.collections.liste_id import ListeID
from bases.objet.attribut import Attribut

from primaires.interpreteur.editeur.choix import Choix
from primaires.objet.types.base import BaseType

class ObjetJeu(BaseType):
    
    """Type d'objet: jeu.
    
    """
    
    nom_type = "jeu"
    
    def __init__(self, cle=""):
        """Constructeur du type jeu"""
        BaseType.__init__(self, cle)
        
        self.jeu = None
        self.etendre_editeur("j", "Type de jeu", Choix, self, "jeu")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.
        
        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.
        
        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.
        
        """
        jeux = type(self).importeur.jeux.jeux
        
        env = enveloppes["j"] # on récupère 'jeu'
        env.prompt = "Entrez un nom de jeu : "
        env.apercu = self.jeu and "{objet.jeu}" or ""
        env.aide_courte = \
            "Entrez le nom du jeu ou |cmd|/|ff| pour revenir à " \
            "la fenêtre mère.\n\n" \
            "Jeu possible :\n" + \
            ", ".join(sorted(jeux.keys())) + "\n\n" \
            "Jeu actuel : " + \
            "|bc|{objet.nom_jeu} |ff|"
        
    # Actions sur les objets
    def regarder(self, personnage):
        moi = BaseType.regarder(self, personnage) + "\n\n"
        moi += self.jeu.regarder(moi)
        return moi
