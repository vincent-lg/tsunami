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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier contient l'éditeur EdtScript, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *
from .edt_evenement import EdtEvenement

class EdtScript(Editeur):
    
    """Contexte-éditeur des évènements d'uns script.
    
    L'objet appelant est le script.
    Ses évènements se trouvent dans l'attribut evenements
    (en lecture uniquement).
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        script = self.objet
        msg = "| |tit|"
        msg += "Edition des scripts de {}".format(script.parent).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Voici les différents évènements que vous pouvez éditer pour " \
                "cet objet.\n" \
                "Entrez simplement son |ent|nom|ff| pour éditer un " \
                "évènement ou |cmd|/|ff| pour revenir à\n" \
                "la fenêtre parente.\n\n"
        evenements = sorted(script.evenements.values(),
                key=lambda evt: evt.nom)
        if evenements:
            msg += "|cy|Evènements disponibles :|ff|\n\n"
            t_max = 0
            for evt in evenements:
                if len(evt.nom) > t_max:
                    t_max = len(evt.nom)
            lignes = ["  " + evt.nom.ljust(t_max) + " : " + evt.aide_courte \
                    for evt in evenements]
            msg += "\n".join(lignes)
        else:
            msg += "|att|Aucun évènement n'est disponible pour cet objet.|ff|"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        script = self.objet
        nom_evt = supprimer_accents(msg).lower()
        if nom_evt in script.evenements or script.creer_evenement_dynamique(
                msg):
            evenement = script.evenements[nom_evt]
            enveloppe = EnveloppeObjet(EdtEvenement, evenement)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)
            
            self.migrer_contexte(contexte)
        else:
            self.pere << "|err|Cet évènement n'existe pas.|ff|"
