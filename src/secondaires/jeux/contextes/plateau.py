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
    
    def __init__(self, pere, objet):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        
        self.objet = objet
        
        self.options = {
            # Options d'user
            "q" : self.opt_quit,
            "p" : self.opt_pause,
            "d" : self.opt_demarrer,
            "s" : self.opt_dire
            }
    
    def __getnewargs__(self):
        return (None, None)
    
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
        res = "Vous rejoignez la partie\n\n"
        res += "/q pour quitter\n"
        res += "/p pour mettre/enlever la pause\n"
        res += "/d pour pour démarrer\n"
        res += "/s pour dire quelque chose à votre adversaire\n"
        return res
    
    def opt_demarrer(self, arguments):
        """Option pause : /d"""
        partie = type(self).importeur.jeux.get_partie(self.objet)
        if not partie.demarrer():
            self.pere << "Impossible de démarrer la partie."
    
    def opt_pause(self, arguments):
        """Option pause : /p"""
        partie = type(self).importeur.jeux.get_partie(self.objet)
        if not partie.pause():
            self.pere << "Impossible de mettre en pause."
    
    def opt_dire(self, arguments):
        """Option pause : /s"""
        jeux = type(self).importeur.jeux
        jeux.get_partie(self.objet).dire(self.pere.joueur, arguments)
    
    def opt_quit(self, arguments):
        """Option quitter : /q"""
        partie = type(self).importeur.jeux.get_partie(self.objet)
        try:
            partie.quitter(self.pere.joueur)
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
            type(self).importeur.jeux.get_partie(self.objet).jouer(self.pere.joueur, msg)
                
            
