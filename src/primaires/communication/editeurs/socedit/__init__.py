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


"""Package contenant l'éditeur 'socedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Auquel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur import Editeur
from primaires.communication.attitude import STATUTS

class EdtSocedit(Editeur):
    
    """Classe définissant l'éditeur d'attitude 'socedit'.
    
    """
    
    nom = "socedit"
    
    def __init__(self, personnage, objet, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Editeur.__init__(self, instance_connexion, objet, attribut)
        self.personnage = personnage
        self.ajouter_option("q", self.opt_quitter)
        self.ajouter_option("c", self.opt_changer_cle)
        self.ajouter_option("aim", self.opt_aim)
        self.ajouter_option("aif", self.opt_aif)
        self.ajouter_option("oim", self.opt_oim)
        self.ajouter_option("oif", self.opt_oif)
        self.ajouter_option("adm", self.opt_adm)
        self.ajouter_option("adf", self.opt_adf)
        self.ajouter_option("idm", self.opt_idm)
        self.ajouter_option("idf", self.opt_idf)
        self.ajouter_option("odm", self.opt_odm)
        self.ajouter_option("odf", self.opt_odf)
    
    def __getnewargs__(self):
        return (None, None)
    
    def accueil(self):
        """Méthode d'accueil de l'éditeur"""
        attitude = self.objet
        msg = "| |tit|Edition de l'attitude {}|ff|".format(
                attitude.cle).ljust(87) + "|\n"
        msg += self.opts.separateur + "\n"
        msg += \
            "Utilisez une des options pour paramétrer l'attitude.\n" \
            "Statut actuel de l'attitude : " + STATUTS[attitude.statut] + "\n" \
            "Clé (commande entrée par le joueur) : |cmd|" + \
            attitude.cle + "|ff|\n\n" \
            "Options :" \
            "\n - |cmd|/aim|ff|, |cmd|/aif|ff|, |cmd|/oim|ff|... : édite un " \
            "paramètre de l'attitude" \
            "\n - |cmd|/c|ff| : change la clé" \
            "\n - |cmd|/q|ff| : permet de quitter l'éditeur" \
            "\n - |cmd|/d|ff| : supprimer l'attitude\n\n"
        msg += "AIM (Acteur Indépendant Masculin) :\n |ent|"
        msg += attitude.independant["aim"] or \
                "Vous vous faites tout petit."
        msg += "|ff|\nAIF (Acteur Indépendant Féminin) :\n |ent|"
        msg += attitude.independant["aif"] or \
                "Vous vous faites toute petite."
        msg += "|ff|\nOIM (Observateur Indépendant Masculin) :\n |ent|"
        msg += attitude.independant["oim"] or \
                "|acteur| se fait tout petit."
        msg += "|ff|\nOIF (Observateur Indépendant Féminin) :\n |ent|"
        msg += attitude.independant["oif"] or \
                "|acteur| se fait toute petite."
        msg += "|ff|\nADM (Acteur Dépendant Masculin) :\n |ent|"
        msg += attitude.dependant["adm"] or \
                "Vous vous faites tout petit devant |cible|."
        msg += "|ff|\nADF (Acteur Dépendant Féminin) :\n |ent|"
        msg += attitude.dependant["adf"] or \
                "Vous vous faites toute petite devant |cible|."
        msg += "|ff|\nIDM (Interlocuteur Dépendant Masculin) :\n |ent|"
        msg += attitude.dependant["idm"] or \
                "|acteur| se fait tout petit devant vous."
        msg += "|ff|\nIDF (Interlocuteur Dépendant Féminin) :\n |ent|"
        msg += attitude.dependant["idf"] or \
                "|acteur| se fait toute petite devant vous."
        msg += "|ff|\nODM (Observateur Dépendant Masculin) :\n |ent|"
        msg += attitude.dependant["odm"] or \
                "|acteur| se fait tout petit devant |cible|."
        msg += "|ff|\nODF (Observateur Dépendant Féminin) :\n |ent|"
        msg += attitude.dependant["odf"] or \
                "|acteur| se fait toute petite devant |cible|."
        
        return msg + "|ff|"
    
    def opt_quitter(self, arguments):
        """Option quitter"""
        self.pere.joueur.contextes.retirer()
        self.pere.envoyer("Fermeture de l'éditeur.")
    
    def opt_changer_cle(self, arguments):
        """Option permettant de changer la clé de l'attitude"""
        self.objet.cle = arguments
        self.actualiser()
    
    def opt_aim(self, arguments):
        self.objet.independant["aim"] = arguments
        self.actualiser()
   
    def opt_aif(self, arguments):
        self.objet.independant["aif"] = arguments
        self.actualiser()
    
    def opt_oim(self, arguments):
        self.objet.independant["oim"] = arguments
        self.actualiser()
    
    def opt_oif(self, arguments):
        self.objet.independant["oif"] = arguments
        self.actualiser()
    
    def opt_adm(self, arguments):
        self.objet.independant["adm"] = arguments
        self.actualiser()
   
    def opt_adf(self, arguments):
        self.objet.independant["adf"] = arguments
        self.actualiser()
    
    def opt_idm(self, arguments):
        self.objet.independant["idm"] = arguments
        self.actualiser()
   
    def opt_idf(self, arguments):
        self.objet.independant["idf"] = arguments
        self.actualiser()
    
    def opt_odm(self, arguments):
        self.objet.independant["odm"] = arguments
        self.actualiser()
    
    def opt_odf(self, arguments):
        self.objet.independant["odf"] = arguments
        self.actualiser()
