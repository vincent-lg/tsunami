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


"""Ce fichier est à la racine du package 'contexte', définissant plusieurs
types de contexte, chacun avec son paquet propre.

Ce fichier définit aussi la classe Contexte, classe-mère de tous les contextes
développés dans ce package.

"""

from abstraits.obase import BaseObj
from primaires.format.fonctions import *

contextes = {} # dictionnaire des différents contextes

class MetaContexte(type):
    
    """Métaclasse des contextes.
    A chaque fois qu'on crée une classe héritée de Contexte avec un nom
    valide, on l'ajoute dans le dictionnaire 'contextes'.
    
    """
    
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        if cls.nom:
            contextes[cls.nom] = cls

class OptionsContexte:
    """Options du contexte.
    
    Liste des options :
    Options de réception :
    *   echp_sp_cars - échapper les caractères spéciaux du message :
        Si cette option est à True, les caractères spéciaux entrés
        par le client seront échappés.
        Si cette option est à False, les caractères spéciaux ne seront pas
        échappés ce qui permet au client d'entrer des caractères spéciaux (sauts
        de ligne, couleurs...).
    
    Options d'envoi :
    *   aff_sp_cars : affiche les caractères spéciaux
        Utile dans un contexte qui a également l'option 'echp_sp_cars' à
        False. Elle échape les caractères spéciaux envoyé au client.
    *   sup_accents - on supprime les accents du message avant de l'envoyer
    *   prompt_clr - colorisation du prompt :
        Si un code couleur est précisé dans cette option, on l'applique au
        prompt pour le faire ressortir sur le texte
    *   prompt_prf - préfixage du prompt :
        Contient une chaîne de caractères (str) qui est utilisée en tant que
        préfixe du prompt, pour le faire ressortir par rapport aux instructions.
    Ces dernières options dépendent de l'activation ou non de l'option ncod.
    
    Options de navigation :
    *   rci_ctx_prec - raccourci vers le contexte précédent :
        Si un contexte précédent est entré dans cette option, le client pourra
        l'atteindre automatiquement en entrant le raccourci de retour
        (voir la constante 'RCI_PREC').
    
    """    
    def __init__(self):
        """Constructeur par défaut des options"""
        # Options de réception
        self.echp_sp_cars = True
        
        # Options d'envoi
        self.aff_sp_cars = False
        self.sup_accents = False
        self.prompt_clr = ""
        self.prompt_prf = ""
        
        # Options de navigation
        self.rci_ctx_prec = ""

RCI_PREC = "/"

