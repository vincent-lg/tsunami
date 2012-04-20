# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la classe CommandeDynamique détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.interpreteur.commande.commande import Commande

class CommandeDynamique(BaseObj):
    
    """Classe décrivant les commandes dynamiques.
    
    Une commande dynamique est une commande de l'univers, mais
    au lieu d'être définie statiquement (comme le sont la plupart
    des commandes usuelles, regarder/look, prendre/get, manger/eat...),
    elles peuvent être manipulées par des éditeurs et ajoutées ou
    retirées par des immortels.
    
    Ces commandes doivent être, pour le joueur les utilisant, aussi proche
    des commandes statiques que possible.
    
    L'ajout d'une commande dynamique permet l'ajout d'un nouvel
    évènement dans les objets scriptables qui sera appelé pour interragir
    avec l'élément observé désigné par le joueur. Par exemple, si
    le joueur entre :
        push mur
    Que la commande pousser/push est une commande dynamique et que 'mur'
    est un détail visible dans la salle du joueur, l'évènement
    'pousser' de ce détail sera appelé avec certains paramètres.
    
    """
    
    enregistrer = True
    
    def __init__(self, nom_francais, nom_anglais):
        """Constructeur d'une commande dynamique."""
        self.nom_francais = nom_francais
        self.nom_anglais = nom_anglais
        self.nom_categorie = "divers"
        self.aide_courte = "à renseigner..."
        self.aide_longue = Description(parent=self, scriptable=False)
        self.aide_courte_evt = "Un personnage fait quelque chose"
        self.aide_longue_evt = Description(parent=self, scriptable=False)
    
    def __getnewargs__(self):
        return ("", "")
    
    def __repr__(self):
        return "<Commande dynamique '{}/{}'>".format(
                self.nom_francais, self.nom_anglais)
    
    def __str__(self):
        return self.nom_francais + "/" + self.nom_anglais
    
    def ajouter(self):
        """Ajoute la commande dans l'interpréteur.
        
        Il est préférable de faire cela après l'insertion des commandes
        statiques dans l'interpréteur, c'est-à-dire durant la phase de
        préparation du module.
        
        """
        commande = Commande(self.nom_francais, self.nom_anglais)
        commande.nom_categorie = self.nom_categorie
        commande.aide_courte = self.aide_courte
        commande.aide_longue = str(self.aide_longue)
        #commande.schema = "<element_observable>"
        commande.interpreter = self.interpreter
        importeur.interpreteur.ajouter_commande(commande)
       
    def interpreter(self, personnage, dic_masques):
        personnage << "pop !"
