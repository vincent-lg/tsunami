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


"""Contexte-éditeur 'edt_membre', voir plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import oui_ou_non
from primaires.format.fonctions import supprimer_accents
from primaires.perso.membre import FLAGS

class EdtMembre(Editeur):

    """Contexte d'édition d'un membre.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("f", self.opt_changer_flag)
        self.ajouter_option("n", self.opt_changer_nom)
        self.ajouter_option("g", self.opt_changer_groupe)
    
    def opt_changer_flag(self, arguments):
        """Change l'état d'un flag
        Syntaxe : /f flag
        
        """
        membre = self.objet
        squelette = membre.parent
        flag = arguments.strip()
        if flag in FLAGS:
            squelette.changer_flag_membre(membre.nom,
                    membre.flags ^ FLAGS[flag])
            self.actualiser()
        else:
            self.pere << "|err|Ce flag n'est pas disponible.|ff|"
    
    def opt_changer_groupe(self, arguments):
        """Change le groupe du membre.
        
        Syntaxe : /g <nouveau groupe>
        
        """
        membre = self.objet
        squelette = membre.parent
        nom_groupe = arguments.strip()
        squelette.changer_groupe_membre(membre.nom, groupe)
        self.actualiser()
    
    def opt_changer_nom(self, arguments):
        """Change le nom
        Syntaxe : /n nom
        
        """
        membre = self.objet
        squelette = membre.parent
        nom = supprimer_accents(arguments).lower()
        if squelette.a_membre(nom):
            self.pere << "|err|Ce nom est déjà utilisé.|ff|"
        else:
            squelette.renommer_membre(membre.nom, arguments)
            self.actualiser()
    
    def accueil(self):
        """Message d'accueil du contexte"""
        membre = self.objet
        squelette = membre.parent
        msg = "| |tit|"
        msg += "Edition du membre {} de {}".format(
                membre.nom, squelette.cle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        
        msg += "\n Nom du membre : |ent|" + membre.nom + "|ff|"
        msg += "\n Groupe :|ent|" + (membre.groupe or "aucun") + "|ff|"
        msg += "\n Flags :"
        for flag in FLAGS:
            msg += "\n     " + flag + " : "
            if FLAGS[flag] & membre.flags:
                msg += "oui"
            else:
                msg += "non"
        return msg