class Contexte(BaseObj, metaclass=MetaContexte):
    """Classe abstraite définissant un contexte.
    Si vous voulez utiliser un contexte :
    *   Choisissez-le dans les classes-filles de Contexte
    *   Créez une nouvelle sous-classe de Contexte correspondant mieux à vos
        attentes
    
    Cette classe est abstraite. Aucun objet ne doit être créé directement
    depuis cette classe. L'architecture de chaque contexte est à la charge du
    paquet concerné. Consultez la documentation de la classe avant de l'utiliser
    comme contexte.
    
    Les contextes sont des formes d'interpréteur destinés à remplir
    une mission bien précise. Ces contextes sont souvent chaînés.
    
    Par exemple, le contexte chargé de demander son nom à l'utilisateur
    va avoir plusieurs sorties pereibles :
    *   Si le joueur entre un nom valide :
        *   Si le nom existe, on charge le personnage lié à ce nom
            et on redirige le joueur sur le contexte 'entrer le mot de passe'
        *   Si le nom n'existe pas, on redirige vers le contexte chargé
            de la création de personnage
    *   Si le nom est invalide, on demande au joueur de l'entrer à nouveau
        Autrement dit, on lui affiche un message d'erreur et on le redirige sur
        le même contexte.
    
    Il s'agit d'un exemple simple, mais des contextes peuvent être plus
    complexes, notamment les éditeurs. En fonction de la récurrence d'un
    contexte, des objets hérités devront être créés avec un certain nombre de
    comportements par défaut déjà programmés.
    
    Pour plus d'informations, visiter les sous-paquets.

    """
    importeur = None
    nom = None
    
    def __init__(self, pere):
        """Constructeur d'un contexte."""
        BaseObj.__init__(self)
        self.pere = pere
        self.opts = OptionsContexte()
        # Récupération du fichier de configuration de la charte graphique
        cfg_charte = type(self.importeur).anaconf.get_config("charte_graph")
        self.opts.prompt_clr = cfg_charte.couleur_prompt
        self.opts.prompt_prf = cfg_charte.prefixe_prompt
    
    def __getinitargs__(self):
        """Méthode retournant les valeurs par défaut du constructeur"""
        return (None, )
    
    def entrer(self):
        """Méthode appelée quand le père entre dans le contexte"""
        pass
    
    def sortir(self):
        """Méthode appelée quand le père sort du contexte"""
        pass
    
    def get_prompt(self):
        """Retourne le prompt qui sera affiché à chaque message envoyé"""
        return ""
    
    def accueil(self):
        """Retourne un message d'accueil au père du contexte.
        Ce message est envoyé à chaque fois que le client reçoit un message et
        qu'il est dans ce contexte.
        
        """
        return ""
    
    def deconnecter(self):
        """Méthode appelée quand le père se déconnecte du contexte
        (déconnexion non demandée, on ne sort pas du contexte naturellement)
        
        """
        pass
    
    def _get_contexte(self, nom_contexte):
        """Récupère depuis l'interpréteur l'instance du contexte
        dont le nom est fourni.
        
        """
        return type(self).importeur.interpreteur.contextes[nom_contexte]

    def actualiser(self):
        """Méthode appelée pour boucler sur le contexte courant.
        Cela veut dire qu'on ne change pas de contexte, on migre vers 'self'.
        L'émetteur reçoit ainsi le message d'accueil du contexte.
        
        """
        self.migrer_contexte(type(self).nom)
    
    def migrer_contexte(self, contexte, afficher_accueil=True):
        """Cas de transfert de contexte.
        Le contexte doit être donné sous la forme d'un nom (type 'str').
        
        """
        if type(contexte) is str:
            nouveau_contexte = self._get_contexte(contexte)(self.pere)
        else:
            nouveau_contexte = contexte
        
        self.pere.contexte_actuel.sortir()
        self.pere.migrer_contexte(nouveau_contexte)
        self.pere.contexte_actuel.entrer()
        if nouveau_contexte is self.pere.contexte_actuel and afficher_accueil:
            # Cette condition est là pour éviter qu'en cas de migration de
            # contexte dans la méthode 'entrer', le message d'accueil ne
            # s'affiche en double
            self.pere.envoyer(self.pere.contexte_actuel.accueil())
    
    def interpreter(self, msg):
        """Méthode appelée quand le contexte reçoit un message à interpréter.
            msg - le message sous la forme d'une chaîne
        
        On déduit l'émetteur, c'est le père du contexte (self.pere).
        
        """
        pass
    
    def receptionner(self, msg):
        """Méthode appelée quand le contexte reçoit un message.
        On le redirige vers 'interpreter' après avoir appliqué les options
        de réception.
        
        CETTE METHODE NE DOIT PAS ETRE REDEFINIE.
        
        On déduit l'émetteur, c'est le père du contexte (self.pere).
        
        """
        emt = self.pere
        if self.opts.echp_sp_cars:
            msg = echapper_sp_cars(msg)
        
        # Si un contexte précédent est défini et que le client a entré
        # RCI_PREC, on retourne au contexte précédent
        if self.opts.rci_ctx_prec and msg == RCI_PREC:
            self.migrer_contexte(self.opts.rci_ctx_prec)
        else:
            self.interpreter(msg)
