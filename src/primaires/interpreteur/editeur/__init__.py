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


"""Ce fichier est à la racine du package 'editeur'.
Dans ce fichier est définie la classe Editeur, héritée de Contexte.
Elle est détaillée plus bas.

"""

from primaires.format.fonctions import *
from ..contexte import Contexte, RCI_PREC
from .env_objet import EnveloppeObjet

class Editeur(Contexte):
    
    """Classe de base pour former des objets Editeur.
    Ces objets formeront l'architecture d'un éditeur.
    
    """
    
    nom = None
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Contexte.__init__(self, pere)
        self.opts.separateur = "+" + "-" * 77 + "+"
        self.opts.prompt_clr = ""
        self.opts.prompt_prf = ""
        self.objet = objet
        self.attribut = attribut
        self.prompt = ""
        self.apercu = ""
        self.aide_courte = ""
        self.aide_longue = ""
        self.options = {}
    
    def __getstate__(self):
        """On nettoie les options"""
        dico_attr = Contexte.__getstate__(self)
        dico_attr["options"] = dico_attr["options"].copy()
        for rac, fonction in dico_attr["options"].items():
            dico_attr["options"][rac] = fonction.__name__
        return dico_attr
    
    def __setstate__(self, dico_attr):
        """Récupération de l'éditeur"""
        Contexte.__setstate__(self, dico_attr)
        for rac, nom in self.options.items():
            fonction = getattr(self, nom)
            self.options[rac] = fonction
    
    def ajouter_option(self, option, fonction):
        """Ajoute une option.
        Les options sont appelables grâce au raccourci
        '/<option> <arguments>' dans l'éditeur.
        
        Si l'option est appelée, la fonction correspondante dans l'éditeur
        sera appelée. On lui passe en paramètre :
        *   les arguments réceptionnés sous la forme d'une chaîne
        
        """
        self.options[option] = fonction
    
    def actualiser(self):
        """Redéfinition d'actualiser.
        Au lieu de migrer sur 'self', on se contente d'envoyer le
        message d'accueil à 'self.pere'.
        
        """
        self.pere.envoyer(self.pere.contexte_actuel.opts.separateur)
        self.pere.envoyer(self.accueil())
    
    def get_apercu(self):
        """Retourne l'aperçu"""
        return self.apercu.format(objet = self.objet)
    
    def get_prompt(self):
        """Retourne le prompt"""
        prompt = self.prompt
        if not prompt:
            prompt = "-> "
        return prompt

    def receptionner(self, msg):
        """Méthode appelée quand l'éditeur reçoit un message.
        On le redirige vers 'interpreter' après avoir appliqué les options
        de réception.
        
        On déduit l'émetteur, c'est le père du contexte (self.pere).
        
        """
        emt = self.pere
        # Alias contextes
        res = self.traiter_alias_contextes(msg)
        if res:
            return
        
        if self.opts.echp_sp_cars:
            msg = echapper_sp_cars(msg)
        
        # Si un contexte précédent est défini et que le client a entré
        # RCI_PREC, on retourne au contexte précédent
        if self.opts.rci_ctx_prec and msg == RCI_PREC:
            self.migrer_contexte(self.opts.rci_ctx_prec)
        elif msg.startswith(RCI_PREC):
            # C'est une option
            # On extrait le nom de l'option
            mots = msg.split(" ")
            option = mots[0][1:]
            arguments = " ".join(mots[1:])
            if option not in self.options.keys():
                emt << "|err|Option invalide ({}).|ff|".format(option)
            else: # On appelle la fonction correspondante à l'option
                fonction = self.options[option]
                fonction(arguments)
        else:
            self.interpreter(msg)
    
    def migrer_contexte(self, contexte, afficher_accueil=True):
        """Redéfinition de la méthode 'migrer_contexte' de Contexte.
        Quand on migre un éditeur à l'autre, l'ancien éditeur doit être
        retiré de la pile.
        
        """
        self.fermer()
        Contexte.migrer_contexte(self, contexte, afficher_accueil)
        self.pere.contexte_actuel.pere = self.pere
