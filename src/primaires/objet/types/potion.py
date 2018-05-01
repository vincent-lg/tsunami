# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 EILERS Christoff
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


"""Fichier contenant le type Potion."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from bases.objet.attribut import Attribut
from .base import BaseType

class Potion(BaseType):
    
    """Type d'objet: potion.
    
    """
    
    nom_type = "potion"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.qualite = 1
        self.remplissant = 1
        self.message_boit = "Vous buvez {}.".format(self.nom_singulier)
        self.etendre_editeur("a", "qualité", Entier, self, "qualite", 1, 10)
        self.etendre_editeur("r", "remplissant", Entier, self, "remplissant",
                1, 10)
        self.etendre_editeur("i", "message d'ingestion", Uniligne, self,
                "message_boit")
    
    def etendre_script(self):
        """Extension du scripting."""
        evt_boit = self.script.creer_evenement("boit")
        evt_boit.aide_courte = "le personnage boit la potion"
        evt_boit.aide_longue = \
            "Cet évènement est appelé quand le personnage boit la potion."
        var_perso = evt_boit.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage buvant la potion"
        var_objet = evt_boit.ajouter_variable("objet", "Objet")
        var_objet.aide = "la potion bue"

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        qualite = enveloppes["a"]
        qualite.apercu = "{objet.qualite}"
        qualite.prompt = "Qualité de la potion : "
        qualite.aide_courte = \
            "Entrez la |ent|qualité|ff| de la potion, entre |cmd|1|ff| " \
            "et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Qualité actuelle : {objet.qualite}"
        
        remplissant = enveloppes["r"]
        remplissant.apercu = "{objet.remplissant}"
        remplissant.prompt = "Valeur remplissante : "
        remplissant.aide_courte = \
            "Entrez la |ent|valeur remplissante|ff| de la potion, entre " \
            "|cmd|1|ff| et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\n" \
            "Valeur remplissante actuelle : {objet.remplissant}"
        
        message_boit = enveloppes["i"]
        message_boit.prompt = "Message lors de l'ingestion : "
        message_boit.aide_courte = \
            "Entrez le |ent|texte|ff| affiché au joueur lorsqu'il boit la potion ou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\n" \
            "Message présent : {objet.message_boit}"
