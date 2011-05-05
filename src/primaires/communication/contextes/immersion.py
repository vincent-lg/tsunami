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


"""Fichier contenant le contexte 'communication:immersion'"""

from primaires.interpreteur.contexte import Contexte

class Immersion(Contexte):
    
    """Contexte d'immersion dans un canal de communication.
    
    """
    
    nom = "communication:immersion"
    
    def __init__(self, pere, canal=None):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.canal = canal
        self.options = {
            "q" : self.opt_quit,
            "w" : self.opt_who,
            "h" : self.opt_help,
            "e" : self.opt_eject,
            }
    
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
        canal = self.canal
        res = "+" + "-" * 77 + "+" + "\n"
        res += "| |tit|Immersion dans le canal " + canal.nom.ljust(52) + "|ff||" + "\n"
        res += "+" + "-" * 77 + "+"
        
        return res
    
    def opt_quit(self, arguments):
        """Option quitter : /q"""
        personnage = self.pere.joueur
        self.canal.immerger(personnage)        
        personnage << "Fermeture de l'immersion."
    
    def opt_who(self, arguments):
        """Option qui : /w"""
        personnage = self.pere.joueur
        res = "- Joueurs connectés :"
        for connecte in self.canal.connectes:
            if connecte in type(self).importeur.connex.joueurs_connectes:
                if connecte is self.canal.auteur:
                    statut = "|rgc|@"
                elif connecte in self.canal.moderateurs:
                    statut = "|jnc|*"
                else:
                    statut = "|bc|"
                res += "\n  " + statut + connecte.nom + "|ff|"
                if connecte in self.canal.immerges:
                    res += " (immergé)"
        personnage << res
    
    def opt_help(self, arguments):
        """Options d'affichage de l'aide : /h"""
        personnage = self.pere.joueur
        canal = self.canal
        res = "- Aide du canal {} ({}) :".format(canal.nom, canal.resume)
        res += str(canal.description)
        modos = ""
        if len(canal.moderateurs) == 1:
            modos = "\n  Modérateurs : " + canal.moderateurs[0].nom
        elif len(canal.moderateurs) > 1:
            modos = "\n  Modérateurs : " + ", ".join(
                    sorted([modo.nom for modo in canal.moderateurs]))
        res += modos
        res += "\n  Commandes disponibles : /h, /q, /w"
        personnage << res
    
    def opt_eject(self, arguments):
        return # a effacer pour mise en service
        """Option permettant d'éjecter un joueur connecté : /e <joueur>"""
        canal = self.canal
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for connecte in canal.connectes:
            nom = connecte.nom.lower()
            if nom == nom_joueur:
                joueur = connecte
        if joueur is None:
            self.pere.joueur << "Ce joueur n'est pas connecté au canal."
        else:
            if joueur is self.pere.joueur:
                self.pere.joueur << "Vous ne pouvez vous éjecter vous-même."
            else:
                if joueur in canal.immerges:
                    canal.immerger(joueur)
                    joueur.contextes.retirer()
                canal.connecter(joueur)
                joueur << "Vous avez été éjecté du canal {}.".format(canal.nom)
    
    def opt_promod(self, arguments):
        return # a effacer pour mise en service
        canal = self.canal
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for connecte in canal.connectes:
            nom = connecte.nom.lower()
            if nom == nom_joueur:
                joueur = connecte
        if joueur is None:
            self.pere.joueur << "Ce joueur n'est pas connecté au canal."
        else:
            if joueur is self.pere.joueur:
                self.pere.joueur << "Vous ne pouvez vous promouvoir vous-même."
            else:
                canal.moderateurs.append(joueur)
                joueur << "Vous avez été promu modérateur sur le canal " \
                        "{}.".format(canal.nom)
    
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
            self.canal.envoyer(self.pere.joueur, msg)
