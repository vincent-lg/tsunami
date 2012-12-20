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


"""Fichier contenant le type boule de neige."""

from datetime import datetime

from bases.objet.attribut import Attribut
from corps.aleatoire import *
from primaires.salle.salle import Salle
from primaires.perso.personnage import Personnage
from .base import BaseType

class BouleNeige(BaseType):
    
    """Type d'objet: boule de neige."""
    
    nom_type = "boule de neige"
    selectable = False
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.nom_singulier = "une boule de neige"
        self.nom_pluriel = "boules de neige"
        self.etat_singulier = "se trouve ici"
        self.etat_pluriel = "se trouvent là"
        
        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "apparition": Attribut(datetime.now),
        }
    
    def poser(self, objet, personnage):
        """On pose l'objet."""
        if isinstance(objet.contenu, Salle) and \
                (datetime.now() - objet.apparition).seconds < 100:
            objet.apparition = datetime.now()
        BaseType.poser(self, objet, personnage)
    
    def veut_jeter(self, personnage, sur):
        """Le personnage veut jeter l'objet sur sur."""
        if isinstance(sur, Personnage):
            return "jeter_personnage"
        
        return ""
    
    def jeter(self, personnage, adversaire):
        """Jète la boule de neige sur un adversaire."""
        fact = varier(personnage.agilite, 20) / 100
        fact *= (1.6 - personnage.poids / personnage.poids_max)
        fact_a = varier(adversaire.agilite, 20) / 100
        fact_a *= (1.6 - adversaire.poids / adversaire.poids_max)
        reussite = fact >= fact_a
        if reussite:
            personnage.envoyer("Vous lancez {} sur {{}}.".format(
                    self.get_nom()), adversaire)
            adversaire.envoyer("{{}} vous lance {} dessus !".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} sur {{}}.".format(
                    self.get_nom()), personnage, adversaire)
        else:
            personnage.envoyer("Vous lancez {} mais manquez {{}}".format(
                    self.get_nom()), adversaire)
            personnage.salle.envoyer("{{}} envoie {} mais manque {{}}.".format(
                    self.get_nom()), personnage, adversaire)
            importeur.objet.supprimer_objet(self.identifiant)
        
        return reussite
    
    def jeter_personnage(self, personnage, adversaire):
        pass
    
    def nettoyage_cyclique(self):
        """Nettoyage cyclique de la boule de neige."""
        parent = self.grand_parent
        if not isinstance(parent, Salle) and \
                (datetime.now() - self.apparition).seconds > 300:
            parent.envoyer("{} fond puis disparaît en quelques gouttes " \
                    "d'eau.".format(self.get_nom()))
            importeur.objet.supprimer_objet(self.identifiant)
