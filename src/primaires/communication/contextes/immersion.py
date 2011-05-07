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
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.canal = None
        self.options = {
            # Options d'user
            "q" : self.opt_quit,
            "w" : self.opt_who,
            "h" : self.opt_help,
            "i" : self.opt_invite,
            # Options de modo
            "e" : self.opt_eject,
            "b" : self.opt_ban,
            # Options d'admin
            "p" : self.opt_promote,
            "d" : self.opt_dissolve,
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
        res = "> Immersion dans le canal " + canal.nom.ljust(53)
        
        return res
    
    def opt_quit(self, arguments):
        """Option quitter : /q"""
        personnage = self.pere.joueur
        self.canal.immerger_ou_sortir(personnage)
        
        personnage << "> Retour au jeu."
    
    def opt_who(self, arguments):
        """Option qui : /w"""
        personnage = self.pere.joueur
        res = "> Joueurs connectés :"
        for connecte in self.canal.connectes:
            if connecte in type(self).importeur.connex.joueurs_connectes:
                if connecte is self.canal.auteur:
                    statut = "|rgc|@"
                elif connecte in self.canal.moderateurs:
                    statut = "|jn|*"
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
        res = "> Aide du canal {} ({}) :".format(canal.nom, canal.resume)
        res += str(canal.description)
        res += "\n  Administrateur : |rgc|" + canal.auteur.nom + "|ff|"
        modos = ""
        if len(canal.moderateurs) == 1:
            modos = "\n  Modérateur : |jn|" + canal.moderateurs[0].nom + "|ff|"
        elif len(canal.moderateurs) > 1:
            modos = "\n  Modérateurs : |jn|" + "|ff|, |jn|".join(
                    sorted([modo.nom for modo in canal.moderateurs])) + "|ff|"
        res += modos
        res += "\n\n  Commandes disponibles :"
        res += "\n   - |cmd|/h|ff| : affiche ce message d'aide"
        res += "\n   - |cmd|/w|ff| : liste les joueurs connectés au canal"
        res += "\n   - |cmd|/i <joueur>|ff| : invite un joueur à rejoindre "
        res += "le canal"
        res += "\n   - |cmd|/q|ff| : permet de sortir du mode immersif"
        
        personnage << res
    
    def opt_invite(self, arguments):
        """Option pour inviter un ami à rejoindre le cana : /i <joueur>"""
        canal = self.canal
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez spécifier un joueur.|ff|"
            return
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for t_joueur in type(self).importeur.connex.joueurs_connectes:
            if nom_joueur == t_joueur.nom.lower():
                joueur = t_joueur
                break
        if joueur is None:
            self.pere.joueur << "|err|Le joueur passé en paramètre n'a pu " \
                    "être trouvé.|ff|"
            return
        if joueur in canal.connectes:
            self.pere.joueur << "|err|Ce joueur est déjà connecté au canal.|ff|"
            return
        res = "|vrc|" + self.pere.joueur.nom + " vous invite à rejoindre "
        res += "le canal" + canal.nom + ". Pour ce faire, entrez |ff||ent|+"
        res += canal.nom + "|ff||vrc|.|ff|"
        
        joueur << res
        self.pere.joueur << "|att|Vous venez d'inviter {} à rejoindre le " \
                "canal {}.|ff|".format(joueur.nom, canal.nom)
        
    
    def opt_eject(self, arguments):
        """Option permettant d'éjecter un joueur connecté : /e <joueur>"""
        canal = self.canal
        if not self.pere.joueur in canal.moderateurs and \
                self.pere.joueur is not canal.auteur:
            self.pere.joueur << "|err|Vous n'avez pas accès à cette option.|ff|"
            return
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez spécifier un joueur.|ff|"
            return
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for connecte in canal.connectes:
            if nom_joueur == connecte.nom.lower():
                joueur = connecte
                break
        if joueur is None:
            self.pere.joueur << "|err|Ce joueur n'est pas connecté au " \
                    "canal.|ff|"
            return
        if joueur is self.pere.joueur:
            self.pere.joueur << "|err|Vous ne pouvez vous éjecter " \
                    "vous-même.|ff|"
            return
        canal.ejecter(joueur)
    
    def opt_ban(self, arguments):
        """Option permettant de bannir un joueur connecté : /b <joueur>"""
        canal = self.canal
        if not self.pere.joueur in canal.moderateurs and \
                self.pere.joueur is not canal.auteur:
            self.pere.joueur << "|err|Vous n'avez pas accès à cette option.|ff|"
            return
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for t_joueur in type(self).importeur.connex.joueurs_connectes:
            if nom_joueur == t_joueur.nom.lower():
                joueur = t_joueur
                break
        if joueur is None:
            self.pere.joueur << "|err|Le joueur passé en paramètre n'a pu " \
                    "être trouvé.|ff|"
            return
        if joueur is self.pere.joueur:
            self.pere.joueur << "|err|Vous ne pouvez vous bannir vous-même.|ff|"
            return
        canal.bannir(joueur)
    
    def opt_promote(self, arguments):
        """Option permettant de promouvoir un joueur connecté : /p <joueur>"""
        canal = self.canal
        if self.pere.joueur is not canal.auteur:
            self.pere.joueur << "|err|Vous n'avez pas accès à cette option.|ff|"
            return
        nom_joueur = arguments.split(" ")[0]
        joueur = None
        for connecte in canal.connectes:
            if nom_joueur == connecte.nom.lower():
                joueur = connecte
                break
        if joueur is None:
            self.pere.joueur << "|err|Ce joueur n'est pas connecté au " \
                    "canal.|ff|"
            return
        if joueur is self.pere.joueur:
            self.pere.joueur << "|err|Vous ne pouvez vous promouvoir " \
                    "vous-même.|ff|"
            return
        if joueur is canal.auteur:
            self.pere.joueur << "|err|Ce joueur est déjà administrateur.|ff|"
            return
        canal.promouvoir_ou_dechoir(joueur)
        if joueur in canal.moderateurs:
            self.pere.joueur << "|att|{} a été promu modérateur.|ff|".format(
                    joueur.nom)
        else:
            self.pere.joueur << "|att|{} a été déchu du statut de " \
                    "modérateur.|ff|".format(joueur.nom)
    
    def opt_dissolve(self, arguments):
        """Option permettant de dissoudre le canal"""
        canal = self.canal
        if self.pere.joueur is not canal.auteur:
            self.pere.joueur << "|err|Vous n'avez pas accès à cette option.|ff|"
            return
        joueur = self.pere.joueur
        canal.rejoindre_ou_quitter(joueur, False)
        canal.immerger_ou_sortir(joueur, False)
        joueur << "|err|Le canal {} a été dissous.|ff|".format(canal.nom)
        canal.dissoudre()
    
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
