# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant le contexte 'jeux:plateau'"""

from primaires.format.constantes import ponctuations_finales

from primaires.interpreteur.contexte import Contexte

class Plateau(Contexte):
    
    """Contexte dans lequel on peut jouer à un jeu.
    
    """
    
    nom = "jeux:plateau"
    
    def __init__(self, pere, identifiant, objet):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        
        self.identifiant = identifiant
        self.objet = objet
        
        jeux = type(self).importeur.jeux
        if not objet is None:
            self.partie = jeux.get_partie(objet)
        
        self.options = {
            # Options d'user
            "q" : self.opt_quit
            }
    
    def __getnewargs__(self):
        return (None, 0, None)
    
    def __getstate__(self):
        """Nettoyage des options"""
        dico_attr = Contexte.__getstate__(self)
        dico_attr["options"] = dico_attr["options"].copy()
        for rac, fonction in dico_attr["options"].items():
            dico_attr["options"][rac] = fonction.__name__
        return dico_attr
    
    def __setstate__(self, dico_attr):
        """Récupération du contexte"""
        Contexte.__setstate__(self, dico_attr)
        for rac, nom in self.options.items():
            fonction = getattr(self, nom)
            self.options[rac] = fonction
    
    def accueil(self):
        """Message d'accueil du contexte"""
        res = "Vous rejoignez la partie\n"
        res += self.partie.plateau()
        return res
    
    def opt_quit(self, arguments):
        """Option quitter : /q"""
        try:
            self.partie.joueurs.remove(self.pere.joueur)
        except ValueError:
            pass
        self.pere.joueur.contextes.retirer()
        self.pere << "Vous quittez le plateau."
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        if msg.startswith("/"):
            # C'est une option
            # On extrait le nom de l'option
            mots = msg.split(" ")
            option = mots[0][1:]
            arguments = " ".join(mots[1:])
            if option not in self.options.keys():
                self.pere << "|err|Option invalide ({}).|ff|".format(option)
            else: # On appelle la fonction correspondante à l'option
                fonction = self.options[option]
                fonction(arguments)
        else:
            # On envoit au gestionnaire de jeu
            (perso, tous) = self.partie.jouer(self.identifiant, msg)
            if perso != "":
                self.pere << perso
            if tous != "":
                for joueur in self.partie.joueurs:
                    joueur << tous
                
            
