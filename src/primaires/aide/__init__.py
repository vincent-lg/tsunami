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


"""Fichier contenant le module primaire aide."""

from abstraits.module import *
from .sujet import SujetAide
from primaires.format.fonctions import supprimer_accents
from . import commandes
from .editeurs.hedit import EdtHedit

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire aide.
    
    Ce module gère l'aide in-game, c'est-à-dire les sujets d'aide
    (fichier ./sujet.py), la commande aide/help et l'éditeur hedit.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "aide", "primaire")
        self.__sujets = []
    
    def init(self):
        """Initialisation du module.
        
        On récupère les sujets d'aide enregistrés.
        
        """
        sujets = self.importeur.supenr.charger_groupe(SujetAide)
        self.__sujets = sujets
        print(len(sujets), "sujets d'aides récupérés.")
        
        BaseModule.init(self)
    
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.aide.CmdAide(),
            commandes.hedit.CmdHedit(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'hedit'
        self.importeur.interpreteur.ajouter_editeur(EdtHedit)
    
    def __getitem__(self, titre):
        """Retourne le sujet portant ce titre.
        
        Si le titre n'est pas trouvé, lève l'exception KeyError.
        
        La recherche du sujet se fait sans tenir compte des accents ou de
        la casse.
        
        """
        titre = supprimer_accents(titre).lower()
        for sujet in self.__sujets:
            if supprimer_accents(sujet.titre).lower() == titre:
                return sujet
        
        raise KeyError("le titre {} n'a pas pu être trouvé".format(titre))
    
    @property
    def sujets(self):
        """Retourne la liste déréférencée des sujets."""
        return list(self.__sujets)
    
    def ajouter_sujet(self, titre):
        """Ajoute un sujet à la liste des sujets d'aide.
        
        Le titre du sujet doit être fourni en paramètre.
        
        Si le titre est déjà utilisé, lève une exception.
        
        Sinon, retourne le sujet nouvellement créé.
        
        """
        titres_sujets = [supprimer_accents(s.titre).lower() for s in \
                self.__sujets]
        
        if supprimer_accents(titre).lower() in titres_sujets:
            raise ValueError("le titre {} est déjà utilisé".format(titre))
        sujet = SujetAide(titre)
        self.__sujets.append(sujet)
        return sujet
