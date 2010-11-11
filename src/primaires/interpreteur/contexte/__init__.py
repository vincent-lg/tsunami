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


"""Ce fichier est à la racine du package 'contexte', définissant plusieurs
types de contexte, chacun avec son paquet propre.

Ce fichier définit aussi la classe Contexte, classe-mère de tous les contextes
développés dans ce package.

"""

from primaires.format.fonctions import *

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
    
    Options d'envoie :
    *   ncod - encoder les messages à envoyer :
        Si cette option est à True, on encode le message avant de l'envoyer
        en fonction de l'encodage précisé (voir l'option emt_ncod)
        Si cette option est à False, on n'encode rien avant d'envoyer
        (on part donc du principe qu'on reçoit un type 'bytes')
    *   emt_ncod - encoder les messages à envoyer grâce à l'encodage de
        l'émetteur :
        Pour que cette option soit prise en compte, l'option 'ncod' doit être
        à True.
        Si l'option 'emt_ncod' est à True, on encodera les messages à envoyer
        en fonction de l'encodage précisé danss l'émetteur (attribut
        'encodage' de l'objet 'emt')
        Si cette option est à False, on encode grâce à l'encodage par défaut
        (Utf-8).
    *   sup_accents - on supprime les accents du message avant de l'envoyer
        Attention : cette option n'est efficace que si 'ncod' est à True.
    *   prompt_clr : colorisation du prompt
        Si un code couleur est précisé dans cette option, on l'applique au
        prompt pour le faire ressortir sur le texte
    
    Options de navigation :
    *   rci_ctx_prec - raccourci vers le contexte précédent :
        Si un contexte précédent est entré dans cette option, le client pourra
        l'atteindre automatiquement en entrant le raccourci de retour
        (voir la constante 'RCI_PREC')
    
    """
    def __init__(self):
        """Constructeur par défaut des options"""
        # Options de réception
        self.echp_sp_cars = True
        
        # Options d'envoie
        self.emt_ncod = True
        self.sup_accents = False
        self.ncod = True
        self.prompt_clr = "|jn|"
        
        # Options de navigation
        self.rci_ctx_prec = ""

RCI_PREC = "/"

class Contexte:
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
    va avoir plusieurs sorties possibles :
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
    
    def __init__(self, nom):
        """Constructeur d'un contexte."""
        self.nom = nom
        type(self).importeur.interpreteur.ajouter_contexte(self)
        self.opts = OptionsContexte()
    
    def get_prompt(self, emt):
        """Retourne le prompt qui sera affiché à chaque message envoyé"""
        return ""
    
    def accueil(self, emt):
        """Retourne un message d'accueil à l'émetteur.
        Ce message est envoyé à chaque fois que le joueur arrive dans ce
        contexte.
        
        """
        return ""
    
    def deconnecter(self, emt):
        """Méthode appelée quand l'émetteur se déconnecte du contexte
        (déconnexion non demandée, on ne sort pas du contexte naturellement)
        
        """
        pass
    
    def get_contexte(self, nom_contexte):
        """Récupère depuis l'interpréteur l'instance du contexte
        dont le nom est fourni.
        
        """
        return type(self).importeur.interpreteur.contextes[nom_contexte]

    def actualiser(self, emt):
        """Méthode appelée pour boucler sur le contexte courant.
        Cela veut dire qu'on ne change pas de contexte, on migre vers 'self'.
        L'émetteur reçoit ainsi le message d'accueil du contexte.
        
        """
        self.migrer_contexte(emt, self)
    
    def migrer_contexte(self, emt, contexte):
        """Cas de transfert de contexte.
        Le contexte peut être donné sous la forme d'un nom (type 'str')
        ou d'un objet contexte.
        
        """
        if type(contexte) is str:
            nouveau_contexte = self.get_contexte(contexte)
        else:
            nouveau_contexte = contexte
        
        emt.migrer_contexte(nouveau_contexte)
        emt.contexte_actuel.envoyer(emt, emt.contexte_actuel.accueil(emt))
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand le contexte reçoit un message à interpréter.
            emt - l'émetteur du message
            msg - le message sous la forme d'une chaîne
        
        """
        pass
    
    def receptionner(self, emt, msg):
        """Méthode appelée quand le contexte reçoit un message.
        On le redirige vers 'interpreter' après avoir appliqué les options
        de réception.
        
        CETTE METHODE NE DOIT PAS ETRE REDEFINIE.
        
        """
        if self.opts.echp_sp_cars:
            msg = echapper_sp_cars(msg)
        
        # Si un contexte précédent est défini et que le client a entré
        # RCI_PREC, on retourne au contexte précédent
        if self.opts.rci_ctx_prec and msg == RCI_PREC:
            self.migrer_contexte(emt, self.opts.rci_ctx_prec)
        else:
            self.interpreter(emt, msg)
    
    def envoyer(self, emt, msg):
        """Méthode appelée quand on souhaite envoyer un message à
        l'émetteur.
        
        """
        # On ajoute le prompt à msg
        prompt = self.get_prompt(emt)
        if self.opts.prompt_clr and self.opts.ncod:
            prompt = self.opts.prompt_clr + prompt + "|ff|"
        if type(msg) == bytes:
            sep = b"\n\n"
            if type(prompt) == str:
                prompt = prompt.encode()
            msg += sep + prompt
        else:
            msg += "\n\n" + prompt
        if type(msg) == str:
            # Ajout de la couleur
            msg = ajouter_couleurs(msg)
            
            # On échappe les caractères spéciaux
            msg = remplacer_sp_cars(msg)
        
            # Suppression des accents si l'option est activée
            if self.opts.sup_accents:
                msg = supprimer_accents(msg)
            if self.opts.emt_ncod:
                msg = msg.encode(emt.encodage)
            else:
                msg = msg.encode()
        
        # On remplace les sauts de ligne
        msg = convertir_nl(msg)
        
        emt.envoyer(msg)
