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


"""Package contenant la commande 'acheter'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.commerce.transaction import *

class CmdAcheter(Commande):
    
    """Commande 'acheter'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "acheter", "buy")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <objet:nom_objet_magasin|id_objet_magasin>"
        self.aide_courte = "achète un objet"
        self.aide_longue = \
            "Cette commande permet d'acheter des objets dans un magasin. " \
            "Vous devez posséder l'argent nécessaire sur vous. Notez " \
            "que le magasin peut avoir à vous rendre une partie de " \
            "l'argent si vous ne possédez pas exactement la somme " \
            "requise, mais plus. Vous devez également pouvoir prendre " \
            "l'article, sans quoi la transaction est annulée."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if salle.magasin is None:
            personnage << "|err|Il n'y a pas de magasin ici.|ff|"
            return
        magasin = salle.magasin
        nb_obj = dic_masques["nombre"].nombre if \
            dic_masques["nombre"] is not None else 1
        no_ligne = dic_masques["objet"].no_ligne
        service, qtt = magasin.inventaire[no_ligne]
        if qtt < nb_obj:
            nb_obj = qtt
        
        somme = service.m_valeur * nb_obj
        
        # On crée la transaction associée
        try:
            transaction = Transaction.initier(personnage, magasin, somme)
        except FondsInsuffisants:
            personnage << "|err|Vous n'avez pas assez d'argent.|ff|"
            return
        
        # Distribution des objets
        service.acheter(nb_obj, magasin, transaction)
        personnage << "Vous achetez {}.".format(service.get_nom(nb_obj))
